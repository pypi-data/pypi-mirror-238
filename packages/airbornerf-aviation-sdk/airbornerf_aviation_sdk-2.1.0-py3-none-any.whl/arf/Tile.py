import math
from collections import namedtuple
from struct import pack, unpack
import logging
import mmap
import numpy as np
import time
import copy
from math import floor
import hashlib


class Tile:
	logger = logging.getLogger("Tile")

	TileHeader = namedtuple('TileHeader',
							'magic version xsize ysize zsize altitude verticalResolution latitude longitude latSize lonSize '
							'density valueOffset creationTime ceiling checksum statistics dtype padding')
	ElevationTileStatisticsHeader = namedtuple('ElevationTileStatisticsHeader',
											   'type version minElevation maxElevation meanElevation stddevElevation')

	class CalculatedTileHeader:
		horizontalLayerSize : int = 0
		tileBufferLength :int = 0

	header = None
	headerOffset = None
	calculatedHeader = None
	fp = None
	mm = None
	density = None

	def __init__(self, tileFilename: str=None, longitude: float=None, latitude: float=None,
				 xsize: int = None, ysize: int=None, zsize: int=None, altitude:int=None,
				 verticalResolution:int=None, density:int=None, valueOffset:int=0,
				 tile=None, latSize:float=0.1, lonSize:float=0.1):

		if tileFilename is not None:
			self.fp = open(tileFilename, 'rb')
			self.mm = mmap.mmap(self.fp.fileno(), 0, access=mmap.ACCESS_READ)

			# Read the header
			self.headerOffset = 582
			self.header = self.TileHeader._make(unpack('<8sbIIIhHffffbhIH20s256sb255s', self.mm[0:582]))
			if self.header.magic != b'DMTRTILE':
				raise RuntimeError("File is not a Dimetor tile!")
			if self.header.version > 4:
				# IMPORTANT: NOTE: If you raise the Tile version number, also check and change it in
				# the "cell-importer" project where a shortcut is used for performance reasons! Search
				# for "tile.header.version" there, and you'll find it. It should be a simple fix, but must not
				# be forgotten. A few PD importers use that important shortcut.
				raise RuntimeError("Unsupported Dimetor tile version: {}!".format(self.header.version))

			if self.header.version < 3:
				# Tile files version < 3 didn't have those header fields.
				self.headerOffset -= 256 + 256   # statistics and padding (as of version 3)

			if self.header.version == 1:
				# Density correction: see Tile.hpp in the C++ version
				if self.header.density == 8:
					self.density = 1
				elif self.header.density == 2:
					self.density = 4
				elif self.header.density == 1:
					self.density = 8
			else:
				self.density = self.header.density

			if self.density != 1 and self.density != 4 and self.density != 8 and self.density != 16:
				raise RuntimeError(f'Density {self.density} is not supported - only node densities of 1, 4, 8 or 16 are currently supported!')

			self._calculateHelpers()

			if self.header.version >= 3:
				if self.header.statistics[0] == 0:
					self.logger.debug("No statistics header")
				else:
					if self.header.statistics[0] == 1:
						self.logger.debug("Elevation tile statistics:")
						statistics = self.getElevationTileStatisticsHeader()
						self.logger.debug(f"   minElevation = {statistics.minElevation}")
						self.logger.debug(f"   maxElevation = {statistics.maxElevation}")
						self.logger.debug(f"   meanElevation = {statistics.meanElevation}")
						self.logger.debug(f"   stddevElevation = {statistics.stddevElevation}")
					else:
						self.logger.error(f"Unsupported statistics header type {self.header.statistics[0]}")

		elif tile is not None:
			# Construct a Tile from another tile (= 1:1 cloning)
			self.headerOffset = tile.headerOffset
			self.density = tile.density
			self.header = copy.deepcopy(tile.header)
			self._calculateHelpers()
			self.mm = bytearray(tile.mm[:])
			self.writeHeaderToBuffer()
		else:
			# create a new Tile in memory.
			self.headerOffset = 582
			header = {
				'magic': b'DMTRTILE',
				'version': 4,
				'xsize': xsize,
				'ysize': ysize,
				'latSize': latSize,
				'lonSize': lonSize,
				'verticalResolution': verticalResolution,
				'altitude': altitude,
				'zsize': zsize,
				'latitude': latitude,
				'longitude': longitude,
				'density': density,
				'valueOffset': valueOffset,
				'creationTime': int(time.time()),
				'checksum': bytearray(20),
				'ceiling': 0,
				'statistics': bytearray(256),
				'dtype': 0,
				'padding': bytearray(255)
			}
			self.header = self.TileHeader(**header)
			self.density = self.header.density

			if self.density != 1 and self.density != 4 and self.density != 8 and self.density != 16:
				raise RuntimeError("Only node densities of 1, 4, 8 or 16 are currently supported!")

			self._calculateHelpers()

			# create the buffer
			self.mm = bytearray(self.calculatedHeader.tileBufferLength)
			self.writeHeaderToBuffer()

		self.logger.debug("magic = {}".format(self.header.magic))
		self.logger.debug("version = {}".format(self.header.version))
		self.logger.debug("xsize = {}".format(self.header.xsize))
		self.logger.debug("ysize = {}".format(self.header.ysize))
		self.logger.debug("zsize = {}".format(self.header.zsize))
		self.logger.debug("altitude = {}".format(self.header.altitude))
		self.logger.debug("verticalResolution = {}".format(self.header.verticalResolution))
		self.logger.debug("latitude = {}".format(self.header.latitude))
		self.logger.debug("longitude = {}".format(self.header.longitude))
		self.logger.debug("latSize = {}".format(self.header.latSize))
		self.logger.debug("lonSize = {}".format(self.header.lonSize))
		self.logger.debug("density = {}".format(self.header.density))
		self.logger.debug("valueOffset = {}".format(self.header.valueOffset))
		self.logger.debug("creationTime = {}".format(self.header.creationTime))
		self.logger.debug("ceiling = {}".format(self.header.ceiling))
		self.logger.debug("checksum = {}".format(self.header.checksum))

	@staticmethod
	def calculate_n_bytes(nodes: int, node_density:int) -> int:
		"""
		Computes the number of bytes that are needed to store the data for the node values.
		We define node density as log2(n_bytes_node),
		where n_bytes_node is the number of bytes that are needed to store the data for one node.

		:param nodes: The number of nodes.
		:param node_density: The node density.
		:return: Number of bytes that are needed to store the data for the nodes.
		"""
		if node_density > 0:
			return nodes * (1 << node_density)
		elif node_density < 0:
			n_bytes = nodes // (1 << -node_density)
			r = nodes % (1 << -node_density)
			return n_bytes if r == 0 else n_bytes + 1
		else:
			return nodes


	def _calculateHelpers(self):
		self.calculatedHeader = self.CalculatedTileHeader()
		self.calculatedHeader.horizontalLayerSize = self.header.xsize * self.header.ysize
		numberOfGridNodes = self.calculatedHeader.horizontalLayerSize * self.header.zsize

		if self.density == 1:
			node_density = -3
		elif self.density == 4:
			node_density = -1
		elif self.density == 8:
			node_density = 0
		elif self.density == 16:
			node_density = 1

		nodeDataBytes = Tile.calculate_n_bytes( numberOfGridNodes, node_density )
		self.calculatedHeader.tileBufferLength = nodeDataBytes + self.headerOffset

		self.logger.debug(self.calculatedHeader.horizontalLayerSize)
		self.logger.debug(self.calculatedHeader.tileBufferLength)

	def writeHeaderToBuffer(self):
		self.mm[0:self.headerOffset] = pack('<8sbIIIhHffffbhIH20s256sb255s', *self.header)

	@staticmethod
	def roundHalfUp(x):
		floorX = floor(x)
		if x - floorX >= 0.5:
			return floorX + 1
		return floorX

	def findCoordinates(self, lat: float, lon: float) -> (int, int, int):
		"""
		Find the z layer where the node value at the given coordinate is 0 for the first time.
		:param lat:
		:param lon:
		:return:
		"""
		x = self.roundHalfUp((lon - self.header.longitude) / self.header.lonSize * self.header.xsize)
		y = self.roundHalfUp((self.header.latitude - lat) / self.header.latSize * self.header.ysize)

		for z in range(0, self.header.zsize):
			if self.getNode(x, y, z) == 0:
				return x, y, z

		return -1, -1, -1

	@staticmethod
	def clamp(value, min_value, max_value):
		return min(max(min_value, value), max_value)

	@staticmethod
	def getTileCoordinatesWithHeader(header, lat: float, lon: float, altitude: float, clip_coo = True) -> (int, int, int):
		"""
		Convert WGS 84 coordinates to tile coordinates
		:param lat:
		:param lon:
		:param altitude:
		:param clip_coo: If true, coordinates are clipped to valid range ( s.t. (x,y,z) corresponds to a point on the tile area).
		:return:
		"""
		x = Tile.roundHalfUp((lon - header.longitude) / header.lonSize * header.xsize)
		y = Tile.roundHalfUp((header.latitude - lat) / header.latSize * header.ysize)
		z = Tile.roundHalfUp((altitude - header.altitude) / header.verticalResolution)

		if clip_coo:
			x = Tile.clamp(x, 0, header.xsize - 1)
			y = Tile.clamp(y, 0, header.ysize - 1)
			z = Tile.clamp(z, 0, header.zsize - 1)

		return x, y, z

	def getTileCoordinates(self, lat: float, lon: float, altitude: float, clip_coo = True) -> (int, int, int):
		return Tile.getTileCoordinatesWithHeader(self.header, lat, lon, altitude, clip_coo)

	@staticmethod
	def getFractionalCoordinatesWithHeader(header, lat: float, lon: float, clip_coo= True) -> (float, float):
		"""
		Convert WGS 84 coordinates to fractional tile coordinates
		:param lat:
		:param lon:
		:return:
		"""
		x = (lon - header.longitude) / header.lonSize * header.xsize
		y = (header.latitude - lat) / header.latSize * header.ysize

		if clip_coo:
			x = Tile.clamp(x, 0, header.xsize - 1)
			y = Tile.clamp(y, 0, header.ysize - 1)

		return x, y

	def getLatLong(self, x: float, y: float) -> (float, float):
		"""
		Convert tile coordinates to WGS 84 coordinates
		:param x:
		:param y:
		:return:
		"""

		lon = self.header.longitude + x / self.header.xsize * self.header.lonSize
		lat = self.header.latitude - y / self.header.ysize * self.header.latSize
		return lon, lat

	def getLatLongAlt(self, x: int, y: int, z: int) -> (float, float, float):
		"""
		Convert tile coordinates to WGS 84 coordinates
		:param x:
		:param y:
		:param z:
		:return:
		"""
		lon = x / self.header.xsize * self.header.lonSize + self.header.longitude
		lat = self.header.latitude - y / self.header.ysize * self.header.latSize
		altitude = z * self.header.verticalResolution + self.header.altitude
		return lon, lat, altitude

	def getNode(self, x: int, y: int, z: int):

		if x >= self.header.xsize or y >= self.header.ysize or z >= self.header.zsize or x < 0 or y < 0 or z < 0:
			return None

		node_index = self._getNodeIndex(x, y, z)

		if self.density == 1:
			byte_index = int(node_index / 8)
			bit_index = node_index % 8
			byte_index += self.headerOffset
			return (self.mm[byte_index] & (1 << bit_index)) >> bit_index
		elif self.density == 4:
			byte_index = int(node_index / 2)
			nibble_index = node_index % 2
			byte_index += self.headerOffset
			bufVal = (self.mm[byte_index] & (0xF0 >> (nibble_index * 4))) >> ((1 - nibble_index) * 4)
			if bufVal == 0:
				return None
			else:
				return bufVal + self.header.valueOffset
		elif self.density == 8:
			byte_index = node_index + self.headerOffset
			bufVal = self.mm[ byte_index ]
			if bufVal == 0:
				return None
			else:
				return bufVal + self.header.valueOffset
		elif self.density == 16:
			byte_index = node_index * 2 + self.headerOffset
			bufVal = ( ( self.mm[ byte_index ] << 8 ) | (self.mm[ byte_index + 1 ] ) ) & 0xFFFF
			if bufVal == 0:
				return None
			else:
				return bufVal + self.header.valueOffset
		else:
			raise RuntimeError("Unsupported density")

	def putNode(self, value: int, x: int, y: int, z: int):
		"""
		Put the value at the specified location into the tile map.
		Pass None to indicate no value
		:param value:
		:param x:
		:param y:
		:param z:
		:return:
		"""
		if x >= self.header.xsize or y >= self.header.ysize or z >= self.header.zsize:
			return
		if x < 0 or y < 0 or z < 0:
			return

		node_index = self._getNodeIndex(x, y, z)

		if self.header.density == 1:
			byte_index = int(node_index / 8)
			bit_index = node_index % 8
			byte_index += self.headerOffset

			# Note: this is not thread safe! Would need atomic ANDs and ORs.
			if value != 0:
				bitmask = 1 << bit_index
				self.mm[byte_index] = self.mm[byte_index] | bitmask
			else:
				bitmask = ~(1 << bit_index)
				self.mm[byte_index] = self.mm[byte_index] & bitmask
		elif self.header.density == 4:
			# Note: this is not thread safe! Would need atomic ANDs and ORs.
			byte_index = int(node_index / 2)
			nibble_index = node_index % 2
			byte_index += self.headerOffset
			theValue = 0
			if value is not None:
				val = value - self.header.valueOffset
				theValue = max(min(16, val), 1)
			self.mm[byte_index] &= 0x0F << (nibble_index * 4)
			self.mm[byte_index] |= (theValue & 0x0F) << ((1-nibble_index) * 4)
		elif self.header.density == 16:
			byte_index = node_index * 2 + self.headerOffset
			theValue = 0
			if value is not None:
				val = value - self.header.valueOffset
				theValue = max(min(65535, val), 1)
			self.mm[byte_index] = (theValue >> 8) & 0xFF
			self.mm[byte_index + 1] = theValue & 0xFF
		else:
			raise RuntimeError(f'Unsupported density of {self.density}.')

	def getZElevation(self, x: int, y: int):
		"""
		Calculates the Z elevation at the given point.
		:param x:
		:param y:
		:return:
		"""
		for z in range(0, self.header.zsize):
			if self.getNode(x, y, z) == 0:
				return z

	def getElevation(self, x: int, y: int):
		"""
		Returns elevation at the given point.
		:param x:
		:param y:
		:return:
		"""
		return self.getZElevation(x, y) * self.header.verticalResolution + self.header.altitude

	def __del__(self):

		if type(self.mm) is mmap.mmap:
			self.mm.close()
		if self.fp is not None:
			self.fp.close()

	# TODO: check if getLayerZ is needed
	def getLayerZ(self, z: int):
		"""
		Extract layer points and return as 2D array.
		:param z:
		:return:
		"""
		points = []
		for x in range(0, self.header.xsize):
			column = []
			for y in range(0, self.header.ysize):
				column.append(self.getNode(x, y, z))
			points.append(column)
		return points
	def _getNodeIndex(self, x:int, y:int, z:int):
		return z * self.calculatedHeader.horizontalLayerSize + y * self.header.xsize + x

	def getTileLayers(self, returnAsList, return2D, *layers):
		"""
        Extract all point values of a layer and return a list of 1D/2D arrays OR a 3D array.
		:return:
		"""

		if self.density != 1:
			raise RuntimeError("Unsupported density")

		bitData = np.unpackbits(self.mm)
		bitData = bitData[self.headerOffset * 8:]

		# unpackbits unpacks the bits in an opposite order so they need to be flipped below.
		bitDataByteOrder = bitData.reshape((len(bitData) // 8, 8))
		bitDataByteOrder = np.flip(bitDataByteOrder, axis=1)
		bitData = bitDataByteOrder.flatten()

		if not layers:
			layers = range(self.header.zsize)

		extractedLayers = []

		for z in layers:
			# Layer extracted as 1D array
			layer = bitData[z * self.header.xsize * self.header.ysize:(z + 1) * self.header.xsize * self.header.ysize]
			if return2D:
				extractedLayers.append(layer.reshape(self.header.xsize, self.header.ysize))
			else:
				extractedLayers.append(layer)

		if returnAsList:
			return extractedLayers
		else:
			return np.asarray(extractedLayers)

	# TODO: check if getNodeLayerZ is needed
	def getNodeLayerZ(self, value: int, z: int):
		"""
		Extract all the points in a layer with a specific value (ex. 0 or 1)
		:param value:
		:param z:
		:return:
		"""
		points = []
		for x in range(0, self.header.xsize):
			for y in range(0, self.header.ysize):
				if self.getNode(x, y, z) == value:
					points.append([x, y])
		npArray = np.asarray(points)
		return npArray

	# TODO: check if getNodeLayerZset is needed
	def getNodeLayerZset(self, value: int, z: int):
		""""
		Extract all the points in a layer with a specific value (ex. 0 or 1) but return set.
		:param value:
		:param z:
		:return:
		"""
		pSet = set()
		for x in range(0, self.header.xsize):
			for y in range(0, self.header.ysize):
				if self.getNode(x, y, z) == value:
					pSet.add((x, y))
		return pSet

	def getLayerHeight(self, z: int):
		"""
		Get the height of a layer passing the z layer index.
		:param z:
		:return:
		"""
		return self.header.altitude + z * self.header.verticalResolution

	def getLayerFloorAndCeiling(self, z: int) -> (float, float):
		"""
		Get the bottom and top of a layer passing the z layer index.
		:param z:
		:return:
		"""
		height = self.getLayerHeight(z)

		floor = height - 0.5 * self.header.verticalResolution
		ceiling = height + 0.5 * self.header.verticalResolution

		return floor, ceiling

	@staticmethod
	def normalizeCoordinates(latitude: float, longitude: float) -> (float, float):
		"""
		Fix up input lat/lon to be within [-90,90] and [-180,180) respectively.
		This avoids problems if out of range coordinates are given anywhere (e.g. as user input).

		Longitude wraps around at 180 to -180. The reason for choosing this range
		(instead of (-180,180]) is that the tilespec represents the SW corner, so
		the tile comprises points "to the right" of its name - this way they have
		the same sign.

		Latitudes >90 and <-90 are treated as being mirrored at +-90, with the longitude
		being "reversed" in this case - as if one walked straight over
		the North or South Pole.

		:param latitude:
		:param longitude:
		:return: tupple (latitude, longitude) with the normalized coordinates.
		"""
		if latitude >= 180 or latitude < -180:
			latitude = (math.fmod((math.fmod(latitude + 180.0, 360.0) + 360.0), 360.0) - 180.0)

		if latitude >= 90:
			latitude = 180 - latitude
			longitude += 180
		elif latitude < -90:
			latitude = -180 - latitude
			longitude += 180

		if longitude >= 180 or longitude < -180:
			longitude = (math.fmod((math.fmod(longitude + 180, 360) + 360), 360) - 180)

		return latitude, longitude

	@staticmethod
	def generateTilespec(latitude: float, longitude: float) -> str:
		"""
		Generate the tilespec for the tile that contains the location at lat, lon
		:param lat:
		:param lon:
		:return:
		"""

		latitude, longitude = Tile.normalizeCoordinates(latitude, longitude)

		assert -90 <= latitude <= 90, "Latitude out of bounds"
		assert -180 <= longitude <= 180, "Longitude out of bounds"

		tilespec = [''] * 9

		tilespec[0] = 'n' if latitude >= 0 else 's'
		tilespec[4] = 'e' if longitude >= 0 else 'w'

		lat_deci_deg = int(abs(floor(latitude * 10)))
		q = lat_deci_deg // 100
		r = lat_deci_deg % 100

		tilespec[1] = chr(q + ord('0'))
		q = r // 10
		r = r % 10
		tilespec[2] = chr(q + ord('0'))
		tilespec[3] = chr(r + ord('0'))

		lon_deci_deg = int(abs(floor(longitude * 10)))
		q = lon_deci_deg // 1000
		r = lon_deci_deg % 1000

		tilespec[5] = chr(q + ord('0'))

		q = r // 100
		r = r % 100

		tilespec[6] = chr(q + ord('0'))

		q = r // 10
		r = r % 10

		tilespec[7] = chr(q + ord('0'))
		tilespec[8] = chr(r + ord('0'))

		return ''.join(tilespec)

	@staticmethod
	def getCoordinatesForTilespec(tilespec: str) -> (float, float):
		latitude = int(tilespec[1]) * 10 + int(tilespec[2]) + int(tilespec[3]) * 0.1

		if tilespec[0] == 's' or tilespec[0] == 'S':
			latitude *= -1

		longitude = int(tilespec[5]) * 100 + int(tilespec[6]) * 10 + int(tilespec[7]) + int(tilespec[8]) * 0.1

		if tilespec[4] == 'w' or tilespec[4] == 'W':
			longitude *= -1

		return latitude, longitude

	def getElevationTileStatisticsHeader(self):
		"""
		Return the elevation tile statistics header. Valid only for version >= 3 elevation tiles.
		If the file is not a version >=3 elevation tile or it has no statistics header, returns None.
		:return:
		"""
		if self.header.version < 3:
			return None
		if self.header.statistics[0] == 0:
			return None
		return self.ElevationTileStatisticsHeader._make(unpack('<bbhhff', self.mm[70:84]))

	def setElevationTileStatisticsHeader(self, statistics: ElevationTileStatisticsHeader):
		self.mm[70:84] = pack('<bbhhff', *statistics)
		self.header.statistics[0:14] = pack('<bbhhff', *statistics)

	def validateChecksum(self):
		"""
		Checks if the checksum stored in the "checksum" header is correct for this tile.
		:return:
		"""
		sha1 = hashlib.sha1()

		# Update from the start of the buffer to the checksum:
		sha1.update(self.mm[0:50])

		# Next, add a fake checksum field with all zeros
		sha1.update(b'\x00' * 20)

		# Finally, add everything from after the checksum to the end of file
		sha1.update(self.mm[70:])

		return sha1.digest() == self.header.checksum

	def createChecksum(self):
		sha1 = hashlib.sha1()

		# Update from the start of the buffer to the checksum:
		sha1.update(self.mm[0:50])

		# Next, add a fake checksum field with all zeros
		sha1.update(b'\x00' * 20)

		# Finally, add everything from after the checksum to the end of file
		sha1.update(self.mm[70:])

		self.mm[50:70] = sha1.digest()
		self.header.checksum[0:20] = sha1.digest()
		# self.writeHeaderToBuffer()

	def writeToFile(self, filename):
		self.createChecksum()
		with open(filename, 'wb') as fp:
			fp.write(self.mm)
