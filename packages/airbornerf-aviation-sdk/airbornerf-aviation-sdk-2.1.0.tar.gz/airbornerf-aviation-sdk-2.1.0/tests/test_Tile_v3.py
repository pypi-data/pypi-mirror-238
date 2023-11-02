from arf.Tile import Tile
import tempfile
import subprocess
import shutil
import logging
import math
import random


class TestClass(object):

	def test_tile(self, caplog):
		caplog.set_level(logging.DEBUG)

		with tempfile.TemporaryDirectory() as tmpdirname:
			shutil.copy('tests/fixtures/n47e016_elevation_v3.tile.bz2', tmpdirname)
			subprocess.check_output(["bzip2", "-d", tmpdirname + '/n47e016_elevation_v3.tile.bz2'],
			                        stderr=subprocess.STDOUT)
			tileFilename = tmpdirname + '/n47e016_elevation_v3.tile'

			tile = Tile(tileFilename)
			assert tile.header.xsize == 3600
			assert tile.header.ysize == 3600
			assert tile.header.zsize == 1

			statistics = tile.getElevationTileStatisticsHeader()
			assert statistics is not None
			assert statistics.minElevation == 99
			assert statistics.maxElevation == 1318

			# Check some heights
			(x, y, z) = tile.getTileCoordinates(47.843099, 16.259886, 0)
			assert tile.getNode(x, y, 0) == 265

			(x, y, z) = tile.getTileCoordinates(47.661540, 16.277572, 0)
			assert tile.getNode(x, y, 0) == 629

			(x, y, z) = tile.getTileCoordinates(47.348019, 16.412280, 0)
			assert tile.getNode(x, y, 0) == 812

			(x, y, z) = tile.getTileCoordinates(47.855793, 16.769651, 0)
			assert tile.getNode(x, y, 0) == 110

			assert tile.getTileCoordinates(47.843099, 16.259886, 0) == (936, 564, 0)
			assert tile.getTileCoordinates(47.855793, 16.769651, 0) == (2771, 518, 0)

			assert tile.getLatLong(0, 0) == (16.0, 47.99972152709961)
			assert tile.getLatLong(0, 3600) == (16.0, 46.99972152709961)
			assert tile.getLatLong(3600, 0) == (17.0, 47.99972152709961)
			assert tile.getLatLong(3600, 3600) == (17.0, 46.99972152709961)

	def test_checksum(self, caplog):

		caplog.set_level(logging.DEBUG)

		with tempfile.TemporaryDirectory() as tmpdirname:
			shutil.copy('tests/fixtures/n47e016_elevation_v3.tile.bz2', tmpdirname)
			subprocess.check_output(["bzip2", "-d", tmpdirname + '/n47e016_elevation_v3.tile.bz2'],
									stderr=subprocess.STDOUT)
			tileFilename = tmpdirname + '/n47e016_elevation_v3.tile'

			tile = Tile(tileFilename)
			assert tile.validateChecksum() is True

	def test_copy(self, caplog):
		caplog.set_level(logging.DEBUG)
		logging.getLogger("Tile").setLevel(logging.DEBUG)

		with tempfile.TemporaryDirectory() as tmpdirname:
			shutil.copy('tests/fixtures/n47e016_elevation_v3.tile.bz2', tmpdirname)
			subprocess.check_output(["bzip2", "-d", tmpdirname + '/n47e016_elevation_v3.tile.bz2'],
									stderr=subprocess.STDOUT)
			tileFilename = tmpdirname + '/n47e016_elevation_v3.tile'

			sourceTile = Tile(tileFilename)
			targetTile = Tile(tile=sourceTile)

			# sourceTile and targetTile must be identical now
			assert sourceTile.header.version == targetTile.header.version
			assert sourceTile.header.xsize == targetTile.header.xsize
			assert sourceTile.header.ysize == targetTile.header.ysize
			assert sourceTile.header.zsize == targetTile.header.zsize
			for x in range(0, sourceTile.header.xsize):
				for y in range(0, sourceTile.header.ysize):
					for z in range(0, sourceTile.header.zsize):
						assert sourceTile.getNode(x, y, z) == targetTile.getNode(x, y, z)