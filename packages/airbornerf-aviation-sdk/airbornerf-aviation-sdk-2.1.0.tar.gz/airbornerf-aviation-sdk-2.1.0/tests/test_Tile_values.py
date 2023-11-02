import csv
import json
import logging
import os
import random
import subprocess
from collections import namedtuple
from importlib.resources import files
from typing import List, Dict

import pytest

from arf.Tile import Tile
from arf.TileConstants import TileConstants

class TestPutGetNode:

    @pytest.mark.parametrize('dtype', [TileConstants.DTypes.UINT1, TileConstants.DTypes.UINT4, TileConstants.DTypes.UINT16])
    @pytest.mark.parametrize('xdim', [1, 360, 361])
    @pytest.mark.parametrize('ydim', [1, 360, 361, 180, 181])
    @pytest.mark.parametrize('zdim', [1, 4, 8])
    def test_put_get_node(self, caplog, dtype: TileConstants.DTypes, xdim: int, ydim: int, zdim: int):
        '''
        Tests whether the value val that was written at node (x,y,z) with putNode(x,y,z)
        can be correctly recovered with getNode(x,y,z),
        if val is in the value range of the Tile (as specified by the data type and offset).
        :param caplog:
        :return: None
        '''

        caplog.set_level(logging.DEBUG)

        logging.info(f'Testing write of tiles with dType {str(dtype)}')

        valueOffset = -1
        tile = Tile(latitude=47, longitude=16, xsize=xdim, ysize=ydim, zsize=zdim, altitude=0, verticalResolution=1,
                    density=TileConstants.get_bitwidth(dtype), valueOffset=valueOffset)

        # The tiles are filled with randomn values.
        # The range of the values is { 0,1,.., valueMax}, and depends on the tile's data type:
        valueMax = 1 if dtype == TileConstants.DTypes.UINT1 else (1 << (TileConstants.get_bitwidth(dtype) - 1)) - 1

        expected_values = self._create_expected_values_map(xdim=xdim, ydim=ydim, zdim=zdim, value_range_min=0, value_range_max=valueMax)

        # Fill the tile with values:
        for x in range(0, xdim):
            for y in range(0, ydim):
                for z in range(0, zdim):
                    tile.putNode(expected_values[x][y][z], x, y, z)

        # Read from tile and compare with the expected values:
        for x in range(0, xdim):
            for y in range(0, ydim):
                for z in range(0, zdim):
                    assert (expected_values[x][y][z] == tile.getNode(x, y, z))

    def _create_expected_values_map(self, xdim, ydim, zdim, value_range_min, value_range_max):

        expected_values = {}

        for x in range(0, xdim):
            expected_values[x] = {}
            for y in range(0, ydim):
                expected_values[x][y] = {}
                for z in range(0, zdim):
                    expected_values[x][y][z] = random.randint(value_range_min, value_range_max)

        return expected_values


class TestTileFileValues:

    TileValuesTestCase = namedtuple('TileValuesTestCase', 'tile_path expected_values_path expected_tile_dim_path')

    def test_tile_file_values(self, tmpdir):
        '''
        Tests whether a tile that was initialized from a (tile) holds the correct node values,
        in the sense that Tile::getNode yields that expected result.
        Test cases for various densities and offsets are contained in tests/fixtures/tiletestcases.tar.gz.
        '''

        test_cases = self._tile_test_cases(tmpdir)

        for test_case in test_cases:
            with open(test_case.expected_tile_dim_path) as tile_dim_json_file:
                expected_tile_dim = json.load(tile_dim_json_file)
            expected_values = self._parse_expected_values(expected_values_csv_path=test_case.expected_values_path,
                                                          tile_dim=expected_tile_dim)

            tile = Tile(tileFilename=test_case.tile_path)

            assert (tile.header.xsize == expected_tile_dim['xsize'])
            assert (tile.header.ysize == expected_tile_dim['ysize'])
            assert (tile.header.zsize == expected_tile_dim['zsize'])

            for x in range(0, tile.header.xsize):
                for y in range(0, tile.header.ysize):
                    for z in range(0, tile.header.zsize):
                        assert (expected_values[x][y][z] == tile.getNode(x, y, z))

    def _tile_test_cases(self, tmpdir) -> List[TileValuesTestCase]:
        testdatadir = files("tests").joinpath("fixtures")

        tile_test_cases_tar = os.path.join(testdatadir, "tiletestcases.tar.gz")
        tile_test_cases_dir = os.path.join(tmpdir, "tiletestcases")
        os.makedirs(tile_test_cases_dir)
        self._extract_tar(tile_test_cases_tar, tile_test_cases_dir)
        test_data_path = os.path.join(tile_test_cases_dir, "tiletestcases")

        for path in os.listdir(test_data_path):
            dir = os.path.join(test_data_path, path)
            self._extract_gzip( os.path.join(dir, 'test_tile.tile.gz'))

        test_cases: List[TestTileFileValues.TileValuesTestCase] = []

        for test_case_folder in os.listdir(test_data_path):
            test_case_path = os.path.join(test_data_path, test_case_folder)
            test_case = TestTileFileValues.TileValuesTestCase(
                expected_values_path=os.path.join(test_case_path, "expected_values.csv"),
                tile_path=os.path.join(test_case_path, "test_tile.tile"),
                expected_tile_dim_path=os.path.join(test_case_path, "expected_tile_dim.json"))
            test_cases.append(test_case)

        assert (96 == len(test_cases))

        return test_cases

    def _parse_expected_values(self, expected_values_csv_path: str, tile_dim: json) -> Dict[ int, Dict[int, Dict[int, int]]]:
        # pre-create the result_map with the expected dimensions:
        result_map = {}

        xsize, ysize, zsize = tile_dim['xsize'], tile_dim['ysize'], tile_dim['zsize']

        for x in range(0, xsize):
            result_map[x] = {}
            for y in range(0, ysize):
                result_map[x][y] = {}
                for z in range(0, zsize):
                    result_map[x][y][z] = {}

        with open(expected_values_csv_path) as f:
            reader = csv.reader(f)

            for z, row in enumerate(reader, 0):
                assert (len(row) == xsize * ysize)
                for y in range(0, ysize):
                    for x in range(0, xsize):
                        result_map[x][y][z] = int(row[y * xsize + x])

        assert z == zsize - 1
        return result_map

    def _extract_tar(self, source_path, target_path):
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        fc = subprocess.Popen(["tar", "-xzf", source_path,
                               "--directory", target_path],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        fc.communicate()

    def _extract_gzip(self, source_path):
        fc = subprocess.Popen(["gzip", "-d", source_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        fc.communicate()
