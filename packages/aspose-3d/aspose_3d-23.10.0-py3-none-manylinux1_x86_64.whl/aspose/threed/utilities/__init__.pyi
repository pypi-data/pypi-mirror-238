from typing import List, Optional, Dict, Iterable
import aspose.pycore
import aspose.pydrawing
import aspose.threed
import aspose.threed.animation
import aspose.threed.deformers
import aspose.threed.entities
import aspose.threed.formats
import aspose.threed.profiles
import aspose.threed.render
import aspose.threed.shading
import aspose.threed.utilities

class BoundingBox:
    '''The axis-aligned bounding box'''
    
    @overload
    def merge(self, pt : aspose.threed.utilities.Vector4):
        '''Merge current bounding box with given point'''
        ...
    
    @overload
    def merge(self, pt : aspose.threed.utilities.Vector3):
        '''Merge current bounding box with given point'''
        ...
    
    @overload
    def merge(self, x : float, y : float, z : float):
        '''Merge current bounding box with given point'''
        ...
    
    @overload
    def merge(self, bb : aspose.threed.utilities.BoundingBox):
        '''Merges the new box into the current bounding box.'''
        ...
    
    def scale(self) -> float:
        '''Calculates the absolute largest coordinate value of any contained point.'''
        ...
    
    @staticmethod
    def from_geometry(geometry : aspose.threed.entities.Geometry) -> aspose.threed.utilities.BoundingBox:
        '''Construct a bounding box from given geometry'''
        ...
    
    def overlaps_with(self, box : aspose.threed.utilities.BoundingBox) -> bool:
        '''Check if current bounding box overlaps with specified bounding box.
        
        :param box: The other bounding box to test'''
        ...
    
    def contains(self, p : aspose.threed.utilities.Vector3) -> bool:
        '''Check if the point p is inside the bounding box
        
        :param p: The point to test'''
        ...
    
    @property
    def extent(self) -> aspose.threed.utilities.BoundingBoxExtent:
        '''Gets the extent of the bounding box.'''
        ...
    
    @property
    def minimum(self) -> aspose.threed.utilities.Vector3:
        '''The minimum corner of the bounding box'''
        ...
    
    @property
    def maximum(self) -> aspose.threed.utilities.Vector3:
        '''The maximum corner of the bounding box'''
        ...
    
    @property
    def size(self) -> aspose.threed.utilities.Vector3:
        '''The size of the bounding box'''
        ...
    
    @property
    def center(self) -> aspose.threed.utilities.Vector3:
        '''The center of the bounding box.'''
        ...
    
    @classmethod
    @property
    def NULL(cls) -> aspose.threed.utilities.BoundingBox:
        '''The null bounding box'''
        ...
    
    @classmethod
    @property
    def INFINITE(cls) -> aspose.threed.utilities.BoundingBox:
        '''The infinite bounding box'''
        ...
    
    ...

class BoundingBox2D:
    '''The axis-aligned bounding box for :py:class:`aspose.threed.utilities.Vector2`'''
    
    @overload
    def merge(self, pt : aspose.threed.utilities.Vector2):
        '''Merges the new box into the current bounding box.'''
        ...
    
    @overload
    def merge(self, bb : aspose.threed.utilities.BoundingBox2D):
        '''Merges the new box into the current bounding box.'''
        ...
    
    @property
    def extent(self) -> aspose.threed.utilities.BoundingBoxExtent:
        '''Gets the extent of the bounding box.'''
        ...
    
    @property
    def minimum(self) -> aspose.threed.utilities.Vector2:
        '''The minimum corner of the bounding box'''
        ...
    
    @property
    def maximum(self) -> aspose.threed.utilities.Vector2:
        '''The maximum corner of the bounding box'''
        ...
    
    @classmethod
    @property
    def NULL(cls) -> aspose.threed.utilities.BoundingBox2D:
        '''The null bounding box'''
        ...
    
    @classmethod
    @property
    def INFINITE(cls) -> aspose.threed.utilities.BoundingBox2D:
        '''The infinite bounding box'''
        ...
    
    ...

class DummyFileSystem(FileSystem):
    '''Read/write operations are dummy operations.'''
    
    def read_file(self, file_name : str, options : aspose.threed.formats.IOConfig) -> io.RawIOBase:
        '''Create a stream for reading dependencies.'''
        ...
    
    def write_file(self, file_name : str, options : aspose.threed.formats.IOConfig) -> io.RawIOBase:
        '''Create a stream for writing dependencies.'''
        ...
    
    ...

class FMatrix4:
    '''Matrix 4x4 with all component in float type'''
    
    @overload
    def concatenate(self, m2 : aspose.threed.utilities.FMatrix4) -> aspose.threed.utilities.FMatrix4:
        '''Concatenates the two matrices
        
        :param m2: M2.
        :returns: New matrix4'''
        ...
    
    @overload
    def concatenate(self, m2 : aspose.threed.utilities.Matrix4) -> aspose.threed.utilities.FMatrix4:
        '''Concatenates the two matrices
        
        :param m2: M2.
        :returns: New matrix4'''
        ...
    
    def transpose(self) -> aspose.threed.utilities.FMatrix4:
        '''Transposes this instance.
        
        :returns: The transposed matrix.'''
        ...
    
    def inverse(self) -> aspose.threed.utilities.FMatrix4:
        '''Calculate the inverse matrix of current instance.
        
        :returns: Inverse matrix4'''
        ...
    
    @property
    def m00(self) -> float:
        '''The m00.'''
        ...
    
    @m00.setter
    def m00(self, value : float):
        '''The m00.'''
        ...
    
    @property
    def m01(self) -> float:
        '''The m01.'''
        ...
    
    @m01.setter
    def m01(self, value : float):
        '''The m01.'''
        ...
    
    @property
    def m02(self) -> float:
        '''The m02.'''
        ...
    
    @m02.setter
    def m02(self, value : float):
        '''The m02.'''
        ...
    
    @property
    def m03(self) -> float:
        '''The m03.'''
        ...
    
    @m03.setter
    def m03(self, value : float):
        '''The m03.'''
        ...
    
    @property
    def m10(self) -> float:
        '''The m10.'''
        ...
    
    @m10.setter
    def m10(self, value : float):
        '''The m10.'''
        ...
    
    @property
    def m11(self) -> float:
        '''The m11.'''
        ...
    
    @m11.setter
    def m11(self, value : float):
        '''The m11.'''
        ...
    
    @property
    def m12(self) -> float:
        '''The m12.'''
        ...
    
    @m12.setter
    def m12(self, value : float):
        '''The m12.'''
        ...
    
    @property
    def m13(self) -> float:
        '''The m13.'''
        ...
    
    @m13.setter
    def m13(self, value : float):
        '''The m13.'''
        ...
    
    @property
    def m20(self) -> float:
        '''The m20.'''
        ...
    
    @m20.setter
    def m20(self, value : float):
        '''The m20.'''
        ...
    
    @property
    def m21(self) -> float:
        '''The m21.'''
        ...
    
    @m21.setter
    def m21(self, value : float):
        '''The m21.'''
        ...
    
    @property
    def m22(self) -> float:
        '''The m22.'''
        ...
    
    @m22.setter
    def m22(self, value : float):
        '''The m22.'''
        ...
    
    @property
    def m23(self) -> float:
        '''The m23.'''
        ...
    
    @m23.setter
    def m23(self, value : float):
        '''The m23.'''
        ...
    
    @property
    def m30(self) -> float:
        '''The m30.'''
        ...
    
    @m30.setter
    def m30(self, value : float):
        '''The m30.'''
        ...
    
    @property
    def m31(self) -> float:
        '''The m31.'''
        ...
    
    @m31.setter
    def m31(self, value : float):
        '''The m31.'''
        ...
    
    @property
    def m32(self) -> float:
        '''The m32.'''
        ...
    
    @m32.setter
    def m32(self, value : float):
        '''The m32.'''
        ...
    
    @property
    def m33(self) -> float:
        '''The m33.'''
        ...
    
    @m33.setter
    def m33(self, value : float):
        '''The m33.'''
        ...
    
    @classmethod
    @property
    def IDENTITY(cls) -> aspose.threed.utilities.FMatrix4:
        '''The identity matrix'''
        ...
    
    ...

class FVector2:
    '''A float vector with two components.'''
    
    def equals(self, rhs : aspose.threed.utilities.FVector2) -> bool:
        '''Check if two vectors are equal'''
        ...
    
    ...

class FVector3:
    '''A float vector with three components.'''
    
    def normalize(self) -> aspose.threed.utilities.FVector3:
        '''Normalizes this instance.
        
        :returns: Normalized vector.'''
        ...
    
    def cross(self, rhs : aspose.threed.utilities.FVector3) -> aspose.threed.utilities.FVector3:
        '''Cross product of two vectors
        
        :param rhs: Right hand side value.
        :returns: Cross product of two :py:class:`aspose.threed.utilities.FVector3`s.'''
        ...
    
    @classmethod
    @property
    def zero(cls) -> aspose.threed.utilities.FVector3:
        '''The Zero vector.'''
        ...
    
    @classmethod
    @property
    def one(cls) -> aspose.threed.utilities.FVector3:
        '''The unit scale vector with all components are all 1'''
        ...
    
    @classmethod
    @property
    def UNIT_SCALE(cls) -> aspose.threed.utilities.FVector3:
        ...
    
    ...

class FVector4:
    '''A float vector with four components.'''
    
    ...

class FileSystem:
    '''File system encapsulation.
    Aspose.3D will use this to read/write dependencies.'''
    
    def read_file(self, file_name : str, options : aspose.threed.formats.IOConfig) -> io.RawIOBase:
        '''Create a stream for reading dependencies.'''
        ...
    
    def write_file(self, file_name : str, options : aspose.threed.formats.IOConfig) -> io.RawIOBase:
        '''Create a stream for writing dependencies.'''
        ...
    
    ...

class IOUtils:
    '''Utilities to write matrix/vector to binary writer'''
    
    ...

class LocalFileSystem(FileSystem):
    '''The :py:class:`aspose.threed.utilities.LocalFileSystem` will maps the read/write operations to local directory.'''
    
    def read_file(self, file_name : str, options : aspose.threed.formats.IOConfig) -> io.RawIOBase:
        '''Create a stream for reading dependencies.'''
        ...
    
    def write_file(self, file_name : str, options : aspose.threed.formats.IOConfig) -> io.RawIOBase:
        '''Create a stream for writing dependencies.'''
        ...
    
    ...

class MathUtils:
    '''A set of useful mathematical utilities.'''
    
    @overload
    @staticmethod
    def to_degree(radian : aspose.threed.utilities.Vector3) -> aspose.threed.utilities.Vector3:
        '''Convert a :py:class:`aspose.threed.utilities.Vector3` from radian to degree.
        
        :param radian: The radian value.
        :returns: The degree value.'''
        ...
    
    @overload
    @staticmethod
    def to_degree(radian : float) -> float:
        '''Convert a number from radian to degree
        
        :param radian: The radian value.
        :returns: The degree value.'''
        ...
    
    @overload
    @staticmethod
    def to_degree(radian : float) -> float:
        '''Convert a number from radian to degree
        
        :param radian: The radian value.
        :returns: The degree value.'''
        ...
    
    @overload
    @staticmethod
    def to_degree(x : floaty : float, z : float) -> aspose.threed.utilities.Vector3:
        '''Convert a number from radian to degree
        
        :param x: The x component in radian value.
        :param y: The y component in radian value.
        :param z: The z component in radian value.
        :returns: The degree value.'''
        ...
    
    @overload
    @staticmethod
    def to_radian(degree : aspose.threed.utilities.Vector3) -> aspose.threed.utilities.Vector3:
        '''Convert a :py:class:`aspose.threed.utilities.Vector3` from degree to radian
        
        :param degree: The degree value.
        :returns: The radian value.'''
        ...
    
    @overload
    @staticmethod
    def to_radian(degree : float) -> float:
        '''Convert a number from degree to radian
        
        :param degree: The degree value.
        :returns: The radian value.'''
        ...
    
    @overload
    @staticmethod
    def to_radian(degree : float) -> float:
        '''Convert a number from degree to radian
        
        :param degree: The degree value.
        :returns: The radian value.'''
        ...
    
    @overload
    @staticmethod
    def to_radian(x : floaty : float, z : float) -> aspose.threed.utilities.Vector3:
        '''Convert a vector from degree to radian
        
        :param x: The x component in degree value.
        :param y: The y component in degree value.
        :param z: The z component in degree value.
        :returns: The radian value.'''
        ...
    
    @staticmethod
    def clamp(val : floatmin : float, max : float) -> float:
        '''Clamp value to range [min, max]
        
        :param val: Value to clamp.
        :param min: Minimum value.
        :param max: Maximum value.
        :returns: The value between [min, max]'''
        ...
    
    ...

class Matrix4:
    '''4x4 matrix implementation.'''
    
    @overload
    @staticmethod
    def translate(t : aspose.threed.utilities.Vector3) -> aspose.threed.utilities.Matrix4:
        '''Creates a matrix that translates along the x-axis, the y-axis and the z-axis
        
        :param t: Translate offset'''
        ...
    
    @overload
    @staticmethod
    def translate(tx : floatty : float, tz : float) -> aspose.threed.utilities.Matrix4:
        '''Creates a matrix that translates along the x-axis, the y-axis and the z-axis
        
        :param tx: X-coordinate offset
        :param ty: Y-coordinate offset
        :param tz: Z-coordinate offset'''
        ...
    
    @overload
    @staticmethod
    def scale(s : aspose.threed.utilities.Vector3) -> aspose.threed.utilities.Matrix4:
        '''Creates a matrix that scales along the x-axis, the y-axis and the z-axis.
        
        :param s: Scaling factories applies to the x-axis, the y-axis and the z-axis'''
        ...
    
    @overload
    @staticmethod
    def scale(s : float) -> aspose.threed.utilities.Matrix4:
        '''Creates a matrix that scales along the x-axis, the y-axis and the z-axis.
        
        :param s: Scaling factories applies to all axex'''
        ...
    
    @overload
    @staticmethod
    def scale(sx : floatsy : float, sz : float) -> aspose.threed.utilities.Matrix4:
        '''Creates a matrix that scales along the x-axis, the y-axis and the z-axis.
        
        :param sx: Scaling factories applies to the x-axis
        :param sy: Scaling factories applies to the y-axis
        :param sz: Scaling factories applies to the z-axis'''
        ...
    
    @overload
    @staticmethod
    def rotate_from_euler(eul : aspose.threed.utilities.Vector3) -> aspose.threed.utilities.Matrix4:
        '''Create a rotation matrix from Euler angle
        
        :param eul: Rotation in radian'''
        ...
    
    @overload
    @staticmethod
    def rotate_from_euler(rx : floatry : float, rz : float) -> aspose.threed.utilities.Matrix4:
        '''Create a rotation matrix from Euler angle
        
        :param rx: Rotation in x axis in radian
        :param ry: Rotation in y axis in radian
        :param rz: Rotation in z axis in radian'''
        ...
    
    @overload
    @staticmethod
    def rotate(angle : floataxis : aspose.threed.utilities.Vector3) -> aspose.threed.utilities.Matrix4:
        '''Create a rotation matrix by rotation angle and axis
        
        :param angle: Rotate angle in radian
        :param axis: Rotation axis'''
        ...
    
    @overload
    @staticmethod
    def rotate(q : aspose.threed.utilities.Quaternion) -> aspose.threed.utilities.Matrix4:
        '''Create a rotation matrix from a quaternion
        
        :param q: Rotation quaternion'''
        ...
    
    def concatenate(self, m2 : aspose.threed.utilities.Matrix4) -> aspose.threed.utilities.Matrix4:
        '''Concatenates the two matrices
        
        :param m2: M2.
        :returns: New matrix4'''
        ...
    
    def transpose(self) -> aspose.threed.utilities.Matrix4:
        '''Transposes this instance.
        
        :returns: The transposed matrix.'''
        ...
    
    def normalize(self) -> aspose.threed.utilities.Matrix4:
        '''Normalizes this instance.
        
        :returns: Normalize matrix4'''
        ...
    
    def inverse(self) -> aspose.threed.utilities.Matrix4:
        '''Inverses this instance.
        
        :returns: Inverse matrix4'''
        ...
    
    def set_trs(self, translation : aspose.threed.utilities.Vector3, rotation : aspose.threed.utilities.Vector3, scale : aspose.threed.utilities.Vector3):
        '''Initializes the matrix with translation/rotation/scale
        
        :param translation: Translation.
        :param rotation: Euler angles for rotation, fields are in degree.
        :param scale: Scale.'''
        ...
    
    def to_array(self) -> List[float]:
        '''Converts matrix to array.
        
        :returns: The array.'''
        ...
    
    def decompose(self, translation : Any, scaling : Any, rotation : Any) -> bool:
        ...
    
    @classmethod
    @property
    def identity(cls) -> aspose.threed.utilities.Matrix4:
        '''Gets the identity matrix.'''
        ...
    
    @property
    def determinant(self) -> float:
        '''Gets the determinant of the matrix.'''
        ...
    
    @property
    def m00(self) -> float:
        '''The m00.'''
        ...
    
    @m00.setter
    def m00(self, value : float):
        '''The m00.'''
        ...
    
    @property
    def m01(self) -> float:
        '''The m01.'''
        ...
    
    @m01.setter
    def m01(self, value : float):
        '''The m01.'''
        ...
    
    @property
    def m02(self) -> float:
        '''The m02.'''
        ...
    
    @m02.setter
    def m02(self, value : float):
        '''The m02.'''
        ...
    
    @property
    def m03(self) -> float:
        '''The m03.'''
        ...
    
    @m03.setter
    def m03(self, value : float):
        '''The m03.'''
        ...
    
    @property
    def m10(self) -> float:
        '''The m10.'''
        ...
    
    @m10.setter
    def m10(self, value : float):
        '''The m10.'''
        ...
    
    @property
    def m11(self) -> float:
        '''The m11.'''
        ...
    
    @m11.setter
    def m11(self, value : float):
        '''The m11.'''
        ...
    
    @property
    def m12(self) -> float:
        '''The m12.'''
        ...
    
    @m12.setter
    def m12(self, value : float):
        '''The m12.'''
        ...
    
    @property
    def m13(self) -> float:
        '''The m13.'''
        ...
    
    @m13.setter
    def m13(self, value : float):
        '''The m13.'''
        ...
    
    @property
    def m20(self) -> float:
        '''The m20.'''
        ...
    
    @m20.setter
    def m20(self, value : float):
        '''The m20.'''
        ...
    
    @property
    def m21(self) -> float:
        '''The m21.'''
        ...
    
    @m21.setter
    def m21(self, value : float):
        '''The m21.'''
        ...
    
    @property
    def m22(self) -> float:
        '''The m22.'''
        ...
    
    @m22.setter
    def m22(self, value : float):
        '''The m22.'''
        ...
    
    @property
    def m23(self) -> float:
        '''The m23.'''
        ...
    
    @m23.setter
    def m23(self, value : float):
        '''The m23.'''
        ...
    
    @property
    def m30(self) -> float:
        '''The m30.'''
        ...
    
    @m30.setter
    def m30(self, value : float):
        '''The m30.'''
        ...
    
    @property
    def m31(self) -> float:
        '''The m31.'''
        ...
    
    @m31.setter
    def m31(self, value : float):
        '''The m31.'''
        ...
    
    @property
    def m32(self) -> float:
        '''The m32.'''
        ...
    
    @m32.setter
    def m32(self, value : float):
        '''The m32.'''
        ...
    
    @property
    def m33(self) -> float:
        '''The m33.'''
        ...
    
    @m33.setter
    def m33(self, value : float):
        '''The m33.'''
        ...
    
    ...

class MemoryFileSystem(FileSystem):
    '''The :py:class:`aspose.threed.utilities.MemoryFileSystem` will maps the read/write operations to memory.'''
    
    def read_file(self, file_name : str, options : aspose.threed.formats.IOConfig) -> io.RawIOBase:
        '''Create a stream for reading dependencies.'''
        ...
    
    def write_file(self, file_name : str, options : aspose.threed.formats.IOConfig) -> io.RawIOBase:
        '''Create a stream for writing dependencies.'''
        ...
    
    def get_file_content(self, file_name : str) -> bytes:
        '''Returns the raw content of the specified file.
        Throw :py:class:`System.IO.FileNotFoundException` if the specified file is not existing.'''
        ...
    
    @property
    def file_names(self) -> List[str]:
        ...
    
    ...

class ParseException:
    '''Exception when Aspose.3D failed to parse the input.'''
    
    ...

class Quaternion:
    '''Quaternion is usually used to perform rotation in computer graphics.'''
    
    @overload
    @staticmethod
    def from_euler_angle(pitch : floatyaw : float, roll : float) -> aspose.threed.utilities.Quaternion:
        '''Creates quaternion from given Euler angle
        
        :param pitch: Pitch in radian
        :param yaw: Yaw in radian
        :param roll: Roll in radian
        :returns: Created quaternion'''
        ...
    
    @overload
    @staticmethod
    def from_euler_angle(euler_angle : aspose.threed.utilities.Vector3) -> aspose.threed.utilities.Quaternion:
        '''Creates quaternion from given Euler angle
        
        :param euler_angle: Euler angle in radian
        :returns: Created quaternion'''
        ...
    
    def conjugate(self) -> aspose.threed.utilities.Quaternion:
        '''Returns a conjugate quaternion of current quaternion
        
        :returns: The conjugate quaternion.'''
        ...
    
    def inverse(self) -> aspose.threed.utilities.Quaternion:
        '''Returns a inverse quaternion of current quaternion
        
        :returns: Inverse quaternion.'''
        ...
    
    def dot(self, q : aspose.threed.utilities.Quaternion) -> float:
        '''Dots product
        
        :param q: The quaternion
        :returns: Dot value'''
        ...
    
    def euler_angles(self) -> aspose.threed.utilities.Vector3:
        '''Converts quaternion to rotation represented by Euler angles
        All components are in radian
        
        :returns: Result vector'''
        ...
    
    def normalize(self) -> aspose.threed.utilities.Quaternion:
        '''Normalize the quaternion
        
        :returns: Normalized quaternion.'''
        ...
    
    def to_angle_axis(self, angle : Any, axis : Any):
        ...
    
    def concat(self, rhs : aspose.threed.utilities.Quaternion) -> aspose.threed.utilities.Quaternion:
        '''Concatenate two quaternions'''
        ...
    
    @staticmethod
    def from_angle_axis(a : floataxis : aspose.threed.utilities.Vector3) -> aspose.threed.utilities.Quaternion:
        '''Creates a quaternion around given axis and rotate in clockwise
        
        :param a: Clockwise rotation in radian
        :param axis: Axis
        :returns: Created quaternion'''
        ...
    
    @staticmethod
    def from_rotation(orig : aspose.threed.utilities.Vector3dest : aspose.threed.utilities.Vector3) -> aspose.threed.utilities.Quaternion:
        '''Creates a quaternion that rotate from original to destination direction
        
        :param orig: Original direction
        :param dest: Destination direction
        :returns: Created quaternion'''
        ...
    
    def to_matrix(self) -> aspose.threed.utilities.Matrix4:
        '''Convert the rotation presented by quaternion to transform matrix.
        
        :returns: The matrix representation of current quaternion.'''
        ...
    
    @staticmethod
    def interpolate(t : floatfrom_address : aspose.threed.utilities.Quaternion, to : aspose.threed.utilities.Quaternion) -> aspose.threed.utilities.Quaternion:
        '''Populates this quaternion with the interpolated value between the given quaternion arguments for a t between from and to.
        
        :param t: The coefficient to interpolate.
        :param from_address: Source quaternion.
        :param to: Target quaternion.
        :returns: The interpolated quaternion.'''
        ...
    
    @property
    def length(self) -> float:
        '''Gets the length of the quaternion'''
        ...
    
    @classmethod
    @property
    def IDENTITY(cls) -> aspose.threed.utilities.Quaternion:
        '''The Identity quaternion.'''
        ...
    
    ...

class Rect:
    '''A class to represent the rectangle'''
    
    def contains(self, x : int, y : int) -> bool:
        '''Return true if the given point is inside the rectangle.'''
        ...
    
    @property
    def width(self) -> int:
        '''Gets the width of the size'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Sets the width of the size'''
        ...
    
    @property
    def height(self) -> int:
        '''Gets the height of the size'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Sets the height of the size'''
        ...
    
    @property
    def x(self) -> int:
        '''Gets the x of the size'''
        ...
    
    @x.setter
    def x(self, value : int):
        '''Sets the x of the size'''
        ...
    
    @property
    def y(self) -> int:
        '''Gets the y of the size'''
        ...
    
    @y.setter
    def y(self, value : int):
        '''Sets the y of the size'''
        ...
    
    @property
    def left(self) -> int:
        '''Gets the left of the rectangle'''
        ...
    
    @property
    def right(self) -> int:
        '''Gets the right of the rectangle'''
        ...
    
    @property
    def top(self) -> int:
        '''Gets the top of the rectangle'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Gets the bottom of the rectangle'''
        ...
    
    ...

class RelativeRectangle:
    '''Relative rectangle
    The formula between relative component to absolute value is:
    Scale * (Reference Width) + offset
    So if we want it to represent an absolute value, leave all scale fields zero, and use offset fields instead.'''
    
    def to_absolute(self, left : int, top : int, width : int, height : int) -> aspose.threed.utilities.Rect:
        '''Convert the relative rectangle to absolute rectangle
        
        :param left: Left of the rectangle
        :param top: Top of the rectangle
        :param width: Width of the rectangle
        :param height: Height of the rectangle'''
        ...
    
    @staticmethod
    def from_scale(scale_x : floatscale_y : float, scale_width : float, scale_height : float) -> aspose.threed.utilities.RelativeRectangle:
        '''Construct a :py:class:`aspose.threed.utilities.RelativeRectangle` with all offset fields zero and scale fields from given parameters.'''
        ...
    
    @property
    def scale_x(self) -> float:
        ...
    
    @scale_x.setter
    def scale_x(self, value : float):
        ...
    
    @property
    def scale_y(self) -> float:
        ...
    
    @scale_y.setter
    def scale_y(self, value : float):
        ...
    
    @property
    def scale_width(self) -> float:
        ...
    
    @scale_width.setter
    def scale_width(self, value : float):
        ...
    
    @property
    def scale_height(self) -> float:
        ...
    
    @scale_height.setter
    def scale_height(self, value : float):
        ...
    
    @property
    def offset_x(self) -> int:
        ...
    
    @offset_x.setter
    def offset_x(self, value : int):
        ...
    
    @property
    def offset_y(self) -> int:
        ...
    
    @offset_y.setter
    def offset_y(self, value : int):
        ...
    
    @property
    def offset_width(self) -> int:
        ...
    
    @offset_width.setter
    def offset_width(self, value : int):
        ...
    
    @property
    def offset_height(self) -> int:
        ...
    
    @offset_height.setter
    def offset_height(self, value : int):
        ...
    
    ...

class SemanticAttribute:
    '''Allow user to use their own structure for static declaration of :py:class:`aspose.threed.utilities.VertexDeclaration`'''
    
    @property
    def semantic(self) -> aspose.threed.utilities.VertexFieldSemantic:
        '''Semantic of the vertex field'''
        ...
    
    @property
    def alias(self) -> str:
        '''Alias of the vertex field'''
        ...
    
    ...

class TransformBuilder:
    '''The :py:class:`aspose.threed.utilities.TransformBuilder` is used to build transform matrix by a chain of transformations.'''
    
    @overload
    def scale(self, s : float) -> aspose.threed.utilities.TransformBuilder:
        '''Chain a scaling transform matrix with a component scaled by s'''
        ...
    
    @overload
    def scale(self, x : float, y : float, z : float) -> aspose.threed.utilities.TransformBuilder:
        '''Chain a scaling transform matrix'''
        ...
    
    @overload
    def scale(self, s : aspose.threed.utilities.Vector3) -> aspose.threed.utilities.TransformBuilder:
        '''Chain a scale transform'''
        ...
    
    @overload
    def rotate_degree(self, angle : float, axis : aspose.threed.utilities.Vector3) -> aspose.threed.utilities.TransformBuilder:
        '''Chain a rotation transform in degree
        
        :param angle: The angle to rotate in degree
        :param axis: The axis to rotate'''
        ...
    
    @overload
    def rotate_degree(self, rot : aspose.threed.utilities.Vector3, order : aspose.threed.utilities.RotationOrder):
        '''Append rotation with specified order
        
        :param rot: Rotation in degrees'''
        ...
    
    @overload
    def rotate_radian(self, angle : float, axis : aspose.threed.utilities.Vector3) -> aspose.threed.utilities.TransformBuilder:
        '''Chain a rotation transform in radian
        
        :param angle: The angle to rotate in radian
        :param axis: The axis to rotate'''
        ...
    
    @overload
    def rotate_radian(self, rot : aspose.threed.utilities.Vector3, order : aspose.threed.utilities.RotationOrder):
        '''Append rotation with specified order
        
        :param rot: Rotation in radian'''
        ...
    
    @overload
    def rotate_euler_radian(self, x : float, y : float, z : float) -> aspose.threed.utilities.TransformBuilder:
        '''Chain a rotation by Euler angles in radian'''
        ...
    
    @overload
    def rotate_euler_radian(self, r : aspose.threed.utilities.Vector3) -> aspose.threed.utilities.TransformBuilder:
        '''Chain a rotation by Euler angles in radian'''
        ...
    
    @overload
    def translate(self, tx : float, ty : float, tz : float) -> aspose.threed.utilities.TransformBuilder:
        '''Chain a translation transform'''
        ...
    
    @overload
    def translate(self, v : aspose.threed.utilities.Vector3) -> aspose.threed.utilities.TransformBuilder:
        '''Chain a translation transform'''
        ...
    
    def compose(self, m : aspose.threed.utilities.Matrix4):
        '''Append or prepend the argument to internal matrix.'''
        ...
    
    def append(self, m : aspose.threed.utilities.Matrix4) -> aspose.threed.utilities.TransformBuilder:
        '''Append the new transform matrix to the transform chain.'''
        ...
    
    def prepend(self, m : aspose.threed.utilities.Matrix4) -> aspose.threed.utilities.TransformBuilder:
        '''Prepend the new transform matrix to the transform chain.'''
        ...
    
    def rearrange(self, new_x : aspose.threed.Axis, new_y : aspose.threed.Axis, new_z : aspose.threed.Axis) -> aspose.threed.utilities.TransformBuilder:
        '''Rearrange the layout of the axis.
        
        :param new_x: The new x component source
        :param new_y: The new y component source
        :param new_z: The new z component source'''
        ...
    
    def rotate(self, q : aspose.threed.utilities.Quaternion) -> aspose.threed.utilities.TransformBuilder:
        '''Chain a rotation by a quaternion'''
        ...
    
    def rotate_euler_degree(self, deg_x : float, deg_y : float, deg_z : float) -> aspose.threed.utilities.TransformBuilder:
        '''Chain a rotation by Euler angles in degree'''
        ...
    
    def reset(self):
        '''Reset the transform to identity matrix'''
        ...
    
    @property
    def matrix(self) -> aspose.threed.utilities.Matrix4:
        '''Gets the current matrix value'''
        ...
    
    @matrix.setter
    def matrix(self, value : aspose.threed.utilities.Matrix4):
        '''Sets the current matrix value'''
        ...
    
    @property
    def compose_order(self) -> aspose.threed.utilities.ComposeOrder:
        ...
    
    @compose_order.setter
    def compose_order(self, value : aspose.threed.utilities.ComposeOrder):
        ...
    
    ...

class Vector2:
    '''A vector with two components.'''
    
    def dot(self, rhs : aspose.threed.utilities.Vector2) -> float:
        '''Gets the dot product of two vectors
        
        :param rhs: Right hand side value.
        :returns: The dot product of the two vectors.'''
        ...
    
    def equals(self, rhs : aspose.threed.utilities.Vector2) -> bool:
        '''Check if two vector2 equals
        
        :param rhs: The right hand side value.
        :returns: True if all components are identically equal.'''
        ...
    
    def cross(self, v : aspose.threed.utilities.Vector2) -> float:
        '''Cross product of two vectors'''
        ...
    
    def normalize(self) -> aspose.threed.utilities.Vector2:
        '''Normalizes this instance.
        
        :returns: Normalized vector.'''
        ...
    
    def compare_to(self, other : aspose.threed.utilities.Vector2) -> int:
        '''Compare current vector to another instance.'''
        ...
    
    @property
    def u(self) -> float:
        '''Gets the U component if the :py:class:`aspose.threed.utilities.Vector2` is used as a mapping coordinate.
        It's an alias of x component.'''
        ...
    
    @u.setter
    def u(self, value : float):
        '''Sets the U component if the :py:class:`aspose.threed.utilities.Vector2` is used as a mapping coordinate.
        It's an alias of x component.'''
        ...
    
    @property
    def v(self) -> float:
        '''Gets the V component if the :py:class:`aspose.threed.utilities.Vector2` is used as a mapping coordinate.
        It's an alias of y component.'''
        ...
    
    @v.setter
    def v(self, value : float):
        '''Sets the V component if the :py:class:`aspose.threed.utilities.Vector2` is used as a mapping coordinate.
        It's an alias of y component.'''
        ...
    
    @property
    def length(self) -> float:
        '''Gets the length.'''
        ...
    
    ...

class Vector3:
    '''A vector with three components.'''
    
    @overload
    def angle_between(self, dir : aspose.threed.utilities.Vector3, up : aspose.threed.utilities.Vector3) -> float:
        '''Calculate the inner angle between two direction
        Two direction can be non-normalized vectors
        
        :param dir: The direction vector to compare with
        :param up: The up vector of the two direction's shared plane
        :returns: inner angle in radian'''
        ...
    
    @overload
    def angle_between(self, dir : aspose.threed.utilities.Vector3) -> float:
        '''Calculate the inner angle between two direction
        Two direction can be non-normalized vectors
        
        :param dir: The direction vector to compare with
        :returns: inner angle in radian'''
        ...
    
    def dot(self, rhs : aspose.threed.utilities.Vector3) -> float:
        '''Gets the dot product of two vectors
        
        :param rhs: Right hand side value.
        :returns: The dot product of the two vectors.'''
        ...
    
    def normalize(self) -> aspose.threed.utilities.Vector3:
        '''Normalizes this instance.
        
        :returns: Normalized vector.'''
        ...
    
    def sin(self) -> aspose.threed.utilities.Vector3:
        '''Calculates sine on each component
        
        :returns: Calculated :py:class:`aspose.threed.utilities.Vector3`.'''
        ...
    
    def cos(self) -> aspose.threed.utilities.Vector3:
        '''Calculates cosine on each component
        
        :returns: Calculated :py:class:`aspose.threed.utilities.Vector3`.'''
        ...
    
    def cross(self, rhs : aspose.threed.utilities.Vector3) -> aspose.threed.utilities.Vector3:
        '''Cross product of two vectors
        
        :param rhs: Right hand side value.
        :returns: Cross product of two :py:class:`aspose.threed.utilities.Vector3`s.'''
        ...
    
    def set(self, new_x : float, new_y : float, new_z : float):
        '''Sets the x/y/z component in one call.
        
        :param new_x: The x component.
        :param new_y: The y component.
        :param new_z: The z component.'''
        ...
    
    def compare_to(self, other : aspose.threed.utilities.Vector3) -> int:
        '''Compare current vector to another instance.'''
        ...
    
    @property
    def length2(self) -> float:
        '''Gets the square of the length.'''
        ...
    
    @property
    def length(self) -> float:
        '''Gets the length of this vector.'''
        ...
    
    @classmethod
    @property
    def zero(cls) -> aspose.threed.utilities.Vector3:
        '''Gets unit vector (0, 0, 0)'''
        ...
    
    @classmethod
    @property
    def one(cls) -> aspose.threed.utilities.Vector3:
        '''Gets unit vector (1, 1, 1)'''
        ...
    
    @classmethod
    @property
    def unit_x(cls) -> aspose.threed.utilities.Vector3:
        ...
    
    @classmethod
    @property
    def unit_y(cls) -> aspose.threed.utilities.Vector3:
        ...
    
    @classmethod
    @property
    def unit_z(cls) -> aspose.threed.utilities.Vector3:
        ...
    
    @classmethod
    @property
    def ORIGIN(cls) -> aspose.threed.utilities.Vector3:
        '''Gets the origin position.'''
        ...
    
    @classmethod
    @property
    def UNIT_SCALE(cls) -> aspose.threed.utilities.Vector3:
        ...
    
    @classmethod
    @property
    def X_AXIS(cls) -> aspose.threed.utilities.Vector3:
        ...
    
    @classmethod
    @property
    def Y_AXIS(cls) -> aspose.threed.utilities.Vector3:
        ...
    
    @classmethod
    @property
    def Z_AXIS(cls) -> aspose.threed.utilities.Vector3:
        ...
    
    def __getitem__(self, key : int) -> float:
        ...
    
    def __setitem__(self, key : int, value : float):
        ...
    
    ...

class Vector4:
    '''A vector with four components.'''
    
    @overload
    def set(self, new_x : float, new_y : float, new_z : float):
        '''Sets vector's xyz components at a time, w will be set to 1
        
        :param new_x: New X component.
        :param new_y: New Y component.
        :param new_z: New Z component.'''
        ...
    
    @overload
    def set(self, new_x : float, new_y : float, new_z : float, new_w : float):
        '''Sets vector's all components at a time
        
        :param new_x: New X component.
        :param new_y: New Y component.
        :param new_z: New Z component.
        :param new_w: New W component.'''
        ...
    
    def compare_to(self, other : aspose.threed.utilities.Vector4) -> int:
        '''Compare current vector to another instance.'''
        ...
    
    ...

class Vertex:
    '''Vertex reference, used to access the raw vertex in :py:class:`aspose.threed.entities.TriMesh`.'''
    
    def compare_to(self, other : aspose.threed.utilities.Vertex) -> int:
        '''Compare the vertex with another vertex instance'''
        ...
    
    def read_vector4(self, field : aspose.threed.utilities.VertexField) -> aspose.threed.utilities.Vector4:
        '''Read the vector4 field
        
        :param field: The field with a Vector4/FVector4 data type'''
        ...
    
    def read_f_vector4(self, field : aspose.threed.utilities.VertexField) -> aspose.threed.utilities.FVector4:
        '''Read the vector4 field
        
        :param field: The field with a Vector4/FVector4 data type'''
        ...
    
    def read_vector3(self, field : aspose.threed.utilities.VertexField) -> aspose.threed.utilities.Vector3:
        '''Read the vector3 field
        
        :param field: The field with a Vector3/FVector3 data type'''
        ...
    
    def read_f_vector3(self, field : aspose.threed.utilities.VertexField) -> aspose.threed.utilities.FVector3:
        '''Read the vector3 field
        
        :param field: The field with a Vector3/FVector3 data type'''
        ...
    
    def read_vector2(self, field : aspose.threed.utilities.VertexField) -> aspose.threed.utilities.Vector2:
        '''Read the vector2 field
        
        :param field: The field with a Vector2/FVector2 data type'''
        ...
    
    def read_f_vector2(self, field : aspose.threed.utilities.VertexField) -> aspose.threed.utilities.FVector2:
        '''Read the vector2 field
        
        :param field: The field with a Vector2/FVector2 data type'''
        ...
    
    def read_double(self, field : aspose.threed.utilities.VertexField) -> float:
        '''Read the double field
        
        :param field: The field with a float/double compatible data type'''
        ...
    
    def read_float(self, field : aspose.threed.utilities.VertexField) -> float:
        '''Read the float field
        
        :param field: The field with a float/double compatible data type'''
        ...
    
    ...

class VertexDeclaration:
    '''The declaration of a custom defined vertex's structure'''
    
    def clear(self):
        '''Clear all fields.'''
        ...
    
    def add_field(self, data_type : aspose.threed.utilities.VertexFieldDataType, semantic : aspose.threed.utilities.VertexFieldSemantic, index : int, alias : str) -> aspose.threed.utilities.VertexField:
        '''Add a new vertex field
        
        :param data_type: The data type of the vertex field
        :param semantic: How will this field used for
        :param index: The index for same field semantic, -1 for auto-generation
        :param alias: The alias name of the field'''
        ...
    
    @staticmethod
    def from_geometry(geometry : aspose.threed.entities.Geometryuse_float : bool) -> aspose.threed.utilities.VertexDeclaration:
        '''Create a :py:class:`aspose.threed.utilities.VertexDeclaration` based on a :py:class:`aspose.threed.entities.Geometry`'s layout.
        
        :param use_float: Use float instead of double type'''
        ...
    
    def compare_to(self, other : aspose.threed.utilities.VertexDeclaration) -> int:
        '''Compares this instance to a specified object and returns an indication of their relative values.'''
        ...
    
    @property
    def sealed(self) -> bool:
        '''A :py:class:`aspose.threed.utilities.VertexDeclaration` will be sealed when its been used by :py:class:`Aspose.ThreeD.Entities.TriMesh`1` or :py:class:`aspose.threed.entities.TriMesh`, no more modifications is allowed.'''
        ...
    
    @property
    def count(self) -> int:
        '''Gets the count of all fields defined in this :py:class:`aspose.threed.utilities.VertexDeclaration`'''
        ...
    
    @property
    def size(self) -> int:
        '''The size in byte of the vertex structure.'''
        ...
    
    def __getitem__(self, key : int) -> aspose.threed.utilities.VertexField:
        ...
    
    ...

class VertexField:
    '''Vertex's field memory layout description.'''
    
    def compare_to(self, other : aspose.threed.utilities.VertexField) -> int:
        '''Compares this instance to a specified object and returns an indication of their relative values.'''
        ...
    
    @property
    def data_type(self) -> aspose.threed.utilities.VertexFieldDataType:
        ...
    
    @property
    def semantic(self) -> aspose.threed.utilities.VertexFieldSemantic:
        '''The usage semantic of this field.'''
        ...
    
    @property
    def alias(self) -> str:
        '''Alias annotated by attribute :py:class:`aspose.threed.utilities.SemanticAttribute`'''
        ...
    
    @property
    def index(self) -> int:
        '''Index of this field in the vertex's layout with same semantic.'''
        ...
    
    @property
    def offset(self) -> int:
        '''The offset in bytes of this field.'''
        ...
    
    @property
    def size(self) -> int:
        '''The size in bytes of this field'''
        ...
    
    ...

class Watermark:
    '''Utility to encode/decode blind watermark  to/from a mesh.'''
    
    @overload
    @staticmethod
    def encode_watermark(input : aspose.threed.entities.Meshtext : str) -> aspose.threed.entities.Mesh:
        '''Encode a text into mesh' blind watermark.
        
        :param input: Mesh to encode a blind watermark
        :param text: Text to encode to the mesh
        :returns: A new mesh instance with blind watermark encoded'''
        ...
    
    @overload
    @staticmethod
    def encode_watermark(input : aspose.threed.entities.Meshtext : str, password : str) -> aspose.threed.entities.Mesh:
        '''Encode a text into mesh' blind watermark.
        
        :param input: Mesh to encode a blind watermark
        :param text: Text to encode to the mesh
        :param password: Password to protect the watermark, it's optional
        :returns: A new mesh instance with blind watermark encoded'''
        ...
    
    @overload
    @staticmethod
    def decode_watermark(input : aspose.threed.entities.Mesh) -> str:
        '''Decode the watermark from a mesh
        
        :param input: The mesh to extract watermark
        :returns: Blind watermark or null if no watermark decoded.'''
        ...
    
    @overload
    @staticmethod
    def decode_watermark(input : aspose.threed.entities.Meshpassword : str) -> str:
        '''Decode the watermark from a mesh
        
        :param input: The mesh to extract watermark
        :param password: The password to decrypt the watermark
        :returns: Blind watermark or null if no watermark decoded.'''
        ...
    
    ...

class ZipArchiveFileSystem(FileSystem):
    '''File system to provide to the read-only access to speicified zip file or zip stream.
    File system will be disposed after the open/save operation.'''
    
    def read_file(self, file_name : str, options : aspose.threed.formats.IOConfig) -> io.RawIOBase:
        '''Open file for reading'''
        ...
    
    def write_file(self, file_name : str, options : aspose.threed.formats.IOConfig) -> io.RawIOBase:
        '''Open file for writing, not implemented in this class.'''
        ...
    
    ...

class BoundingBoxExtent:
    '''The extent of the bounding box'''
    
    @classmethod
    @property
    def NULL(cls) -> BoundingBoxExtent:
        '''Null bounding box'''
        ...
    
    @classmethod
    @property
    def FINITE(cls) -> BoundingBoxExtent:
        '''Finite bounding box'''
        ...
    
    @classmethod
    @property
    def INFINITE(cls) -> BoundingBoxExtent:
        '''Infinite bounding box'''
        ...
    
    ...

class ComposeOrder:
    '''The order to compose transform matrix'''
    
    @classmethod
    @property
    def APPEND(cls) -> ComposeOrder:
        '''Append the new transform to the chain'''
        ...
    
    @classmethod
    @property
    def PREPEND(cls) -> ComposeOrder:
        '''Prepend the new transform to the chain'''
        ...
    
    ...

class RotationOrder:
    '''The order controls which rx ry rz are applied in the transformation matrix.'''
    
    @classmethod
    @property
    def XYZ(cls) -> RotationOrder:
        '''Rotate in X,Y,Z order'''
        ...
    
    @classmethod
    @property
    def XZY(cls) -> RotationOrder:
        '''Rotate in X,Z,Y order'''
        ...
    
    @classmethod
    @property
    def YZX(cls) -> RotationOrder:
        '''Rotate in Y,Z,X order'''
        ...
    
    @classmethod
    @property
    def YXZ(cls) -> RotationOrder:
        '''Rotate in Y,X,Z order'''
        ...
    
    @classmethod
    @property
    def ZXY(cls) -> RotationOrder:
        '''Rotate in Z,X,Y order'''
        ...
    
    @classmethod
    @property
    def ZYX(cls) -> RotationOrder:
        '''Rotate in Z,Y,X order'''
        ...
    
    ...

class VertexFieldDataType:
    '''Vertex field's data type'''
    
    @classmethod
    @property
    def FLOAT(cls) -> VertexFieldDataType:
        '''Type of :py:class:`float`'''
        ...
    
    @classmethod
    @property
    def F_VECTOR2(cls) -> VertexFieldDataType:
        '''Type of :py:class:`aspose.threed.utilities.FVector2`'''
        ...
    
    @classmethod
    @property
    def F_VECTOR3(cls) -> VertexFieldDataType:
        '''Type of :py:class:`aspose.threed.utilities.FVector3`'''
        ...
    
    @classmethod
    @property
    def F_VECTOR4(cls) -> VertexFieldDataType:
        '''Type of :py:class:`aspose.threed.utilities.FVector4`'''
        ...
    
    @classmethod
    @property
    def DOUBLE(cls) -> VertexFieldDataType:
        '''Type of :py:class:`float`'''
        ...
    
    @classmethod
    @property
    def VECTOR2(cls) -> VertexFieldDataType:
        '''Type of :py:class:`aspose.threed.utilities.Vector2`'''
        ...
    
    @classmethod
    @property
    def VECTOR3(cls) -> VertexFieldDataType:
        '''Type of :py:class:`aspose.threed.utilities.Vector3`'''
        ...
    
    @classmethod
    @property
    def VECTOR4(cls) -> VertexFieldDataType:
        '''Type of :py:class:`aspose.threed.utilities.Vector4`'''
        ...
    
    @classmethod
    @property
    def BYTE_VECTOR4(cls) -> VertexFieldDataType:
        '''Type of byte[4], can be used to represent color with less memory consumption.'''
        ...
    
    @classmethod
    @property
    def INT8(cls) -> VertexFieldDataType:
        '''Type of :py:class:`int`'''
        ...
    
    @classmethod
    @property
    def INT16(cls) -> VertexFieldDataType:
        '''Type of :py:class:`int`'''
        ...
    
    @classmethod
    @property
    def INT32(cls) -> VertexFieldDataType:
        '''Type of :py:class:`int`'''
        ...
    
    @classmethod
    @property
    def INT64(cls) -> VertexFieldDataType:
        '''Type of :py:class:`int`'''
        ...
    
    ...

class VertexFieldSemantic:
    '''The semantic of the vertex field'''
    
    @classmethod
    @property
    def POSITION(cls) -> VertexFieldSemantic:
        '''Position data'''
        ...
    
    @classmethod
    @property
    def BINORMAL(cls) -> VertexFieldSemantic:
        '''Binormal vector'''
        ...
    
    @classmethod
    @property
    def NORMAL(cls) -> VertexFieldSemantic:
        '''Normal vector'''
        ...
    
    @classmethod
    @property
    def TANGENT(cls) -> VertexFieldSemantic:
        '''Tangent vector'''
        ...
    
    @classmethod
    @property
    def UV(cls) -> VertexFieldSemantic:
        '''Texture UV coordinate'''
        ...
    
    @classmethod
    @property
    def VERTEX_COLOR(cls) -> VertexFieldSemantic:
        '''Vertex color'''
        ...
    
    @classmethod
    @property
    def VERTEX_CREASE(cls) -> VertexFieldSemantic:
        '''Vertex crease'''
        ...
    
    @classmethod
    @property
    def EDGE_CREASE(cls) -> VertexFieldSemantic:
        '''Edge crease'''
        ...
    
    @classmethod
    @property
    def USER_DATA(cls) -> VertexFieldSemantic:
        '''User data, usually for application-specific purpose'''
        ...
    
    @classmethod
    @property
    def VISIBILITY(cls) -> VertexFieldSemantic:
        '''Visibility for components'''
        ...
    
    @classmethod
    @property
    def SPECULAR(cls) -> VertexFieldSemantic:
        '''Specular colors'''
        ...
    
    @classmethod
    @property
    def WEIGHT(cls) -> VertexFieldSemantic:
        '''Blend weights'''
        ...
    
    ...

