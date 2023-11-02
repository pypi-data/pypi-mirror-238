import enum

class TileConstants:
    class DTypes(enum.Enum):
        UNDEFINED = 0
        UINT1 = 1
        UINT4 = 4
        UINT8 = 8
        UINT16 = 16
        BFLOAT16 = 68

    # Returns the number of bits of the nodes datatype (old name: density)
    @staticmethod
    def get_bitwidth(dtype: DTypes) -> int:

        if dtype == TileConstants.DTypes.UINT1:
            return 1
        elif dtype == TileConstants.DTypes.UINT4:
            return 4
        elif dtype == TileConstants.DTypes.UINT8:
            return 8
        elif dtype == TileConstants.DTypes.UINT16:
            return 16
        elif dtype == TileConstants.DTypes.BFLOAT16:
            return 16
        elif dtype == TileConstants.DTypes.UNDEFINED:
            raise RuntimeError("not yet implemented")