from .msgs import *


class VectorError(Exception):        
    pass

class VectorLengthMismatchError(VectorError):
    def __init__(self):
        super().__init__(LENGTHMISMATCHERR_MSG)

class VectorDimensionMismatchError(VectorError):
    def __init__(self, expected_dimension, actual_dimension):
        super().__init__(DIMMISMATCHERR_MSG.format(
            expected_dimension = expected_dimension,
            actual_dimension = actual_dimension
        ))

class VectorOutOfRangeError(VectorError):
    def __init__(self, index, length):
        super().__init__(OUTOFRANGEERR_MSG.format(
            index = index,
            out_length = length-1
        ))