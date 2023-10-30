import pickle
import random
from typing import Iterable
from .MV_error import VectorDimensionMismatchError, VectorLengthMismatchError, VectorOutOfRangeError, VectorError
from math import sqrt, sin, cos, radians, acos, degrees, atan2, acos, pi
import matplotlib.pyplot as plt


class Vector():
    """
    ## `Vector` Class

    The `Vector` class is a versatile Python library for working with vectors in both 2D and 3D spaces. It provides a wide range of functionalities to create, manipulate, and visualize vectors. This class is designed for users who need to perform vector-based operations in mathematical and engineering applications.

    ### Features

    - **`2D and 3D Support`:** The `Vector` class supports both 2D and 3D vectors, allowing you to work in multiple dimensions.

    - **`Comprehensive Vector Operations`:** Perform a variety of vector operations, such as addition, subtraction, scalar multiplication, dot products, cross products, normalization, and more.

    - **`Sorting:`** Sort the elements of a vector in ascending order using the `sort` method.

    - **`Random Vector Generation`:** Generate random vectors with specified properties using the `randvec` function.

    - **`Zero Vectors`:** Create vectors filled with zeros using the `zeros` function.

    - **`Scalar Repetition`:** Generate vectors with a specified scalar value repeated a number of times using the `nvec` function.

    - **`Unit Conversion`:** Convert angles between degrees and radians with the `degrees_to_radians` and `radians_to_degrees` functions.

    - **`2D and 3D Visualization`:** Visualize vectors in 2D and 3D spaces using the `draw2d` and `draw3d` functions, with optional color customization.

    - **`Custom Exceptions`:** The class includes custom exceptions to handle vector-related errors, making error handling straightforward.

    - **`Coordinate System Transformation`:** Easily change the coordinate system for a vector to adapt to different applications and reference frames.

    - ** `And others`: ** 
    
    ```css
    for more info check class methods docs :)
    ```
    ### `Usage`

    The `Vector` class provides an intuitive and Pythonic interface for working with vectors. It simplifies vector manipulation and calculations in various applications, including physics, computer graphics, and engineering.

    Here's a quick example of creating and adding two 3D vectors using the `Vector` class:

    ```python
    from UML3 import Vector

    # Create two 3D vectors
    vec1 = Vector([1, 2, 3])
    vec2 = Vector([4, 5, 6])

    # Add the vectors
    result = vec1 + vec2

    print(result)  # Output: Vector([5.0, 7.0, 9.0])
    ```
    For more detailed usage examples, method descriptions, and error handling, please refer to the documentation.

    ## `Custom Exceptions`
    The Vector class includes custom exceptions to help you handle errors gracefully when working with vectors. These exceptions provide clear and informative error messages, making it easier to identify and resolve issues in your vector-based code.

    - **`VectorLengthMismatchError`: Raised when vector lengths do not match.
    - **`VectorDimensionMismatchError`: Raised when vector dimensions do not match.
    - **`VectorOutOfRangeError`: Raised when attempting to access an index out of range.
    Please refer to the Custom Exceptions section for more details on these exceptions and how to use them in your code.

    ## `Requirements`
    The Vector class is designed for use in Python 3.12+ environments | 
    ```css 
    IN <3.12 may be bugs :)
    ``` .

    Installation
    You can install the Vector library using pip:

    ```css
    pip install UML3
    ```
    ## `Documentation`
    For detailed information on how to use the Vector class and its methods, please consult the official documentation for UML3.
    """
    def __init__(self, data:list[int|float]) -> None: 
        """
        Initialize a Vector with the given data.

        Args:
            data (list[int | float]): A list of integer or float values to initialize the vector.
        """
        self.vector = data

    def __setitem__(self, key, value:int | float):
        """
        Set the value at the specified index in the vector.

        Args:
            key (int): The index at which to set the value.
            value (int | float): The value to set.

        Raises:
            VectorOutOfRangeError: If the index is out of range.
        """
        try:
            self.vector[key] = value
        except:
            raise VectorOutOfRangeError(key,len(self))
    
    def __getitem__(self, key):
        """
        Get the value at the specified index in the vector.

        Args:
            key (int): The index to access.

        Raises:
            VectorOutOfRangeError: If the index is out of range.

        Returns:
            int | float: The value at the specified index.
        """
        try:
            return self.vector[key]
        except:
            raise VectorOutOfRangeError(key,len(self))
    
    def __iter__(self):
        """
        Iterate over the elements of the vector.

        Returns:
            Iterator[int | float]: An iterator over the elements of the vector.
        """
        return iter(self.vector)
    
    def __len__(self):
        """
        Get the length of the vector.

        Returns:
            int: The number of elements in the vector.
        """
        return len(self.vector)
    
    def __str__(self, mode = 'default'):
        """
        Get a string representation of the vector.

        Args:
            mode (str, optional): The mode for string representation. Defaults to 'default'.

        Returns:
            str: A string representation of the vector.
        """
        if mode == 'default':
            if not self.vector:
                    return "[\n]"
            if len(self) <= 10:
                result = "[\n"
                for element in self.vector:
                    result += f" [{element}]\n"
                result += "]"
            else: 
                result = "[\n"
                for element in self.vector[:5]:
                    result += f" [{element}]\n"
                for element in self.vector[len(self)-5:]:
                    result += f" [{element}]\n"
                result += "]"
        else:
            if not self.vector:
                return "[\n]"
            result = "[\n"
            for element in self.vector:
                result += f" [{element}]\n"
            result += "]"
        return result
    
    def __sum__(self):
        """
        Calculate the sum of the vector's elements.

        Returns:
            int | float: The sum of the vector's elements.
        """
        return sum(self)
    
    def __min__(self):
        """
        Get the minimum value in the vector.

        Returns:
            int | float: The minimum value in the vector.
        """
        return min(self)
    
    def __max__(self):
        """
        Get the maximum value in the vector.

        Returns:
            int | float: The maximum value in the vector.
        """
        return max(self)
    
    def __eq__(self, other):
        """
        Check if two vectors are equal element-wise.

        Args:
            other (Vector): The other vector to compare.

        Returns:
            bool: True if the vectors are equal, False otherwise.
        """
        if len(self) != len(other):
            return False
        return all(self_el == other_el for self_el, other_el in zip(self, other))

    def __ne__(self, other):
        """
        Check if two vectors are not equal element-wise.

        Args:
            other (Vector): The other vector to compare.

        Returns:
            bool: True if the vectors are not equal, False otherwise.
        """
        return not self.__eq__(other)
    
    def __mul__(self, other: 'Vector | int | float') -> 'Vector':
        """
        Multiply the vector by another vector, an integer, or a float.

        Args:
            other (Vector | int | float): The vector, integer, or float to multiply with.

        Returns:
            Vector: The resulting vector.

        Raises:
            VectorLengthMismatchError: If the lengths of the vectors do not match.
        """
        if isinstance(other, Vector):
            if len(self) == len(other):
                return Vector([x*y for x,y in zip(self, other)])
            else:
                raise VectorLengthMismatchError()
        elif isinstance(other, (int,float)):
            return Vector([x*other for x in self])

    def __rmul__(self, other:int|float) -> 'Vector':
        """
        Multiply the vector by an integer or float.

        Args:
            other (int | float): The integer or float to multiply with.

        Returns:
            Vector: The resulting vector.
        """
        if isinstance(other, (int,float)):
            return Vector([x*other for x in self])

    def __add__(self, other:'Vector') -> 'Vector':
        """
        Add two vectors element-wise.

        Args:
            other (Vector): The other vector to add.

        Returns:
            Vector: The resulting vector.

        Raises:
            VectorLengthMismatchError: If the lengths of the vectors do not match.
        """
        if len(self) == len(other):
            return Vector([self_el + other_el for self_el, other_el in zip(self,other)])
        else:
            raise VectorLengthMismatchError()
        
    def __sub__(self, other:'Vector') -> 'Vector':
        """
        Subtract two vectors element-wise.

        Args:
            other (Vector): The other vector to subtract.

        Returns:
            Vector: The resulting vector.

        Raises:
            VectorLengthMismatchError: If the lengths of the vectors do not match.
        """
        if len(self) == len(other):
            return Vector([self_el - other_el for self_el, other_el in zip(self,other)])
        else:
            raise VectorLengthMismatchError()
        
    def __truediv__(self, other:int|float) -> 'Vector':
        """
        Divide the vector by an integer or float.

        Args:
            other (int | float): The integer or float to divide by.

        Returns:
            Vector: The resulting vector.

        Raises:
            ZeroDivisionError: If division by zero is attempted.
        """
        if other == 0:
            raise ZeroDivisionError("Division by zero is not allowed")
        if isinstance(other, (int,float)):
            return Vector([x/other for x in self])
        
    def __floordiv__(self, other:int|float) -> 'Vector':
        """
        Perform integer division on the vector by an integer or float.

        Args:
            other (int | float): The integer or float for division.

        Returns:
            Vector: The resulting vector.

        Raises:
            ZeroDivisionError: If division by zero is attempted.
        """
        if other == 0:
            raise ZeroDivisionError("Division by zero is not allowed")
        if isinstance(other, (int,float)):
            return Vector([x//other for x in self])
        
    def __mod__(self, other:int|float) -> 'Vector':
        """
        Calculate the modulo of the vector by an integer or float.

        Args:
            other (int | float): The integer or float for modulo operation.

        Returns:
            Vector: The resulting vector.

        Raises:
            ZeroDivisionError: If division by zero is attempted.
        """
        if other == 0:
            raise ZeroDivisionError("Division by zero is not allowed")
        if isinstance(other, (int,float)):
            return Vector([x%other for x in self])

    def extend(self, iterable:Iterable[int | float]):
        """
        Extend the vector with elements from an iterable.

        Args:
            iterable (Iterable[int | float]): The iterable to extend the vector with.

        """
        self.vector.extend(iterable)
    
    def append(self, item:int|float):
        """
        Append an element to the end of the vector.

        Args:
            item (int | float): The element to append.
        """
        self.vector.append(item)

    def clear(self):
        """
        Remove all elements from the vector.
        """

        self.vector.clear()

    def reverse(self):
        """
        Reverse the order of elements in the vector.
        """
        self.vector.reverse()

    def scalar(self, other: 'Vector')->float:
        """
        Calculate the scalar product of two vectors.

        Args:
            other (Vector): The other vector for the scalar product.

        Returns:
            float: The scalar product.

        Raises:
            VectorLengthMismatchError: If the lengths of the vectors do not match.

        """
        if isinstance(other, Vector):
            if len(self) == len(other):
                return sum(x*y for x,y in zip(self, other))
            else:
                raise VectorLengthMismatchError()
    
    def cross(self, other: 'Vector')->'Vector':
        """
        Calculate the cross product of two 3D vectors.

        Args:
            other (Vector): The other 3D vector for the cross product.

        Returns:
            Vector: The cross product vector.

        Raises:
            VectorLengthMismatchError: If the lengths of the vectors do not match.
            VectorDimensionMismatchError: If the vectors are not 3D.
        """
        if isinstance(other, Vector):
            if len(self) == 3:
                if len(self) == len(other):
                    return Vector([self[1]*other[2]-self[2]*other[1], self[2]*other[0]-self[0]*other[2], self[0]*other[1] - self[1]*other[0]])
                else:
                    raise VectorLengthMismatchError()
            else:
                raise VectorDimensionMismatchError(3,len(self))
            
    def norm(self) -> float | int:
        """
        Calculate the magnitude (norm) of the vector.

        Returns:
            float | int: The magnitude of the vector.
        """
        return sqrt(sum(x**2 for x in self))

    def nomralize(self) -> 'Vector':
        """
        Normalize the vector to have a magnitude of 1.

        Returns:
            Vector: The normalized vector.

        """
        norm_value = self.norm()
        if norm_value == 0:
            return zeros(len(self))
        else:
            return Vector([x / norm_value for x in self])

    def rotate_2d(self, angle_degrees:float) -> 'Vector':
        """
        Rotate the 2D vector by a specified angle in degrees.

        Args:
            angle_degrees (float): The angle in degrees for rotation.

        Raises:
            VectorDimensionMismatchError: If the vector is not 2D.

        Returns:
            Vector: The rotated 2D vector.
        """
        angle_radians = radians(angle_degrees)        
        if len(self) != 2:
            raise VectorDimensionMismatchError(2, len(self))
        x, y = self[0], self[1]
        new_x = x * cos(angle_radians) - y * sin(angle_radians)
        new_y = x * sin(angle_radians) + y * cos(angle_radians)
        return Vector([new_x, new_y])

    def rotate_3d(self, angle_degrees:float, axis:str='x'):
        """
        Rotate the 3D vector by a specified angle in degrees around a specified axis.

        Args:
            angle_degrees (float): The angle in degrees for rotation.
            axis (str, optional): The axis of rotation ('x', 'y', or 'z'). Defaults to 'x'.

        Raises:
            VectorDimensionMismatchError: If the vector is not 3D.
            SyntaxError: If an invalid axis is specified.

        Returns:
            Vector: The rotated 3D vector.
        """
        if len(self) != 3:
            raise VectorDimensionMismatchError(3, len(self))
        angle_radians = radians(angle_degrees)
        x, y, z = self[0], self[1], self[2]
        if axis == 'x':
            new_x = x
            new_y = y * cos(angle_radians) - z * sin(angle_radians)
            new_z = y * sin(angle_radians) + z * cos(angle_radians)
        elif axis == 'y':
            new_x = x * cos(angle_radians) + z * sin(angle_radians)
            new_y = y
            new_z = -x * sin(angle_radians) + z * cos(angle_radians)
        elif axis == 'z':
            new_x = x * cos(angle_radians) - y * sin(angle_radians)
            new_y = x * sin(angle_radians) + y * cos(angle_radians)
            new_z = z
        else:
            raise SyntaxError("Select valid axis from (x,y,z)")
        return Vector([new_x, new_y, new_z])
    
    def rotate_nd(self, angle_degrees:float, axis_indices:list[int]):
        """
        Rotate the vector in N dimensions by a specified angle in degrees around specified axes.

        Args:
            angle_degrees (float): The angle in degrees for rotation.
            axis_indices (list[int]): List of axis indices to rotate around.

        Returns:
            Vector: The rotated N-dimensional vector.
        """
        angle_radians = radians(angle_degrees)

        # Create a rotation matrix
        rotation_matrix = [[int(i == j) for i in range(len(self))] for j in range(len(self))]

        for axis_index in axis_indices:
            c = cos(angle_radians)
            s = sin(angle_radians)

            axis_vector = [int(i == axis_index) for i in range(len(self))]

            rotation_matrix[axis_index][axis_index] = c
            for i in range(len(self)):
                if i != axis_index:
                    rotation_matrix[axis_index][i] = -s * axis_vector[i]
                    rotation_matrix[i][axis_index] = s * axis_vector[i]

        # Multiply the rotation matrix by the vector
        rotated_vector = [0] * len(self)
        for i in range(len(self)):
            for j in range(len(self)):
                rotated_vector[i] += rotation_matrix[i][j] * self[j]

        return Vector(rotated_vector)

    def angle_between_vectors(self, other: 'Vector') -> float:
        """
        Calculate the angle in degrees between two vectors.

        Args:
            other (Vector): The other vector for angle calculation.

        Raises:
            TypeError: If the other vector is not of type Vector.
            VectorDimensionMismatchError: If the lengths of the vectors do not match.

        Returns:
            float: The angle between the vectors in degrees.
        """
        if not isinstance(other, Vector):
            raise TypeError('{other} must be Vector.')
        if len(self) != len(other):
            raise VectorDimensionMismatchError((len(self),len(self)), (len(self),len(other)))
        dot_product = sum(a * b for a, b in zip(self, other))
        magnitude1 = sqrt(sum(a**2 for a in self))
        magnitude2 = sqrt(sum(b**2 for b in other))
        if magnitude1 == 0 or magnitude2 == 0:
            return 0
        angle_radians = acos(dot_product / (magnitude1 * magnitude2))
        angle_degrees = degrees(angle_radians)
        return angle_degrees

    def vector_projection(self, other: 'Vector') -> 'Vector':
        """
        Calculate the vector projection of the vector onto another vector.

        Args:
            other (Vector): The other vector for projection.

        Raises:
            TypeError: If the other vector is not of type Vector.
            VectorDimensionMismatchError: If the lengths of the vectors do not match.

        Returns:
            Vector: The vector projection.
        """
        if not isinstance(other, Vector):
            raise TypeError('{other} must be Vector.')
        if len(self) != len(other):
            raise VectorDimensionMismatchError((len(self),len(self)), (len(self),len(other)))
        dot_product = self.scalar(other)
        onto_magnitude = sum(b**2 for b in other)
        if onto_magnitude == 0:
            return Vector([0] * len(vector))
        scale = dot_product / onto_magnitude
        projection = [scale * b for b in other]
        return Vector(projection)

    def to_polar(self) -> 'Vector':
        """
        Convert a 2D vector to polar coordinates (r, theta).

        Raises:
            VectorDimensionMismatchError: If the vector is not 2D.

        Returns:
            Vector: The polar coordinates.
        """
        if len(self) != 2:
            raise VectorDimensionMismatchError(2, len(self))
        x,y = self[0], self[1]
        r = sqrt(x**2+y**2)
        theta = degrees(atan2(y,x))
        return Vector([r, theta])

    def to_spherical(self) -> 'Vector':
        """
        Convert a 3D vector to spherical coordinates (r, theta, phi).

        Raises:
            VectorDimensionMismatchError: If the vector is not 3D.

        Returns:
            Vector: The spherical coordinates.
        """
        if len(self) != 3:
            raise VectorDimensionMismatchError(3, len(self))
        x, y, z = self[0], self[1], self[2]
        r = sqrt(x**2 + y**2 + z**2)
        theta = degrees(atan2(y, x))
        phi = degrees(acos(z / r))
        return Vector([r, theta, phi])
    
    def to_conical(self) -> 'Vector':
        """
        Convert a 3D vector to conical coordinates (r, theta, phi).

        Raises:
            VectorDimensionMismatchError: If the vector is not 3D.

        Returns:
            Vector: The conical coordinates.
        """
        if len(self) != 3:
            raise VectorDimensionMismatchError(3, len(self))
        x,y,z = self[0], self[1], self[2]
        r = sqrt(x**2 + y**2)
        theta = degrees(atan2(y, x))
        phi = degrees(atan2(sqrt(x**2 + y**2), z))
        return Vector([r, theta, phi])

    def are_orthogonal(self, other: 'Vector') -> bool:
        """
        Check if two vectors are orthogonal (perpendicular).

        Args:
            other (Vector): The other vector to check for orthogonality.

        Raises:
            TypeError: If the other vector is not of type Vector.
            VectorDimensionMismatchError: If the lengths of the vectors do not match.

        Returns:
            bool: True if the vectors are orthogonal, False otherwise.
        """
        if not isinstance(other, Vector):
            raise TypeError('{other} must be Vector.')
        if len(self) != len(other):
            raise VectorDimensionMismatchError((len(self),len(self)), (len(self),len(other)))
        return self.scalar(other) == 0
   
    def are_parallel(self, other) -> bool:
        """
        Check if two vectors are parallel.

        Args:
            other (Vector): The other vector to check for parallelism.

        Raises:
            TypeError: If the other vector is not of type Vector.
            VectorDimensionMismatchError: If the lengths of the vectors do not match.

        Returns:
            bool: True if the vectors are parallel, False otherwise.
        """
        if not isinstance(other, Vector):
                raise TypeError('{other} must be Vector.')
        if len(self) != len(other):
                raise VectorDimensionMismatchError((len(self),len(self)), (len(self),len(other)))
        for i in range(len(self)):
            if self[i] == 0:
                continue  
            if other[i] == 0:
                return False  
            if self[i] / other[i] != self[0] / other[0]:
                return False  
        return True

    def sum(self) -> float | int:
        """
        Calculate the sum of the vector's elements.

        Returns:
            int | float: The sum of the vector's elements.
        """

        return sum(self)
    
    def mean(self) -> float | int:
        """
        Calculate the mean of the vector's elements.

        Returns:
            int | float: The mean of the vector's elements.
        """
        return sum(self)/len(self)

    def min(self) -> float | int:
        """
        Get the minimum value in the vector.

        Returns:
            int | float: The minimum value in the vector.
        """

        return min(self)
    
    def max(self) -> float | int:
        """
        Get the maximum value in the vector.

        Returns:
            int | float: The maximum value in the vector.
        """
        return max(self)
    
    def save_to_file(self, filename:str = 'vector.pkl') -> None :
        """
        Save the vector to a binary file.

        Args:
            filename (str, optional): The filename for saving. Defaults to 'vector.pkl'.

        Raises:
            VectorError: If an error occurs during file save.

        """
        try:
            with open(filename, 'wb') as file:
                pickle.dump(self.vector, file)
        except Exception as Ex:
            raise VectorError(Ex)
    
    @classmethod
    def load_from_file(cls, filename) -> 'Vector':
        """
        Load a vector from a binary file.

        Args:
            filename (str): The filename from which to load the vector.

        Raises:
            VectorError: If an error occurs during file load.

        Returns:
            Vector: The loaded vector.
        """
        try:
            with open(filename, 'rb') as file:
                data = pickle.load(file)
            return cls(data)
        except Exception as Ex:
            raise VectorError(Ex)
        
    @classmethod
    def save_vectors_to_file(cls, vectors, filename) -> None:
        """
        Save a list of vectors to a binary file.

        Args:
            vectors (list[Vector]): The list of vectors to save.
            filename (str): The filename for saving.

        Raises:
            VectorError: If an error occurs during file save.
        """
        try:
            with open(filename, 'wb') as file:
                data = [vector.vector for vector in vectors]
                pickle.dump(data, file)
        except Exception as Ex:
            raise VectorError(Ex)

    @classmethod
    def load_vectors_from_file(cls, filename) -> list['Vector']:
        """
        Load a list of vectors from a binary file.

        Args:
            filename (str): The filename from which to load the vectors.

        Raises:
            VectorError: If an error occurs during file load.

        Returns:
            list[Vector]: The loaded list of vectors.
        """
        try:
            with open(filename, 'rb') as file:
                data = pickle.load(file)
            return [cls(vector_data) for vector_data in data]
        except Exception as Ex:
            raise VectorError(Ex)
        
    @property
    def dim(self):
        """
        Get the dimension of the vector.

        Returns:
            int: The dimension of the vector.
        """
        return len(self)
   
    @property
    def sort(self):
        """
        Sort the elements of the vector in ascending order.

        Returns:
            Vector: The sorted vector.
        """
        if len(self) <= 1:
                return self
        stack = [(0, len(self) - 1)]  
        while stack:
                left, right = stack.pop()
                pivot_index = self._partition(left, right)
                if pivot_index - 1 > left:
                    stack.append((left, pivot_index - 1))
                if pivot_index + 1 < right:
                    stack.append((pivot_index + 1, right))
        return self
    
    def _partition(self, left, right):
        """
        Helper method for sorting. Partitions the vector for the quicksort algorithm.

        Args:
            left (int): The left index.
            right (int): The right index.

        Returns:
            int: The pivot index.
        """
        pivot = self[right]
        i = left - 1
        for j in range(left, right):
            if self[j] <= pivot:
                i += 1
                self[i], self[j] = self[j], self[i]
        self[i + 1], self[right] = self[right], self[i + 1]
        return i + 1




def randvec(length:int = 1, lower:float=0, upper:float=1):
    """
    Generate a random Vector of specified length with elements between lower and upper values.

    Args:
        length (int, optional): The length of the vector. Defaults to 1.
        lower (float, optional): The lower bound for random values. Defaults to 0.
        upper (float, optional): The upper bound for random values. Defaults to 1.

    Returns:
        Vector: A random vector with specified properties.

    Raises:
        VectorError: If any error occurs during vector generation.
    """
    try:
        return Vector([random.uniform(lower,upper) for i in range(length)])
    except Exception as Ex:
        raise VectorError(Ex)
    
def zeros(num:int=0) -> 'Vector':
    """
    Create a Vector filled with zeros.

    Args:
        num (int, optional): The number of zeros in the vector. Defaults to 0.

    Returns:
        Vector: A vector filled with zeros.

    Raises:
        VectorError: If any error occurs during vector creation.
    """
    try:  
        return Vector([0]*num)
    except Exception as Ex:
            raise VectorError(Ex)

def nvec(scal:int = 1, num:int= 0) -> 'Vector':
    """
    Create a Vector with a specified scalar repeated a number of times.

    Args:
        scal (int, optional): The scalar value. Defaults to 1.
        num (int, optional): The number of times to repeat the scalar. Defaults to 0.

    Returns:
        Vector: A vector with the scalar value repeated.

    Raises:
        VectorError: If any error occurs during vector creation.
    """
    try:
        return Vector([scal] * num)
    except Exception as Ex:
        raise VectorError(Ex)

def degrees_to_radians(degrees:float):
    """
    Convert degrees to radians.

    Args:
        degrees (float): The angle in degrees.

    Returns:
        float: The angle in radians.

    Raises:
        VectorError: If any error occurs during conversion.
    """
    try:
        radians = degrees * (pi / 180)
        return radians
    except Exception as Ex:
        raise VectorError(Ex)

def radians_to_degrees(radians:float):
    """
    Convert radians to degrees.

    Args:
        radians (float): The angle in radians.

    Returns:
        float: The angle in degrees.

    Raises:
        VectorError: If any error occurs during conversion.
    """
    try:
        degrees = radians * (180 / pi)
        return degrees
    except Exception as Ex:
            raise VectorError(Ex)

def draw2d(vectors:Vector | list[Vector], color:str | list[str]=['black']):
    """
    Visualize 2D vectors with optional colors.

    Args:
        vectors (Vector | list[Vector]): A single vector or a list of vectors to visualize.
        color (str | list[str], optional): The color(s) for the vector(s). Defaults to ['black'].

    Raises:
        VectorDimensionMismatchError: If the vector dimension is not 2.
        VectorError: If any error occurs during visualization.
    """
    try:
        plt.figure()
        if isinstance(vectors, Vector):
            if len(vectors) != 2:
                raise VectorDimensionMismatchError(2,len(vectors))
            x, y = vectors[0], vectors[1]
            if color is str:
                pass
            else:
                color = color[0]
            plt.quiver(0, 0, x, y, angles='xy', scale_units='xy', scale=1, color = color)
            plt.text(x , y , f'Vec', fontsize=10)

        elif isinstance(vectors, list):
            i=0
            j=0
            for vec in vectors:
                if not isinstance(vec, Vector):
                    raise VectorError("Argument is not Vector or List of Vectors")
                if len(vec) != 2:
                    raise VectorDimensionMismatchError(2,len(vec))
                x, y = vec[0], vec[1]
                if isinstance(color,str):
                    plt.quiver(0, 0, x, y, angles='xy', scale_units='xy', scale=1, color=color)
                    plt.text(x , y , f'Vec{j+1}', fontsize=10)
                    j+=1
                else:
                    plt.quiver(0, 0, x, y, angles='xy', scale_units='xy', scale=1, color=color[i]) 
                    plt.text(x, y, f'Vec{j+1}', fontsize=10)
                    j+=1
                    if i == len(color)-1:
                        i=0
                    else:
                        i+=1
        else:
            raise VectorError("Argument is not Vector or List of Vectors")
        plt.xlim(-1, 3)
        plt.ylim(-1, 3)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Draw Vector')
        plt.grid()
        plt.show()
    except Exception as Ex:
        raise VectorError(Ex)

def draw3d(vectors:Vector | list[Vector], color:str | list[str]=['black']):
    """
    Visualize 3D vectors with optional colors.

    Args:
        vectors (Vector | list[Vector]): A single vector or a list of vectors to visualize.
        color (str | list[str], optional): The color(s) for the vector(s). Defaults to ['black'].

    Raises:
        VectorDimensionMismatchError: If the vector dimension is not 3.
        VectorError: If any error occurs during visualization.
    """
    try:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        if isinstance(vectors, Vector):
            if len(vectors) != 3:
                    raise VectorDimensionMismatchError(3,len(vectors))
            x, y, z = vectors[0], vectors[1], vectors[2]
            if color is str:
                pass
            else:
                color = color[0]
            ax.quiver(0, 0, 0, x, y, z, color=color)
            ax.text(x, y, z,  f'Vec', fontsize=10)

        elif isinstance(vectors, list):
            i=0
            j=0
            for vec in vectors:
                if not isinstance(vec, Vector):
                    raise VectorError("Argument is not Vector or List of Vectors")
                if len(vec) != 3:
                        raise VectorDimensionMismatchError(3,len(vec))
                x, y, z = vec[0], vec[1], vec[2]
                if isinstance(color,str):
                    ax.quiver(0, 0, 0, x, y, z, color=color)
                    ax.text(x , y , z, f'Vec{j+1}', fontsize=10)
                    j+=1
                else:
                    ax.quiver(0, 0, 0, x, y, z, color=color[i])
                    ax.text(x, y, z,  f'Vec{j+1}', fontsize=10)
                    j+=1
                    if i == len(color)-1:
                        i=0
                    else:
                        i+=1
        else:
            raise VectorError("Argument is not Vector or List of Vectors")
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 2])
        ax.set_zlim([0, 3])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Отрисовка вектора в 3D')
        plt.show()
    except Exception as Ex:
        raise VectorError(Ex)


