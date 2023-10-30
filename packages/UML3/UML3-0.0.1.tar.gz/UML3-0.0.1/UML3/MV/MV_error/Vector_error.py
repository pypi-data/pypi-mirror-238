from .msgs import *


class VectorError(Exception):        
    """### `VectorError` Class
    - **Base Vector Exception:** The `VectorError` class is the base exception class for all exceptions related to vectors. It serves as the foundation for specific vector-related exceptions.
    """
    pass

class VectorLengthMismatchError(VectorError):
    """Exception raised when vector lengths do not match.

    This exception is raised when attempting to perform operations on vectors with different lengths.

    Args:
        VectorError: The base class for vector-related exceptions.
    """
    def __init__(self):
        super().__init__(LENGTHMISMATCHERR_MSG)

class VectorDimensionMismatchError(VectorError):
    """Exception raised when vector dimensions do not match.

    This exception is raised when attempting to perform operations on vectors with different dimensions.

    Args:
        VectorError: The base class for vector-related exceptions.
        expected_dimension (int): The expected dimension of the vector.
        actual_dimension (int): The actual dimension of the vector.
    """
    def __init__(self, expected_dimension, actual_dimension):
        super().__init__(DIMMISMATCHERR_MSG.format(
            expected_dimension = expected_dimension,
            actual_dimension = actual_dimension
        ))

class VectorOutOfRangeError(VectorError):
    """Exception raised when attempting to access an index out of range.

    This exception is raised when trying to access an index that is out of the valid range of the vector.

    Args:
        VectorError: The base class for vector-related exceptions.
        index (int): The index that is out of range.
        length (int): The length of the vector.
    """
    def __init__(self, index, length):
        super().__init__(OUTOFRANGEERR_MSG.format(
            index = index,
            out_length = length-1
        ))