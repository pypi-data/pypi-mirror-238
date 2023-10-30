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

class A3dwSaveOptions(SaveOptions):
    '''Save options for A3DW format.'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def export_textures(self) -> bool:
        ...
    
    @export_textures.setter
    def export_textures(self, value : bool):
        ...
    
    @property
    def export_meta_data(self) -> bool:
        ...
    
    @export_meta_data.setter
    def export_meta_data(self, value : bool):
        ...
    
    @property
    def meta_data_prefix(self) -> str:
        ...
    
    @meta_data_prefix.setter
    def meta_data_prefix(self, value : str):
        ...
    
    ...

class AmfSaveOptions(SaveOptions):
    '''Save options for AMF'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def export_textures(self) -> bool:
        ...
    
    @export_textures.setter
    def export_textures(self, value : bool):
        ...
    
    @property
    def enable_compression(self) -> bool:
        ...
    
    @enable_compression.setter
    def enable_compression(self, value : bool):
        ...
    
    ...

class ColladaSaveOptions(SaveOptions):
    '''Save options for collada'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def export_textures(self) -> bool:
        ...
    
    @export_textures.setter
    def export_textures(self, value : bool):
        ...
    
    @property
    def indented(self) -> bool:
        '''Gets whether the exported XML document is indented.'''
        ...
    
    @indented.setter
    def indented(self, value : bool):
        '''Sets whether the exported XML document is indented.'''
        ...
    
    @property
    def transform_style(self) -> aspose.threed.formats.ColladaTransformStyle:
        ...
    
    @transform_style.setter
    def transform_style(self, value : aspose.threed.formats.ColladaTransformStyle):
        ...
    
    ...

class Discreet3dsLoadOptions(LoadOptions):
    '''Load options for 3DS file.'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def gamma_corrected_color(self) -> bool:
        ...
    
    @gamma_corrected_color.setter
    def gamma_corrected_color(self, value : bool):
        ...
    
    @property
    def flip_coordinate_system(self) -> bool:
        ...
    
    @flip_coordinate_system.setter
    def flip_coordinate_system(self, value : bool):
        ...
    
    @property
    def apply_animation_transform(self) -> bool:
        ...
    
    @apply_animation_transform.setter
    def apply_animation_transform(self, value : bool):
        ...
    
    ...

class Discreet3dsSaveOptions(SaveOptions):
    '''Save options for 3DS file.'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def export_textures(self) -> bool:
        ...
    
    @export_textures.setter
    def export_textures(self, value : bool):
        ...
    
    @property
    def export_light(self) -> bool:
        ...
    
    @export_light.setter
    def export_light(self, value : bool):
        ...
    
    @property
    def export_camera(self) -> bool:
        ...
    
    @export_camera.setter
    def export_camera(self, value : bool):
        ...
    
    @property
    def duplicated_name_separator(self) -> str:
        ...
    
    @duplicated_name_separator.setter
    def duplicated_name_separator(self, value : str):
        ...
    
    @property
    def duplicated_name_counter_base(self) -> int:
        ...
    
    @duplicated_name_counter_base.setter
    def duplicated_name_counter_base(self, value : int):
        ...
    
    @property
    def duplicated_name_counter_format(self) -> str:
        ...
    
    @duplicated_name_counter_format.setter
    def duplicated_name_counter_format(self, value : str):
        ...
    
    @property
    def master_scale(self) -> float:
        ...
    
    @master_scale.setter
    def master_scale(self, value : float):
        ...
    
    @property
    def gamma_corrected_color(self) -> bool:
        ...
    
    @gamma_corrected_color.setter
    def gamma_corrected_color(self, value : bool):
        ...
    
    @property
    def flip_coordinate_system(self) -> bool:
        ...
    
    @flip_coordinate_system.setter
    def flip_coordinate_system(self, value : bool):
        ...
    
    @property
    def high_precise_color(self) -> bool:
        ...
    
    @high_precise_color.setter
    def high_precise_color(self, value : bool):
        ...
    
    ...

class DracoFormat(aspose.threed.FileFormat):
    '''Google Draco format'''
    
    @overload
    @staticmethod
    def detect(stream : io.RawIOBasefile_name : str) -> aspose.threed.FileFormat:
        '''Detect the file format from data stream, file name is optional for guessing types that has no magic header.'''
        ...
    
    @overload
    @staticmethod
    def detect(file_name : str) -> aspose.threed.FileFormat:
        '''Detect the file format from file name, file must be readable so Aspose.3D can detect the file format through file header.'''
        ...
    
    @overload
    def decode(self, file_name : str) -> aspose.threed.entities.Geometry:
        '''Decode the point cloud or mesh from specified file name
        
        :param file_name: The file name contains the drc file
        :returns: A :py:class:`aspose.threed.entities.Mesh` or :py:class:`aspose.threed.entities.PointCloud` instance depends on the file content'''
        ...
    
    @overload
    def decode(self, data : bytes) -> aspose.threed.entities.Geometry:
        '''Decode the point cloud or mesh from memory data
        
        :param data: The raw drc bytes
        :returns: A :py:class:`aspose.threed.entities.Mesh` or :py:class:`aspose.threed.entities.PointCloud` instance depends on the content'''
        ...
    
    @overload
    def encode(self, entity : aspose.threed.Entity, stream : io.RawIOBase, options : aspose.threed.formats.DracoSaveOptions):
        '''Encode the entity to specified stream
        
        :param entity: The entity to be encoded
        :param stream: The stream that encoded data will be written to
        :param options: Extra options for encoding the point cloud'''
        ...
    
    @overload
    def encode(self, entity : aspose.threed.Entity, file_name : str, options : aspose.threed.formats.DracoSaveOptions):
        '''Encode the entity to specified file
        
        :param entity: The entity to be encoded
        :param file_name: The file name to be written
        :param options: Extra options for encoding the point cloud'''
        ...
    
    @overload
    def encode(self, entity : aspose.threed.Entity, options : aspose.threed.formats.DracoSaveOptions) -> bytes:
        '''Encode the entity to Draco raw data
        
        :param entity: The entity to be encoded
        :param options: Extra options for encoding the point cloud
        :returns: The encoded draco data represented in bytes'''
        ...
    
    @staticmethod
    def get_format_by_extension(extension_name : str) -> aspose.threed.FileFormat:
        '''Gets the preferred file format from the file extension name
        The extension name should starts with a dot('.').
        
        :returns: Instance of :py:class:`aspose.threed.FileFormat`, otherwise null returned.'''
        ...
    
    def create_load_options(self) -> aspose.threed.formats.LoadOptions:
        '''Create a default load options for this file format'''
        ...
    
    def create_save_options(self) -> aspose.threed.formats.SaveOptions:
        '''Create a default save options for this file format'''
        ...
    
    @property
    def version(self) -> Version:
        '''Gets file format version'''
        ...
    
    @property
    def can_export(self) -> bool:
        ...
    
    @property
    def can_import(self) -> bool:
        ...
    
    @property
    def extension(self) -> str:
        '''Gets the extension name of this type.'''
        ...
    
    @property
    def extensions(self) -> List[str]:
        '''Gets the extension names of this type.'''
        ...
    
    @property
    def content_type(self) -> aspose.threed.FileContentType:
        ...
    
    @property
    def file_format_type(self) -> aspose.threed.FileFormatType:
        ...
    
    @classmethod
    @property
    def FBX6100ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 6.1.0 version'''
        ...
    
    @classmethod
    @property
    def FBX6100_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7200ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.2.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7200_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7300ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.3.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7300_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7400ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.4.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7400_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7500ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.5.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7500_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7600ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.6.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7600_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7700ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.7.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7700_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def MAYA_ASCII(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def MAYA_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def STL_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def STLASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII STL file format'''
        ...
    
    @classmethod
    @property
    def WAVEFRONT_OBJ(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def DISCREET_3DS(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def COLLADA(cls) -> aspose.threed.FileFormat:
        '''Collada file format'''
        ...
    
    @classmethod
    @property
    def UNIVERSAL_3D(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def GLTF(cls) -> aspose.threed.FileFormat:
        '''Khronos Group's glTF'''
        ...
    
    @classmethod
    @property
    def GLTF2(cls) -> aspose.threed.FileFormat:
        '''Khronos Group's glTF version 2.0'''
        ...
    
    @classmethod
    @property
    def GLTF_BINARY(cls) -> aspose.threed.FileFormat:
        '''Khronos Group's glTF in Binary format'''
        ...
    
    @classmethod
    @property
    def GLTF2_BINARY(cls) -> aspose.threed.FileFormat:
        '''Khronos Group's glTF version 2.0'''
        ...
    
    @classmethod
    @property
    def PDF(cls) -> aspose.threed.formats.PdfFormat:
        '''Adobe's Portable Document Format'''
        ...
    
    @classmethod
    @property
    def DXF(cls) -> aspose.threed.FileFormat:
        '''AutoCAD DXF'''
        ...
    
    @classmethod
    @property
    def PLY(cls) -> aspose.threed.formats.PlyFormat:
        '''Polygon File Format or Stanford Triangle Format'''
        ...
    
    @classmethod
    @property
    def X_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def X_TEXT(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def DRACO(cls) -> aspose.threed.formats.DracoFormat:
        '''Google Draco Mesh'''
        ...
    
    @classmethod
    @property
    def MICROSOFT_3MF(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def RVM_TEXT(cls) -> aspose.threed.formats.RvmFormat:
        ...
    
    @classmethod
    @property
    def RVM_BINARY(cls) -> aspose.threed.formats.RvmFormat:
        ...
    
    @classmethod
    @property
    def ASE(cls) -> aspose.threed.FileFormat:
        '''3D Studio Max's ASCII Scene Exporter format.'''
        ...
    
    @classmethod
    @property
    def IFC(cls) -> aspose.threed.FileFormat:
        '''ISO 16739-1 Industry Foundation Classes data model.'''
        ...
    
    @classmethod
    @property
    def SIEMENS_JT8(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def SIEMENS_JT9(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def AMF(cls) -> aspose.threed.FileFormat:
        '''Additive manufacturing file format'''
        ...
    
    @classmethod
    @property
    def VRML(cls) -> aspose.threed.FileFormat:
        '''The Virtual Reality Modeling Language'''
        ...
    
    @classmethod
    @property
    def ASPOSE_3D_WEB(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def HTML5(cls) -> aspose.threed.FileFormat:
        '''HTML5 File'''
        ...
    
    @classmethod
    @property
    def ZIP(cls) -> aspose.threed.FileFormat:
        '''Zip archive that contains other 3d file format.'''
        ...
    
    @classmethod
    @property
    def USD(cls) -> aspose.threed.FileFormat:
        '''Universal Scene Description'''
        ...
    
    @classmethod
    @property
    def USDZ(cls) -> aspose.threed.FileFormat:
        '''Compressed Universal Scene Description'''
        ...
    
    @classmethod
    @property
    def XYZ(cls) -> aspose.threed.FileFormat:
        '''Xyz point cloud file'''
        ...
    
    @classmethod
    @property
    def PCD(cls) -> aspose.threed.FileFormat:
        '''PCL Point Cloud Data file in ASCII mode'''
        ...
    
    @classmethod
    @property
    def PCD_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    ...

class DracoSaveOptions(SaveOptions):
    '''Save options for Google draco files'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def export_textures(self) -> bool:
        ...
    
    @export_textures.setter
    def export_textures(self, value : bool):
        ...
    
    @property
    def position_bits(self) -> int:
        ...
    
    @position_bits.setter
    def position_bits(self, value : int):
        ...
    
    @property
    def texture_coordinate_bits(self) -> int:
        ...
    
    @texture_coordinate_bits.setter
    def texture_coordinate_bits(self, value : int):
        ...
    
    @property
    def color_bits(self) -> int:
        ...
    
    @color_bits.setter
    def color_bits(self, value : int):
        ...
    
    @property
    def normal_bits(self) -> int:
        ...
    
    @normal_bits.setter
    def normal_bits(self, value : int):
        ...
    
    @property
    def compression_level(self) -> aspose.threed.formats.DracoCompressionLevel:
        ...
    
    @compression_level.setter
    def compression_level(self, value : aspose.threed.formats.DracoCompressionLevel):
        ...
    
    @property
    def apply_unit_scale(self) -> bool:
        ...
    
    @apply_unit_scale.setter
    def apply_unit_scale(self, value : bool):
        ...
    
    @property
    def point_cloud(self) -> bool:
        ...
    
    @point_cloud.setter
    def point_cloud(self, value : bool):
        ...
    
    ...

class FbxLoadOptions(LoadOptions):
    '''Load options for Fbx format.'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def keep_builtin_global_settings(self) -> bool:
        ...
    
    @keep_builtin_global_settings.setter
    def keep_builtin_global_settings(self, value : bool):
        ...
    
    ...

class FbxSaveOptions(SaveOptions):
    '''Save options for Fbx file.'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def export_textures(self) -> bool:
        ...
    
    @export_textures.setter
    def export_textures(self, value : bool):
        ...
    
    @property
    def reuse_primitive_mesh(self) -> bool:
        ...
    
    @reuse_primitive_mesh.setter
    def reuse_primitive_mesh(self, value : bool):
        ...
    
    @property
    def enable_compression(self) -> bool:
        ...
    
    @enable_compression.setter
    def enable_compression(self, value : bool):
        ...
    
    @property
    def fold_repeated_curve_data(self) -> Optional[bool]:
        ...
    
    @fold_repeated_curve_data.setter
    def fold_repeated_curve_data(self, value : Optional[bool]):
        ...
    
    @property
    def export_legacy_material_properties(self) -> bool:
        ...
    
    @export_legacy_material_properties.setter
    def export_legacy_material_properties(self, value : bool):
        ...
    
    @property
    def video_for_texture(self) -> bool:
        ...
    
    @video_for_texture.setter
    def video_for_texture(self, value : bool):
        ...
    
    @property
    def embed_textures(self) -> bool:
        ...
    
    @embed_textures.setter
    def embed_textures(self, value : bool):
        ...
    
    @property
    def generate_vertex_element_material(self) -> bool:
        ...
    
    @generate_vertex_element_material.setter
    def generate_vertex_element_material(self, value : bool):
        ...
    
    ...

class GltfLoadOptions(LoadOptions):
    '''Load options for glTF format'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def flip_tex_coord_v(self) -> bool:
        ...
    
    @flip_tex_coord_v.setter
    def flip_tex_coord_v(self, value : bool):
        ...
    
    ...

class GltfSaveOptions(SaveOptions):
    '''Save options for glTF format.'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def export_textures(self) -> bool:
        ...
    
    @export_textures.setter
    def export_textures(self, value : bool):
        ...
    
    @property
    def pretty_print(self) -> bool:
        ...
    
    @pretty_print.setter
    def pretty_print(self, value : bool):
        ...
    
    @property
    def fallback_normal(self) -> Optional[aspose.threed.utilities.Vector3]:
        ...
    
    @fallback_normal.setter
    def fallback_normal(self, value : Optional[aspose.threed.utilities.Vector3]):
        ...
    
    @property
    def embed_assets(self) -> bool:
        ...
    
    @embed_assets.setter
    def embed_assets(self, value : bool):
        ...
    
    @property
    def image_format(self) -> aspose.threed.formats.GltfEmbeddedImageFormat:
        ...
    
    @image_format.setter
    def image_format(self, value : aspose.threed.formats.GltfEmbeddedImageFormat):
        ...
    
    @property
    def use_common_materials(self) -> bool:
        ...
    
    @use_common_materials.setter
    def use_common_materials(self, value : bool):
        ...
    
    @property
    def external_draco_encoder(self) -> str:
        ...
    
    @external_draco_encoder.setter
    def external_draco_encoder(self, value : str):
        ...
    
    @property
    def flip_tex_coord_v(self) -> bool:
        ...
    
    @flip_tex_coord_v.setter
    def flip_tex_coord_v(self, value : bool):
        ...
    
    @property
    def buffer_file(self) -> str:
        ...
    
    @buffer_file.setter
    def buffer_file(self, value : str):
        ...
    
    @property
    def save_extras(self) -> bool:
        ...
    
    @save_extras.setter
    def save_extras(self, value : bool):
        ...
    
    @property
    def apply_unit_scale(self) -> bool:
        ...
    
    @apply_unit_scale.setter
    def apply_unit_scale(self, value : bool):
        ...
    
    @property
    def draco_compression(self) -> bool:
        ...
    
    @draco_compression.setter
    def draco_compression(self, value : bool):
        ...
    
    ...

class Html5SaveOptions(SaveOptions):
    '''Save options for HTML5'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def export_textures(self) -> bool:
        ...
    
    @export_textures.setter
    def export_textures(self, value : bool):
        ...
    
    @property
    def show_grid(self) -> bool:
        ...
    
    @show_grid.setter
    def show_grid(self, value : bool):
        ...
    
    @property
    def show_rulers(self) -> bool:
        ...
    
    @show_rulers.setter
    def show_rulers(self, value : bool):
        ...
    
    @property
    def show_ui(self) -> bool:
        ...
    
    @show_ui.setter
    def show_ui(self, value : bool):
        ...
    
    @property
    def orientation_box(self) -> bool:
        ...
    
    @orientation_box.setter
    def orientation_box(self, value : bool):
        ...
    
    @property
    def up_vector(self) -> str:
        ...
    
    @up_vector.setter
    def up_vector(self, value : str):
        ...
    
    @property
    def far_plane(self) -> float:
        ...
    
    @far_plane.setter
    def far_plane(self, value : float):
        ...
    
    @property
    def near_plane(self) -> float:
        ...
    
    @near_plane.setter
    def near_plane(self, value : float):
        ...
    
    @property
    def look_at(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @look_at.setter
    def look_at(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def camera_position(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @camera_position.setter
    def camera_position(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def field_of_view(self) -> float:
        ...
    
    @field_of_view.setter
    def field_of_view(self, value : float):
        ...
    
    ...

class IOConfig:
    '''IO config for serialization/deserialization.
    User can specify detailed configurations like dependency look-up path
    Or format-related configs here'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    ...

class LoadOptions(IOConfig):
    '''The base class to configure options in file loading for different types'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    ...

class ObjLoadOptions(LoadOptions):
    '''Load options for wavefront obj'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def flip_coordinate_system(self) -> bool:
        ...
    
    @flip_coordinate_system.setter
    def flip_coordinate_system(self, value : bool):
        ...
    
    @property
    def enable_materials(self) -> bool:
        ...
    
    @enable_materials.setter
    def enable_materials(self, value : bool):
        ...
    
    @property
    def scale(self) -> float:
        '''Scales on x/y/z axis, default value is 1.0'''
        ...
    
    @scale.setter
    def scale(self, value : float):
        '''Scales on x/y/z axis, default value is 1.0'''
        ...
    
    @property
    def normalize_normal(self) -> bool:
        ...
    
    @normalize_normal.setter
    def normalize_normal(self, value : bool):
        ...
    
    ...

class ObjSaveOptions(SaveOptions):
    '''Save options for wavefront obj file'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def export_textures(self) -> bool:
        ...
    
    @export_textures.setter
    def export_textures(self, value : bool):
        ...
    
    @property
    def apply_unit_scale(self) -> bool:
        ...
    
    @apply_unit_scale.setter
    def apply_unit_scale(self, value : bool):
        ...
    
    @property
    def point_cloud(self) -> bool:
        ...
    
    @point_cloud.setter
    def point_cloud(self, value : bool):
        ...
    
    @property
    def verbose(self) -> bool:
        '''Gets whether generate comments for each section'''
        ...
    
    @verbose.setter
    def verbose(self, value : bool):
        '''Sets whether generate comments for each section'''
        ...
    
    @property
    def serialize_w(self) -> bool:
        ...
    
    @serialize_w.setter
    def serialize_w(self, value : bool):
        ...
    
    @property
    def enable_materials(self) -> bool:
        ...
    
    @enable_materials.setter
    def enable_materials(self, value : bool):
        ...
    
    @property
    def flip_coordinate_system(self) -> bool:
        ...
    
    @flip_coordinate_system.setter
    def flip_coordinate_system(self, value : bool):
        ...
    
    ...

class PdfFormat(aspose.threed.FileFormat):
    '''Adobe's Portable Document Format'''
    
    @overload
    @staticmethod
    def detect(stream : io.RawIOBasefile_name : str) -> aspose.threed.FileFormat:
        '''Detect the file format from data stream, file name is optional for guessing types that has no magic header.'''
        ...
    
    @overload
    @staticmethod
    def detect(file_name : str) -> aspose.threed.FileFormat:
        '''Detect the file format from file name, file must be readable so Aspose.3D can detect the file format through file header.'''
        ...
    
    @overload
    def extract(self, file_name : str, password : bytes) -> List[bytes]:
        '''Extract raw 3D content from PDF file.'''
        ...
    
    @overload
    def extract(self, stream : io.RawIOBase, password : bytes) -> List[bytes]:
        '''Extract raw 3D content from PDF stream.'''
        ...
    
    @overload
    def extract_scene(self, file_name : str) -> List[aspose.threed.Scene]:
        '''Extract 3D scenes from PDF file.'''
        ...
    
    @overload
    def extract_scene(self, file_name : str, password : bytes) -> List[aspose.threed.Scene]:
        '''Extract 3D scenes from PDF file.'''
        ...
    
    @overload
    def extract_scene(self, stream : io.RawIOBase, password : bytes) -> List[aspose.threed.Scene]:
        '''Extract raw 3D content from PDF stream.'''
        ...
    
    @staticmethod
    def get_format_by_extension(extension_name : str) -> aspose.threed.FileFormat:
        '''Gets the preferred file format from the file extension name
        The extension name should starts with a dot('.').
        
        :returns: Instance of :py:class:`aspose.threed.FileFormat`, otherwise null returned.'''
        ...
    
    def create_load_options(self) -> aspose.threed.formats.LoadOptions:
        '''Create a default load options for this file format'''
        ...
    
    def create_save_options(self) -> aspose.threed.formats.SaveOptions:
        '''Create a default save options for this file format'''
        ...
    
    @property
    def version(self) -> Version:
        '''Gets file format version'''
        ...
    
    @property
    def can_export(self) -> bool:
        ...
    
    @property
    def can_import(self) -> bool:
        ...
    
    @property
    def extension(self) -> str:
        '''Gets the extension name of this type.'''
        ...
    
    @property
    def extensions(self) -> List[str]:
        '''Gets the extension names of this type.'''
        ...
    
    @property
    def content_type(self) -> aspose.threed.FileContentType:
        ...
    
    @property
    def file_format_type(self) -> aspose.threed.FileFormatType:
        ...
    
    @classmethod
    @property
    def FBX6100ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 6.1.0 version'''
        ...
    
    @classmethod
    @property
    def FBX6100_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7200ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.2.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7200_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7300ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.3.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7300_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7400ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.4.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7400_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7500ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.5.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7500_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7600ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.6.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7600_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7700ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.7.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7700_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def MAYA_ASCII(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def MAYA_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def STL_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def STLASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII STL file format'''
        ...
    
    @classmethod
    @property
    def WAVEFRONT_OBJ(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def DISCREET_3DS(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def COLLADA(cls) -> aspose.threed.FileFormat:
        '''Collada file format'''
        ...
    
    @classmethod
    @property
    def UNIVERSAL_3D(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def GLTF(cls) -> aspose.threed.FileFormat:
        '''Khronos Group's glTF'''
        ...
    
    @classmethod
    @property
    def GLTF2(cls) -> aspose.threed.FileFormat:
        '''Khronos Group's glTF version 2.0'''
        ...
    
    @classmethod
    @property
    def GLTF_BINARY(cls) -> aspose.threed.FileFormat:
        '''Khronos Group's glTF in Binary format'''
        ...
    
    @classmethod
    @property
    def GLTF2_BINARY(cls) -> aspose.threed.FileFormat:
        '''Khronos Group's glTF version 2.0'''
        ...
    
    @classmethod
    @property
    def PDF(cls) -> aspose.threed.formats.PdfFormat:
        '''Adobe's Portable Document Format'''
        ...
    
    @classmethod
    @property
    def DXF(cls) -> aspose.threed.FileFormat:
        '''AutoCAD DXF'''
        ...
    
    @classmethod
    @property
    def PLY(cls) -> aspose.threed.formats.PlyFormat:
        '''Polygon File Format or Stanford Triangle Format'''
        ...
    
    @classmethod
    @property
    def X_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def X_TEXT(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def DRACO(cls) -> aspose.threed.formats.DracoFormat:
        '''Google Draco Mesh'''
        ...
    
    @classmethod
    @property
    def MICROSOFT_3MF(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def RVM_TEXT(cls) -> aspose.threed.formats.RvmFormat:
        ...
    
    @classmethod
    @property
    def RVM_BINARY(cls) -> aspose.threed.formats.RvmFormat:
        ...
    
    @classmethod
    @property
    def ASE(cls) -> aspose.threed.FileFormat:
        '''3D Studio Max's ASCII Scene Exporter format.'''
        ...
    
    @classmethod
    @property
    def IFC(cls) -> aspose.threed.FileFormat:
        '''ISO 16739-1 Industry Foundation Classes data model.'''
        ...
    
    @classmethod
    @property
    def SIEMENS_JT8(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def SIEMENS_JT9(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def AMF(cls) -> aspose.threed.FileFormat:
        '''Additive manufacturing file format'''
        ...
    
    @classmethod
    @property
    def VRML(cls) -> aspose.threed.FileFormat:
        '''The Virtual Reality Modeling Language'''
        ...
    
    @classmethod
    @property
    def ASPOSE_3D_WEB(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def HTML5(cls) -> aspose.threed.FileFormat:
        '''HTML5 File'''
        ...
    
    @classmethod
    @property
    def ZIP(cls) -> aspose.threed.FileFormat:
        '''Zip archive that contains other 3d file format.'''
        ...
    
    @classmethod
    @property
    def USD(cls) -> aspose.threed.FileFormat:
        '''Universal Scene Description'''
        ...
    
    @classmethod
    @property
    def USDZ(cls) -> aspose.threed.FileFormat:
        '''Compressed Universal Scene Description'''
        ...
    
    @classmethod
    @property
    def XYZ(cls) -> aspose.threed.FileFormat:
        '''Xyz point cloud file'''
        ...
    
    @classmethod
    @property
    def PCD(cls) -> aspose.threed.FileFormat:
        '''PCL Point Cloud Data file in ASCII mode'''
        ...
    
    @classmethod
    @property
    def PCD_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    ...

class PdfLoadOptions(LoadOptions):
    '''Options for PDF loading'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def password(self) -> bytes:
        '''The password to unlock the encrypted PDF file.'''
        ...
    
    @password.setter
    def password(self, value : bytes):
        '''The password to unlock the encrypted PDF file.'''
        ...
    
    ...

class PdfSaveOptions(SaveOptions):
    '''The save options in PDF exporting.'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def export_textures(self) -> bool:
        ...
    
    @export_textures.setter
    def export_textures(self, value : bool):
        ...
    
    @property
    def render_mode(self) -> aspose.threed.formats.PdfRenderMode:
        ...
    
    @render_mode.setter
    def render_mode(self, value : aspose.threed.formats.PdfRenderMode):
        ...
    
    @property
    def lighting_scheme(self) -> aspose.threed.formats.PdfLightingScheme:
        ...
    
    @lighting_scheme.setter
    def lighting_scheme(self, value : aspose.threed.formats.PdfLightingScheme):
        ...
    
    @property
    def background_color(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @background_color.setter
    def background_color(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def face_color(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @face_color.setter
    def face_color(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def auxiliary_color(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @auxiliary_color.setter
    def auxiliary_color(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def flip_coordinate_system(self) -> bool:
        ...
    
    @flip_coordinate_system.setter
    def flip_coordinate_system(self, value : bool):
        ...
    
    @property
    def embed_textures(self) -> bool:
        ...
    
    @embed_textures.setter
    def embed_textures(self, value : bool):
        ...
    
    ...

class PlyFormat(aspose.threed.FileFormat):
    '''The PLY format.'''
    
    @overload
    @staticmethod
    def detect(stream : io.RawIOBasefile_name : str) -> aspose.threed.FileFormat:
        '''Detect the file format from data stream, file name is optional for guessing types that has no magic header.'''
        ...
    
    @overload
    @staticmethod
    def detect(file_name : str) -> aspose.threed.FileFormat:
        '''Detect the file format from file name, file must be readable so Aspose.3D can detect the file format through file header.'''
        ...
    
    @overload
    def encode(self, entity : aspose.threed.Entity, stream : io.RawIOBase):
        '''Encode the entity and save the result into the stream.
        
        :param entity: The entity to encode
        :param stream: The stream to write to, this method will not close this stream'''
        ...
    
    @overload
    def encode(self, entity : aspose.threed.Entity, stream : io.RawIOBase, opt : aspose.threed.formats.PlySaveOptions):
        '''Encode the entity and save the result into the stream.
        
        :param entity: The entity to encode
        :param stream: The stream to write to, this method will not close this stream
        :param opt: Save options'''
        ...
    
    @overload
    def encode(self, entity : aspose.threed.Entity, file_name : str):
        '''Encode the entity and save the result into an external file.
        
        :param entity: The entity to encode
        :param file_name: The file to write to'''
        ...
    
    @overload
    def encode(self, entity : aspose.threed.Entity, file_name : str, opt : aspose.threed.formats.PlySaveOptions):
        '''Encode the entity and save the result into an external file.
        
        :param entity: The entity to encode
        :param file_name: The file to write to
        :param opt: Save options'''
        ...
    
    @overload
    def decode(self, file_name : str) -> aspose.threed.entities.Geometry:
        '''Decode a point cloud or mesh from the specified stream.
        
        :param file_name: The input stream
        :returns: A :py:class:`aspose.threed.entities.Mesh` or :py:class:`aspose.threed.entities.PointCloud` instance'''
        ...
    
    @overload
    def decode(self, file_name : str, opt : aspose.threed.formats.PlyLoadOptions) -> aspose.threed.entities.Geometry:
        '''Decode a point cloud or mesh from the specified stream.
        
        :param file_name: The input stream
        :param opt: The load option of PLY format
        :returns: A :py:class:`aspose.threed.entities.Mesh` or :py:class:`aspose.threed.entities.PointCloud` instance'''
        ...
    
    @overload
    def decode(self, stream : io.RawIOBase) -> aspose.threed.entities.Geometry:
        '''Decode a point cloud or mesh from the specified stream.
        
        :param stream: The input stream
        :returns: A :py:class:`aspose.threed.entities.Mesh` or :py:class:`aspose.threed.entities.PointCloud` instance'''
        ...
    
    @overload
    def decode(self, stream : io.RawIOBase, opt : aspose.threed.formats.PlyLoadOptions) -> aspose.threed.entities.Geometry:
        '''Decode a point cloud or mesh from the specified stream.
        
        :param stream: The input stream
        :param opt: The load option of PLY format
        :returns: A :py:class:`aspose.threed.entities.Mesh` or :py:class:`aspose.threed.entities.PointCloud` instance'''
        ...
    
    @staticmethod
    def get_format_by_extension(extension_name : str) -> aspose.threed.FileFormat:
        '''Gets the preferred file format from the file extension name
        The extension name should starts with a dot('.').
        
        :returns: Instance of :py:class:`aspose.threed.FileFormat`, otherwise null returned.'''
        ...
    
    def create_load_options(self) -> aspose.threed.formats.LoadOptions:
        '''Create a default load options for this file format'''
        ...
    
    def create_save_options(self) -> aspose.threed.formats.SaveOptions:
        '''Create a default save options for this file format'''
        ...
    
    @property
    def version(self) -> Version:
        '''Gets file format version'''
        ...
    
    @property
    def can_export(self) -> bool:
        ...
    
    @property
    def can_import(self) -> bool:
        ...
    
    @property
    def extension(self) -> str:
        '''Gets the extension name of this type.'''
        ...
    
    @property
    def extensions(self) -> List[str]:
        '''Gets the extension names of this type.'''
        ...
    
    @property
    def content_type(self) -> aspose.threed.FileContentType:
        ...
    
    @property
    def file_format_type(self) -> aspose.threed.FileFormatType:
        ...
    
    @classmethod
    @property
    def FBX6100ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 6.1.0 version'''
        ...
    
    @classmethod
    @property
    def FBX6100_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7200ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.2.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7200_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7300ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.3.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7300_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7400ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.4.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7400_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7500ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.5.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7500_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7600ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.6.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7600_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7700ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.7.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7700_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def MAYA_ASCII(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def MAYA_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def STL_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def STLASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII STL file format'''
        ...
    
    @classmethod
    @property
    def WAVEFRONT_OBJ(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def DISCREET_3DS(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def COLLADA(cls) -> aspose.threed.FileFormat:
        '''Collada file format'''
        ...
    
    @classmethod
    @property
    def UNIVERSAL_3D(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def GLTF(cls) -> aspose.threed.FileFormat:
        '''Khronos Group's glTF'''
        ...
    
    @classmethod
    @property
    def GLTF2(cls) -> aspose.threed.FileFormat:
        '''Khronos Group's glTF version 2.0'''
        ...
    
    @classmethod
    @property
    def GLTF_BINARY(cls) -> aspose.threed.FileFormat:
        '''Khronos Group's glTF in Binary format'''
        ...
    
    @classmethod
    @property
    def GLTF2_BINARY(cls) -> aspose.threed.FileFormat:
        '''Khronos Group's glTF version 2.0'''
        ...
    
    @classmethod
    @property
    def PDF(cls) -> aspose.threed.formats.PdfFormat:
        '''Adobe's Portable Document Format'''
        ...
    
    @classmethod
    @property
    def DXF(cls) -> aspose.threed.FileFormat:
        '''AutoCAD DXF'''
        ...
    
    @classmethod
    @property
    def PLY(cls) -> aspose.threed.formats.PlyFormat:
        '''Polygon File Format or Stanford Triangle Format'''
        ...
    
    @classmethod
    @property
    def X_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def X_TEXT(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def DRACO(cls) -> aspose.threed.formats.DracoFormat:
        '''Google Draco Mesh'''
        ...
    
    @classmethod
    @property
    def MICROSOFT_3MF(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def RVM_TEXT(cls) -> aspose.threed.formats.RvmFormat:
        ...
    
    @classmethod
    @property
    def RVM_BINARY(cls) -> aspose.threed.formats.RvmFormat:
        ...
    
    @classmethod
    @property
    def ASE(cls) -> aspose.threed.FileFormat:
        '''3D Studio Max's ASCII Scene Exporter format.'''
        ...
    
    @classmethod
    @property
    def IFC(cls) -> aspose.threed.FileFormat:
        '''ISO 16739-1 Industry Foundation Classes data model.'''
        ...
    
    @classmethod
    @property
    def SIEMENS_JT8(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def SIEMENS_JT9(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def AMF(cls) -> aspose.threed.FileFormat:
        '''Additive manufacturing file format'''
        ...
    
    @classmethod
    @property
    def VRML(cls) -> aspose.threed.FileFormat:
        '''The Virtual Reality Modeling Language'''
        ...
    
    @classmethod
    @property
    def ASPOSE_3D_WEB(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def HTML5(cls) -> aspose.threed.FileFormat:
        '''HTML5 File'''
        ...
    
    @classmethod
    @property
    def ZIP(cls) -> aspose.threed.FileFormat:
        '''Zip archive that contains other 3d file format.'''
        ...
    
    @classmethod
    @property
    def USD(cls) -> aspose.threed.FileFormat:
        '''Universal Scene Description'''
        ...
    
    @classmethod
    @property
    def USDZ(cls) -> aspose.threed.FileFormat:
        '''Compressed Universal Scene Description'''
        ...
    
    @classmethod
    @property
    def XYZ(cls) -> aspose.threed.FileFormat:
        '''Xyz point cloud file'''
        ...
    
    @classmethod
    @property
    def PCD(cls) -> aspose.threed.FileFormat:
        '''PCL Point Cloud Data file in ASCII mode'''
        ...
    
    @classmethod
    @property
    def PCD_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    ...

class PlyLoadOptions(LoadOptions):
    '''Load options for PLY files'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def flip_coordinate_system(self) -> bool:
        ...
    
    @flip_coordinate_system.setter
    def flip_coordinate_system(self, value : bool):
        ...
    
    ...

class PlySaveOptions(SaveOptions):
    '''Save options for exporting scene as PLY file.'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def export_textures(self) -> bool:
        ...
    
    @export_textures.setter
    def export_textures(self, value : bool):
        ...
    
    @property
    def point_cloud(self) -> bool:
        ...
    
    @point_cloud.setter
    def point_cloud(self, value : bool):
        ...
    
    @property
    def flip_coordinate(self) -> bool:
        ...
    
    @flip_coordinate.setter
    def flip_coordinate(self, value : bool):
        ...
    
    @property
    def vertex_element(self) -> str:
        ...
    
    @vertex_element.setter
    def vertex_element(self, value : str):
        ...
    
    @property
    def face_element(self) -> str:
        ...
    
    @face_element.setter
    def face_element(self, value : str):
        ...
    
    @property
    def face_property(self) -> str:
        ...
    
    @face_property.setter
    def face_property(self, value : str):
        ...
    
    ...

class RvmFormat(aspose.threed.FileFormat):
    '''The RVM Format'''
    
    @overload
    @staticmethod
    def detect(stream : io.RawIOBasefile_name : str) -> aspose.threed.FileFormat:
        '''Detect the file format from data stream, file name is optional for guessing types that has no magic header.'''
        ...
    
    @overload
    @staticmethod
    def detect(file_name : str) -> aspose.threed.FileFormat:
        '''Detect the file format from file name, file must be readable so Aspose.3D can detect the file format through file header.'''
        ...
    
    @overload
    def load_attributes(self, scene : aspose.threed.Scene, file_name : str, prefix : str):
        '''Load the attributes from specified file name
        
        :param scene: The scene where the attributes will be applied to
        :param file_name: The file's name that contains the attributes
        :param prefix: The prefix of the attributes that used to avoid conflict of names, default value is "rvm:"'''
        ...
    
    @overload
    def load_attributes(self, scene : aspose.threed.Scene, stream : io.RawIOBase, prefix : str):
        '''Load the attributes from specified stream
        
        :param scene: The scene where the attributes will be applied to
        :param stream: The stream that contains the attributes
        :param prefix: The prefix of the attributes that used to avoid conflict of names, default value is "rvm:"'''
        ...
    
    @staticmethod
    def get_format_by_extension(extension_name : str) -> aspose.threed.FileFormat:
        '''Gets the preferred file format from the file extension name
        The extension name should starts with a dot('.').
        
        :returns: Instance of :py:class:`aspose.threed.FileFormat`, otherwise null returned.'''
        ...
    
    def create_load_options(self) -> aspose.threed.formats.LoadOptions:
        '''Create a default load options for this file format'''
        ...
    
    def create_save_options(self) -> aspose.threed.formats.SaveOptions:
        '''Create a default save options for this file format'''
        ...
    
    @property
    def version(self) -> Version:
        '''Gets file format version'''
        ...
    
    @property
    def can_export(self) -> bool:
        ...
    
    @property
    def can_import(self) -> bool:
        ...
    
    @property
    def extension(self) -> str:
        '''Gets the extension name of this type.'''
        ...
    
    @property
    def extensions(self) -> List[str]:
        '''Gets the extension names of this type.'''
        ...
    
    @property
    def content_type(self) -> aspose.threed.FileContentType:
        ...
    
    @property
    def file_format_type(self) -> aspose.threed.FileFormatType:
        ...
    
    @classmethod
    @property
    def FBX6100ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 6.1.0 version'''
        ...
    
    @classmethod
    @property
    def FBX6100_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7200ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.2.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7200_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7300ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.3.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7300_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7400ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.4.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7400_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7500ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.5.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7500_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7600ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.6.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7600_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def FBX7700ASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII FBX file format, with 7.7.0 version'''
        ...
    
    @classmethod
    @property
    def FBX7700_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def MAYA_ASCII(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def MAYA_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def STL_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def STLASCII(cls) -> aspose.threed.FileFormat:
        '''ASCII STL file format'''
        ...
    
    @classmethod
    @property
    def WAVEFRONT_OBJ(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def DISCREET_3DS(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def COLLADA(cls) -> aspose.threed.FileFormat:
        '''Collada file format'''
        ...
    
    @classmethod
    @property
    def UNIVERSAL_3D(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def GLTF(cls) -> aspose.threed.FileFormat:
        '''Khronos Group's glTF'''
        ...
    
    @classmethod
    @property
    def GLTF2(cls) -> aspose.threed.FileFormat:
        '''Khronos Group's glTF version 2.0'''
        ...
    
    @classmethod
    @property
    def GLTF_BINARY(cls) -> aspose.threed.FileFormat:
        '''Khronos Group's glTF in Binary format'''
        ...
    
    @classmethod
    @property
    def GLTF2_BINARY(cls) -> aspose.threed.FileFormat:
        '''Khronos Group's glTF version 2.0'''
        ...
    
    @classmethod
    @property
    def PDF(cls) -> aspose.threed.formats.PdfFormat:
        '''Adobe's Portable Document Format'''
        ...
    
    @classmethod
    @property
    def DXF(cls) -> aspose.threed.FileFormat:
        '''AutoCAD DXF'''
        ...
    
    @classmethod
    @property
    def PLY(cls) -> aspose.threed.formats.PlyFormat:
        '''Polygon File Format or Stanford Triangle Format'''
        ...
    
    @classmethod
    @property
    def X_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def X_TEXT(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def DRACO(cls) -> aspose.threed.formats.DracoFormat:
        '''Google Draco Mesh'''
        ...
    
    @classmethod
    @property
    def MICROSOFT_3MF(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def RVM_TEXT(cls) -> aspose.threed.formats.RvmFormat:
        ...
    
    @classmethod
    @property
    def RVM_BINARY(cls) -> aspose.threed.formats.RvmFormat:
        ...
    
    @classmethod
    @property
    def ASE(cls) -> aspose.threed.FileFormat:
        '''3D Studio Max's ASCII Scene Exporter format.'''
        ...
    
    @classmethod
    @property
    def IFC(cls) -> aspose.threed.FileFormat:
        '''ISO 16739-1 Industry Foundation Classes data model.'''
        ...
    
    @classmethod
    @property
    def SIEMENS_JT8(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def SIEMENS_JT9(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def AMF(cls) -> aspose.threed.FileFormat:
        '''Additive manufacturing file format'''
        ...
    
    @classmethod
    @property
    def VRML(cls) -> aspose.threed.FileFormat:
        '''The Virtual Reality Modeling Language'''
        ...
    
    @classmethod
    @property
    def ASPOSE_3D_WEB(cls) -> aspose.threed.FileFormat:
        ...
    
    @classmethod
    @property
    def HTML5(cls) -> aspose.threed.FileFormat:
        '''HTML5 File'''
        ...
    
    @classmethod
    @property
    def ZIP(cls) -> aspose.threed.FileFormat:
        '''Zip archive that contains other 3d file format.'''
        ...
    
    @classmethod
    @property
    def USD(cls) -> aspose.threed.FileFormat:
        '''Universal Scene Description'''
        ...
    
    @classmethod
    @property
    def USDZ(cls) -> aspose.threed.FileFormat:
        '''Compressed Universal Scene Description'''
        ...
    
    @classmethod
    @property
    def XYZ(cls) -> aspose.threed.FileFormat:
        '''Xyz point cloud file'''
        ...
    
    @classmethod
    @property
    def PCD(cls) -> aspose.threed.FileFormat:
        '''PCL Point Cloud Data file in ASCII mode'''
        ...
    
    @classmethod
    @property
    def PCD_BINARY(cls) -> aspose.threed.FileFormat:
        ...
    
    ...

class RvmLoadOptions(LoadOptions):
    '''Load options for AVEVA Plant Design Management System's RVM file.'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def generate_materials(self) -> bool:
        ...
    
    @generate_materials.setter
    def generate_materials(self, value : bool):
        ...
    
    @property
    def cylinder_radial_segments(self) -> int:
        ...
    
    @cylinder_radial_segments.setter
    def cylinder_radial_segments(self, value : int):
        ...
    
    @property
    def dish_longitude_segments(self) -> int:
        ...
    
    @dish_longitude_segments.setter
    def dish_longitude_segments(self, value : int):
        ...
    
    @property
    def dish_latitude_segments(self) -> int:
        ...
    
    @dish_latitude_segments.setter
    def dish_latitude_segments(self, value : int):
        ...
    
    @property
    def torus_tubular_segments(self) -> int:
        ...
    
    @torus_tubular_segments.setter
    def torus_tubular_segments(self, value : int):
        ...
    
    @property
    def rectangular_torus_segments(self) -> int:
        ...
    
    @rectangular_torus_segments.setter
    def rectangular_torus_segments(self, value : int):
        ...
    
    @property
    def center_scene(self) -> bool:
        ...
    
    @center_scene.setter
    def center_scene(self, value : bool):
        ...
    
    @property
    def attribute_prefix(self) -> str:
        ...
    
    @attribute_prefix.setter
    def attribute_prefix(self, value : str):
        ...
    
    @property
    def lookup_attributes(self) -> bool:
        ...
    
    @lookup_attributes.setter
    def lookup_attributes(self, value : bool):
        ...
    
    ...

class RvmSaveOptions(SaveOptions):
    '''Save options for Aveva PDMS RVM file.'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def export_textures(self) -> bool:
        ...
    
    @export_textures.setter
    def export_textures(self, value : bool):
        ...
    
    @property
    def file_note(self) -> str:
        ...
    
    @file_note.setter
    def file_note(self, value : str):
        ...
    
    @property
    def author(self) -> str:
        '''Author information, default value is '3d@aspose''''
        ...
    
    @author.setter
    def author(self, value : str):
        '''Author information, default value is '3d@aspose''''
        ...
    
    @property
    def creation_time(self) -> str:
        ...
    
    @creation_time.setter
    def creation_time(self, value : str):
        ...
    
    @property
    def attribute_prefix(self) -> str:
        ...
    
    @attribute_prefix.setter
    def attribute_prefix(self, value : str):
        ...
    
    @property
    def attribute_list_file(self) -> str:
        ...
    
    @attribute_list_file.setter
    def attribute_list_file(self, value : str):
        ...
    
    @property
    def export_attributes(self) -> bool:
        ...
    
    @export_attributes.setter
    def export_attributes(self, value : bool):
        ...
    
    ...

class SaveOptions(IOConfig):
    '''The base class to configure options in file saving for different types'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def export_textures(self) -> bool:
        ...
    
    @export_textures.setter
    def export_textures(self, value : bool):
        ...
    
    ...

class StlLoadOptions(LoadOptions):
    '''Load options for STL'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def flip_coordinate_system(self) -> bool:
        ...
    
    @flip_coordinate_system.setter
    def flip_coordinate_system(self, value : bool):
        ...
    
    @property
    def recalculate_normal(self) -> bool:
        ...
    
    @recalculate_normal.setter
    def recalculate_normal(self, value : bool):
        ...
    
    ...

class StlSaveOptions(SaveOptions):
    '''Save options for STL'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def export_textures(self) -> bool:
        ...
    
    @export_textures.setter
    def export_textures(self, value : bool):
        ...
    
    @property
    def flip_coordinate_system(self) -> bool:
        ...
    
    @flip_coordinate_system.setter
    def flip_coordinate_system(self, value : bool):
        ...
    
    ...

class U3dLoadOptions(LoadOptions):
    '''Load options for universal 3d'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def flip_coordinate_system(self) -> bool:
        ...
    
    @flip_coordinate_system.setter
    def flip_coordinate_system(self, value : bool):
        ...
    
    ...

class U3dSaveOptions(SaveOptions):
    '''Save options for universal 3d'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def export_textures(self) -> bool:
        ...
    
    @export_textures.setter
    def export_textures(self, value : bool):
        ...
    
    @property
    def flip_coordinate_system(self) -> bool:
        ...
    
    @flip_coordinate_system.setter
    def flip_coordinate_system(self, value : bool):
        ...
    
    @property
    def mesh_compression(self) -> bool:
        ...
    
    @mesh_compression.setter
    def mesh_compression(self, value : bool):
        ...
    
    @property
    def export_normals(self) -> bool:
        ...
    
    @export_normals.setter
    def export_normals(self, value : bool):
        ...
    
    @property
    def export_texture_coordinates(self) -> bool:
        ...
    
    @export_texture_coordinates.setter
    def export_texture_coordinates(self, value : bool):
        ...
    
    @property
    def export_vertex_diffuse(self) -> bool:
        ...
    
    @export_vertex_diffuse.setter
    def export_vertex_diffuse(self, value : bool):
        ...
    
    @property
    def export_vertex_specular(self) -> bool:
        ...
    
    @export_vertex_specular.setter
    def export_vertex_specular(self, value : bool):
        ...
    
    @property
    def embed_textures(self) -> bool:
        ...
    
    @embed_textures.setter
    def embed_textures(self, value : bool):
        ...
    
    ...

class UsdSaveOptions(SaveOptions):
    '''Save options for USD/USDZ formats.'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def export_textures(self) -> bool:
        ...
    
    @export_textures.setter
    def export_textures(self, value : bool):
        ...
    
    @property
    def primitive_to_mesh(self) -> bool:
        ...
    
    @primitive_to_mesh.setter
    def primitive_to_mesh(self, value : bool):
        ...
    
    @property
    def export_meta_data(self) -> bool:
        ...
    
    @export_meta_data.setter
    def export_meta_data(self, value : bool):
        ...
    
    ...

class XLoadOptions(LoadOptions):
    '''The Load options for DirectX X files.'''
    
    @property
    def file_format(self) -> aspose.threed.FileFormat:
        ...
    
    @property
    def encoding(self) -> System.Text.Encoding:
        '''Gets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @encoding.setter
    def encoding(self, value : System.Text.Encoding):
        '''Sets the default encoding for text-based files.
        Default value is null which means the importer/exporter will decide which encoding to use.'''
        ...
    
    @property
    def file_system(self) -> aspose.threed.utilities.FileSystem:
        ...
    
    @file_system.setter
    def file_system(self, value : aspose.threed.utilities.FileSystem):
        ...
    
    @property
    def lookup_paths(self) -> List[str]:
        ...
    
    @lookup_paths.setter
    def lookup_paths(self, value : List[str]):
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    @property
    def flip_coordinate_system(self) -> bool:
        ...
    
    @flip_coordinate_system.setter
    def flip_coordinate_system(self, value : bool):
        ...
    
    ...

class ColladaTransformStyle:
    '''The node's transformation style of node'''
    
    @classmethod
    @property
    def COMPONENTS(cls) -> ColladaTransformStyle:
        '''Export the node's transformation as rotate/scale/translate'''
        ...
    
    @classmethod
    @property
    def MATRIX(cls) -> ColladaTransformStyle:
        '''Export the node's transfromation as matrix'''
        ...
    
    ...

class DracoCompressionLevel:
    '''Compression level for draco file'''
    
    @classmethod
    @property
    def NO_COMPRESSION(cls) -> DracoCompressionLevel:
        '''No compression, this will result in the minimum encoding time.'''
        ...
    
    @classmethod
    @property
    def FAST(cls) -> DracoCompressionLevel:
        '''Encoder will perform a compression as quickly as possible.'''
        ...
    
    @classmethod
    @property
    def STANDARD(cls) -> DracoCompressionLevel:
        '''Standard mode, with good compression and speed.'''
        ...
    
    @classmethod
    @property
    def OPTIMAL(cls) -> DracoCompressionLevel:
        '''Encoder will compress the scene optimally, which may takes longer time to finish.'''
        ...
    
    ...

class GltfEmbeddedImageFormat:
    '''How glTF exporter will embed the textures during the exporting.'''
    
    @classmethod
    @property
    def NO_CHANGE(cls) -> GltfEmbeddedImageFormat:
        '''Do not convert the image and keep it as it is.'''
        ...
    
    @classmethod
    @property
    def JPEG(cls) -> GltfEmbeddedImageFormat:
        '''All non-supported images formats will be converted to jpeg if possible.'''
        ...
    
    @classmethod
    @property
    def PNG(cls) -> GltfEmbeddedImageFormat:
        '''All non-supported images formats will be converted to png if possible.'''
        ...
    
    ...

class PdfLightingScheme:
    '''LightingScheme specifies the lighting to apply to 3D artwork.'''
    
    @classmethod
    @property
    def ARTWORK(cls) -> PdfLightingScheme:
        '''Uses the lights defined in the scene'''
        ...
    
    @classmethod
    @property
    def NONE(cls) -> PdfLightingScheme:
        '''No lights are used.'''
        ...
    
    @classmethod
    @property
    def WHITE(cls) -> PdfLightingScheme:
        '''Three blue-grey infinite lights, no ambient term'''
        ...
    
    @classmethod
    @property
    def DAY(cls) -> PdfLightingScheme:
        '''Three light-grey infinite lights, no ambient term'''
        ...
    
    @classmethod
    @property
    def NIGHT(cls) -> PdfLightingScheme:
        '''One yellow, one aqua, and one blue infinite light, no ambient term'''
        ...
    
    @classmethod
    @property
    def HARD(cls) -> PdfLightingScheme:
        '''Three grey infinite lights, moderate ambient term'''
        ...
    
    @classmethod
    @property
    def PRIMARY(cls) -> PdfLightingScheme:
        '''One red, one green, and one blue infinite light, no ambient term'''
        ...
    
    @classmethod
    @property
    def BLUE(cls) -> PdfLightingScheme:
        '''Three blue infinite lights, no ambient term'''
        ...
    
    @classmethod
    @property
    def RED(cls) -> PdfLightingScheme:
        '''Three red infinite lights, no ambient term'''
        ...
    
    @classmethod
    @property
    def CUBE(cls) -> PdfLightingScheme:
        '''Six grey infinite lights aligned with the major axes, no ambient term'''
        ...
    
    @classmethod
    @property
    def CAD(cls) -> PdfLightingScheme:
        '''Three grey infinite lights and one light attached to the camera, no ambient term'''
        ...
    
    @classmethod
    @property
    def HEADLAMP(cls) -> PdfLightingScheme:
        '''Single infinite light attached to the camera, low ambient term'''
        ...
    
    ...

class PdfRenderMode:
    '''Render mode specifies the style in which the 3D artwork is rendered.'''
    
    @classmethod
    @property
    def SOLID(cls) -> PdfRenderMode:
        '''Displays textured and lit geometric shapes.'''
        ...
    
    @classmethod
    @property
    def SOLID_WIREFRAME(cls) -> PdfRenderMode:
        '''Displays textured and lit geometric shapes (triangles) with single color edges on top of them.'''
        ...
    
    @classmethod
    @property
    def TRANSPARENT(cls) -> PdfRenderMode:
        '''Displays textured and lit geometric shapes (triangles) with an added level of transparency.'''
        ...
    
    @classmethod
    @property
    def TRANSPARENT_WIREFRAME(cls) -> PdfRenderMode:
        '''Displays textured and lit geometric shapes (triangles) with an added level of transparency, with single color opaque edges on top of it.'''
        ...
    
    @classmethod
    @property
    def BOUNDING_BOX(cls) -> PdfRenderMode:
        '''Displays the bounding box edges of each node, aligned with the axes of the local coordinate space for that node.'''
        ...
    
    @classmethod
    @property
    def TRANSPARENT_BOUNDING_BOX(cls) -> PdfRenderMode:
        '''Displays bounding boxes faces of each node, aligned with the axes of the local coordinate space for that node, with an added level of transparency.'''
        ...
    
    @classmethod
    @property
    def TRANSPARENT_BOUNDING_BOX_OUTLINE(cls) -> PdfRenderMode:
        '''Displays bounding boxes edges and faces of each node, aligned with the axes of the local coordinate space for that node, with an added level of transparency.'''
        ...
    
    @classmethod
    @property
    def WIREFRAME(cls) -> PdfRenderMode:
        '''Displays only edges in a single color.'''
        ...
    
    @classmethod
    @property
    def SHADED_WIREFRAME(cls) -> PdfRenderMode:
        '''Displays only edges, though interpolates their color between their two vertices and applies lighting.'''
        ...
    
    @classmethod
    @property
    def HIDDEN_WIREFRAME(cls) -> PdfRenderMode:
        '''Displays edges in a single color, though removes back-facing and obscured edges.'''
        ...
    
    @classmethod
    @property
    def VERTICES(cls) -> PdfRenderMode:
        '''Displays only vertices in a single color.'''
        ...
    
    @classmethod
    @property
    def SHADED_VERTICES(cls) -> PdfRenderMode:
        '''Displays only vertices, though uses their vertex color and applies lighting.'''
        ...
    
    @classmethod
    @property
    def ILLUSTRATION(cls) -> PdfRenderMode:
        '''Displays silhouette edges with surfaces, removes obscured lines.'''
        ...
    
    @classmethod
    @property
    def SOLID_OUTLINE(cls) -> PdfRenderMode:
        '''Displays silhouette edges with lit and textured surfaces, removes obscured lines.'''
        ...
    
    @classmethod
    @property
    def SHADED_ILLUSTRATION(cls) -> PdfRenderMode:
        '''Displays silhouette edges with lit and textured surfaces and an additional emissive term to remove poorly lit areas of the artwork.'''
        ...
    
    ...

