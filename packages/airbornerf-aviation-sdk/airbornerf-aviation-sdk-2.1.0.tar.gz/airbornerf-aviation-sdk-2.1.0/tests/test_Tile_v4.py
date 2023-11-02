import logging
import math
import random
import shutil
import subprocess
import tempfile

from _pytest.python_api import approx

from arf.Tile import Tile


class TestClass(object):

	def test_tile(self, caplog):
		caplog.set_level(logging.DEBUG)

		with tempfile.TemporaryDirectory() as tmpdirname:
			shutil.copy('tests/fixtures/n47e016_elevation_v4.tile.bz2', tmpdirname)
			subprocess.check_output(["bzip2", "-d", tmpdirname + '/n47e016_elevation_v4.tile.bz2'],
			                        stderr=subprocess.STDOUT)
			tileFilename = tmpdirname + '/n47e016_elevation_v4.tile'

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
			shutil.copy('tests/fixtures/n47e016_elevation_v4.tile.bz2', tmpdirname)
			subprocess.check_output(["bzip2", "-d", tmpdirname + '/n47e016_elevation_v4.tile.bz2'],
									stderr=subprocess.STDOUT)
			tileFilename = tmpdirname + '/n47e016_elevation_v4.tile'

			tile = Tile(tileFilename)
			assert tile.validateChecksum() is True

	def test_create_tile(self, caplog):

		caplog.set_level(logging.DEBUG)
		logging.getLogger("Tile").setLevel(logging.DEBUG)

		for density in [4, 16]:
			with tempfile.TemporaryDirectory() as tmpdirname:

				if density == 16:
					valueOffset = -500
				elif density == 4:
					valueOffset = -3

				tile = Tile(latitude=48, longitude=16, xsize=1800, ysize=1800, zsize=2, altitude=0, verticalResolution=1,
							density=density, valueOffset=valueOffset)

				# Create internal array of ints holding reference values
				values = [None] * 1800 * 1800 * 2
				for i in range(0, 1800 * 1800 * 2):
					values[i] = random.randint(valueOffset + 1, 2**density + valueOffset - 1)
					# Mix in 5% Nones
					if random.random() <= 0.05:
						values[i] = None

				# Put the values into the tile
				for x in range(0, 1800):
					for y in range(0, 1800):
						for z in range(0, 2):
							tile.putNode(values[z*1800*1800+y*1800+x], x, y, z)

				# Check if the values we read from the tile are still the same
				for x in range(0, 1800):
					for y in range(0, 1800):
						for z in range(0, 2):
							assert tile.getNode(x, y, z) == values[z*1800*1800+y*1800+x]

				# Write the tile to a temporary file and close it
				tile_filename = f'{tmpdirname}/the.tile'
				tile.writeToFile(tile_filename)

				# Open the tile afresh
				tile2 = Tile(tile_filename)
				assert tile2.header.xsize == 1800
				assert tile2.header.ysize == 1800
				assert tile2.header.zsize == 2
				assert tile2.header.verticalResolution == 1
				assert math.isclose(tile2.header.latitude, 47.9994, abs_tol=0.001)
				assert tile2.header.longitude == 16
				assert tile2.header.altitude == 0
				assert tile2.header.latSize == approx(0.1)
				assert tile2.header.lonSize == approx(0.1)
				assert tile2.header.density == density
				assert tile2.header.valueOffset == valueOffset
				assert tile2.header.ceiling == 0
				assert tile2.validateChecksum()

				# Check if the values we read from the tile are still the same
				for x in range(0, 1800):
					for y in range(0, 1800):
						for z in range(0, 2):
							assert tile2.getNode(x, y, z) == values[z*1800*1800+y*1800+x]

	def test_copy(self, caplog):
		caplog.set_level(logging.DEBUG)
		logging.getLogger("Tile").setLevel(logging.DEBUG)

		with tempfile.TemporaryDirectory() as tmpdirname:
			shutil.copy('tests/fixtures/n47e016_elevation_v4.tile.bz2', tmpdirname)
			subprocess.check_output(["bzip2", "-d", tmpdirname + '/n47e016_elevation_v4.tile.bz2'],
									stderr=subprocess.STDOUT)
			tileFilename = tmpdirname + '/n47e016_elevation_v4.tile'

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
