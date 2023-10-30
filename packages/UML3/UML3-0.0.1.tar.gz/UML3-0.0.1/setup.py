from setuptools import setup, find_packages

setup(name='UML3',
      version='0.0.1',
      license = "GNU GPLv3",
      url = "https://github.com/VIA-s-acc/UML3",
      description=""" provides a wide range of vector operations, including initialization, arithmetic operations, comparisons, geometric calculations, information retrieval, modification, iteration, index operations, mathematical operations, coordinate system transformations, vector operations, graphical representation, angle measurement conversion, serialization, and random vector generation.
""",
      long_description=""" versatile tool for working with vectors. It encompasses an extensive set of functionalities to manipulate and analyze vectors, making it an essential component for various mathematical and scientific applications. Whether you need to perform basic vector arithmetic or more advanced geometric calculations, this class has you covered.

Initialization:
The class features a constructor for creating vector objects and methods for setting and retrieving vector components. You can easily create, modify, and inspect vectors with these functions.

Arithmetic:
Perform fundamental vector operations such as vector addition, subtraction, scalar multiplication, scalar division, and both scalar and vector multiplication. These operations are crucial for vector manipulation.

Comparison:
Effortlessly compare vectors for equality or inequality, helping you identify whether two vectors are the same or different.

Geometric Operations:
Calculate the dot product and cross product of vectors, find the angle between two vectors, and determine the projection of one vector onto another. These operations are vital in geometry and physics.

Information Retrieval:
Obtain the dimensionality of the vector and represent it as a string, facilitating data retrieval and visualization.

Modification:
Set vector components, add or subtract other vectors, and round vector component values. These modifications make the class adaptable for various use cases.

Iteration:
The class provides an iterator to traverse vector components, streamlining operations that involve each component.

Index Operations:
Access vector components by index and utilize index-based operations, enhancing flexibility when working with vectors.

Mathematical Operations:
Calculate the sum, average, minimum, and maximum values of vector components to perform statistical and mathematical analyses.

Coordinate System Transformations:
Convert vectors between different coordinate systems, facilitating coordinate system changes for different applications.

Vector Operations:
Determine the angle between vectors and find vector projections. Check for orthogonality and parallelism between vectors for advanced vector analyses.

Graphical Representation:
Visualize vectors on graphs and charts for enhanced understanding and communication of vector data.

Angle Measurement Conversion:
Convert between radians and degrees, simplifying angle measurements in mathematical and scientific contexts.

Serialization:
Save vectors to files and load vectors from files, allowing for easy data storage and retrieval.

Random Vector Generation:
Generate random vectors with specified properties, aiding in statistical simulations and experiments.
""",
      author="Via",
      author_email="hroyango@my.msu.ru",
      packages=find_packages(),
      install_requires=[
          'matplotlib',
      ],
      zip_safe=False)