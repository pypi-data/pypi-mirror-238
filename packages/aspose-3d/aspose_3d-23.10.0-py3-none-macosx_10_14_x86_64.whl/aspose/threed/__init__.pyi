"""This is a wrapper module for Aspose.3D .NET assembly"""

from typing import Any

def get_pyinstaller_hook_dirs() -> Any:
  """Function required by PyInstaller. Returns paths to module 
  PyInstaller hooks. Not intended to be called explicitly."""
    ...

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

class A3DObject(INamedObject):
    '''The base class of all Aspose.ThreeD objects, all sub classes will support dynamic properties.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    ...

class AssetInfo(A3DObject):
    '''Information of asset.
    Asset information can be attached to a :py:class:`aspose.threed.Scene`.
    Child :py:class:`aspose.threed.Scene` can have its own :py:class:`aspose.threed.AssetInfo` to override parent's definition.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def creation_time(self) -> Optional[DateTime]:
        ...
    
    @creation_time.setter
    def creation_time(self, value : Optional[DateTime]):
        ...
    
    @property
    def modification_time(self) -> Optional[DateTime]:
        ...
    
    @modification_time.setter
    def modification_time(self, value : Optional[DateTime]):
        ...
    
    @property
    def ambient(self) -> Optional[aspose.threed.utilities.Vector4]:
        '''Gets or Sets the default ambient color of this asset'''
        ...
    
    @ambient.setter
    def ambient(self, value : Optional[aspose.threed.utilities.Vector4]):
        '''Gets or Sets the default ambient color of this asset'''
        ...
    
    @property
    def url(self) -> str:
        '''Gets or Sets the URL of this asset.'''
        ...
    
    @url.setter
    def url(self, value : str):
        '''Gets or Sets the URL of this asset.'''
        ...
    
    @property
    def application_vendor(self) -> str:
        ...
    
    @application_vendor.setter
    def application_vendor(self, value : str):
        ...
    
    @property
    def copyright(self) -> str:
        '''Gets the document's copyright'''
        ...
    
    @copyright.setter
    def copyright(self, value : str):
        '''Sets the document's copyright'''
        ...
    
    @property
    def application_name(self) -> str:
        ...
    
    @application_name.setter
    def application_name(self, value : str):
        ...
    
    @property
    def application_version(self) -> str:
        ...
    
    @application_version.setter
    def application_version(self, value : str):
        ...
    
    @property
    def title(self) -> str:
        '''Gets the title of this asset'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Sets the title of this asset'''
        ...
    
    @property
    def subject(self) -> str:
        '''Gets the subject of this asset'''
        ...
    
    @subject.setter
    def subject(self, value : str):
        '''Sets the subject of this asset'''
        ...
    
    @property
    def author(self) -> str:
        '''Gets the author of this asset'''
        ...
    
    @author.setter
    def author(self, value : str):
        '''Sets the author of this asset'''
        ...
    
    @property
    def keywords(self) -> str:
        '''Gets the keywords of this asset'''
        ...
    
    @keywords.setter
    def keywords(self, value : str):
        '''Sets the keywords of this asset'''
        ...
    
    @property
    def revision(self) -> str:
        '''Gets the revision number of this asset, usually used in version control system.'''
        ...
    
    @revision.setter
    def revision(self, value : str):
        '''Sets the revision number of this asset, usually used in version control system.'''
        ...
    
    @property
    def comment(self) -> str:
        '''Gets the comment of this asset.'''
        ...
    
    @comment.setter
    def comment(self, value : str):
        '''Sets the comment of this asset.'''
        ...
    
    @property
    def unit_name(self) -> str:
        ...
    
    @unit_name.setter
    def unit_name(self, value : str):
        ...
    
    @property
    def unit_scale_factor(self) -> float:
        ...
    
    @unit_scale_factor.setter
    def unit_scale_factor(self, value : float):
        ...
    
    @property
    def coordinated_system(self) -> Optional[aspose.threed.CoordinatedSystem]:
        ...
    
    @coordinated_system.setter
    def coordinated_system(self, value : Optional[aspose.threed.CoordinatedSystem]):
        ...
    
    @property
    def up_vector(self) -> Optional[aspose.threed.Axis]:
        ...
    
    @up_vector.setter
    def up_vector(self, value : Optional[aspose.threed.Axis]):
        ...
    
    ...

class BonePose:
    '''The :py:class:`aspose.threed.BonePose` contains the transformation matrix for a bone node'''
    
    @property
    def node(self) -> aspose.threed.Node:
        '''Gets the scene node, points to a skinned skeleton node'''
        ...
    
    @node.setter
    def node(self, value : aspose.threed.Node):
        '''Sets the scene node, points to a skinned skeleton node'''
        ...
    
    @property
    def matrix(self) -> aspose.threed.utilities.Matrix4:
        '''Gets the transform matrix of the node in current pose.'''
        ...
    
    @matrix.setter
    def matrix(self, value : aspose.threed.utilities.Matrix4):
        '''Sets the transform matrix of the node in current pose.'''
        ...
    
    @property
    def is_local(self) -> bool:
        ...
    
    @is_local.setter
    def is_local(self, value : bool):
        ...
    
    ...

class CustomObject(A3DObject):
    '''Meta data or custom objects used in 3D files are managed by this class.
    All custom properties are saved as dynamic properties.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    ...

class Entity(SceneObject):
    '''The base class of all entities.
    Entity represents a concrete object that attached under a node like :py:class:`aspose.threed.entities.Light`/:py:class:`aspose.threed.entities.Geometry`.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Gets the bounding box of current entity in its object space coordinate system.'''
        ...
    
    def get_entity_renderer_key(self) -> aspose.threed.render.EntityRendererKey:
        '''Gets the key of the entity renderer registered in the renderer'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def parent_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this entity during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this entity during exporting.'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    ...

class ExportException:
    '''Exceptions when Aspose.3D failed to export the scene to file'''
    
    ...

class FileFormat:
    '''File format definition'''
    
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

class FileFormatType:
    '''File format type'''
    
    @property
    def extension(self) -> str:
        '''The extension name of this file format, started with .'''
        ...
    
    @classmethod
    @property
    def MAYA(cls) -> aspose.threed.FileFormatType:
        '''Autodesk Maya format type'''
        ...
    
    @classmethod
    @property
    def FBX(cls) -> aspose.threed.FileFormatType:
        '''FBX file format type'''
        ...
    
    @classmethod
    @property
    def STL(cls) -> aspose.threed.FileFormatType:
        '''STL file format type'''
        ...
    
    @classmethod
    @property
    def WAVEFRONT_OBJ(cls) -> aspose.threed.FileFormatType:
        ...
    
    @classmethod
    @property
    def DISCREET_3DS(cls) -> aspose.threed.FileFormatType:
        ...
    
    @classmethod
    @property
    def COLLADA(cls) -> aspose.threed.FileFormatType:
        '''Khronos Group's Collada file format.'''
        ...
    
    @classmethod
    @property
    def UNIVERSAL_3D(cls) -> aspose.threed.FileFormatType:
        ...
    
    @classmethod
    @property
    def PDF(cls) -> aspose.threed.FileFormatType:
        '''Portable Document Format'''
        ...
    
    @classmethod
    @property
    def GLTF(cls) -> aspose.threed.FileFormatType:
        '''Khronos Group's glTF'''
        ...
    
    @classmethod
    @property
    def DXF(cls) -> aspose.threed.FileFormatType:
        '''AutoCAD DXF'''
        ...
    
    @classmethod
    @property
    def PLY(cls) -> aspose.threed.FileFormatType:
        '''Polygon File Format or Stanford Triangle Format'''
        ...
    
    @classmethod
    @property
    def X(cls) -> aspose.threed.FileFormatType:
        '''DirectX's X File'''
        ...
    
    @classmethod
    @property
    def DRACO(cls) -> aspose.threed.FileFormatType:
        '''Google Draco Mesh'''
        ...
    
    @classmethod
    @property
    def MICROSOFT_3MF(cls) -> aspose.threed.FileFormatType:
        ...
    
    @classmethod
    @property
    def RVM(cls) -> aspose.threed.FileFormatType:
        '''AVEVA Plant Design Management System Model.'''
        ...
    
    @classmethod
    @property
    def ASE(cls) -> aspose.threed.FileFormatType:
        '''3D Studio Max's ASCII Scene Exporter format.'''
        ...
    
    @classmethod
    @property
    def ZIP(cls) -> aspose.threed.FileFormatType:
        '''Zip archive that contains other 3d file format.'''
        ...
    
    @classmethod
    @property
    def USD(cls) -> aspose.threed.FileFormatType:
        '''Universal Scene Description'''
        ...
    
    @classmethod
    @property
    def PCD(cls) -> aspose.threed.FileFormatType:
        '''Point Cloud Data used by Point Cloud Library'''
        ...
    
    @classmethod
    @property
    def XYZ(cls) -> aspose.threed.FileFormatType:
        '''Xyz point cloud file'''
        ...
    
    @classmethod
    @property
    def IFC(cls) -> aspose.threed.FileFormatType:
        '''ISO 16739-1 Industry Foundation Classes data model.'''
        ...
    
    @classmethod
    @property
    def SIEMENS_JT(cls) -> aspose.threed.FileFormatType:
        ...
    
    @classmethod
    @property
    def AMF(cls) -> aspose.threed.FileFormatType:
        '''Additive manufacturing file format'''
        ...
    
    @classmethod
    @property
    def VRML(cls) -> aspose.threed.FileFormatType:
        '''The Virtual Reality Modeling Language'''
        ...
    
    @classmethod
    @property
    def HTML5(cls) -> aspose.threed.FileFormatType:
        '''HTML5 File'''
        ...
    
    @classmethod
    @property
    def ASPOSE_3D_WEB(cls) -> aspose.threed.FileFormatType:
        ...
    
    ...

class GlobalTransform:
    '''Global transform is similar to :py:class:`aspose.threed.Transform` but it's immutable while it represents the final evaluated transformation.
    Right-hand coordinate system is used while evaluating global transform'''
    
    @property
    def translation(self) -> aspose.threed.utilities.Vector3:
        '''Gets the translation'''
        ...
    
    @property
    def scale(self) -> aspose.threed.utilities.Vector3:
        '''Gets the scale'''
        ...
    
    @property
    def euler_angles(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @property
    def rotation(self) -> aspose.threed.utilities.Quaternion:
        '''Gets the rotation represented in quaternion.'''
        ...
    
    @property
    def transform_matrix(self) -> aspose.threed.utilities.Matrix4:
        ...
    
    ...

class INamedObject:
    '''Object that has a name'''
    
    @property
    def name(self) -> str:
        '''Gets the name of the object'''
        ...
    
    ...

class ImageRenderOptions(A3DObject):
    '''Options for :py:func:`aspose.threed.Scene.render` and  :py:func:`aspose.threed.Scene.render`'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def background_color(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @background_color.setter
    def background_color(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def asset_directories(self) -> List[str]:
        ...
    
    @asset_directories.setter
    def asset_directories(self, value : List[str]):
        ...
    
    @property
    def enable_shadows(self) -> bool:
        ...
    
    @enable_shadows.setter
    def enable_shadows(self, value : bool):
        ...
    
    ...

class ImportException:
    '''Exception when Aspose.3D failed to open the specified source'''
    
    ...

class License:
    '''Provides methods to license the component.'''
    
    @overload
    def set_license(self, license_name : str):
        '''Licenses the component.'''
        ...
    
    @overload
    def set_license(self, stream : io.RawIOBase):
        '''Licenses the component.
        
        :param stream: A stream that contains the license.'''
        ...
    
    ...

class Metered:
    '''Provides methods to set metered key.'''
    
    def set_metered_key(self, public_key : str, private_key : str):
        '''Sets metered public and private key.
        If you purchase metered license, when start application, this API should be called, normally, this is enough. However, if always fail to upload consumption data and exceed 24 hours, the license will be set to evaluation status, to avoid such case, you should regularly check the license status, if it is evaluation status, call this API again.
        
        :param public_key: public key
        :param private_key: private key'''
        ...
    
    @staticmethod
    def get_consumption_quantity() -> float:
        '''Gets consumption file size
        
        :returns: consumption quantity'''
        ...
    
    @staticmethod
    def get_consumption_credit() -> float:
        '''Gets consumption credit
        
        :returns: consumption quantity'''
        ...
    
    ...

class Node(SceneObject):
    '''Represents an element in the scene graph.
    A scene graph is a tree of Node objects. The tree management services are self contained in this class.
    Note the Aspose.3D SDK does not test the validity of the constructed scene graph. It is the responsibility of the caller to make sure that it does not generate cyclic graphs in a node hierarchy.
    Besides the tree management, this class defines all the properties required to describe the position of the object in the scene. This information include the basic Translation, Rotation and Scaling properties and the more advanced options for pivots, limits, and IK joints attributes such the stiffness and dampening.
    When it is first created, the Node object is "empty" (i.e: it is an object without any graphical representation that only contains the position information). In this state, it can be used to represent parents in the node tree structure but not much more. The normal use of this type of objects is to add them an entity that will specialize the node (see the "Entity").
    The entity is an object in itself and is connected to the the Node. This also means that the same entity can be shared among multiple nodes. Camera, Light, Mesh, etc... are all entities and they all derived from the base class Entity.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    @overload
    def create_child_node(self) -> aspose.threed.Node:
        '''Creates a child node
        
        :returns: The new child node.'''
        ...
    
    @overload
    def create_child_node(self, node_name : str) -> aspose.threed.Node:
        '''Create a new child node with given node name
        
        :param node_name: The new child node's name
        :returns: The new child node.'''
        ...
    
    @overload
    def create_child_node(self, entity : aspose.threed.Entity) -> aspose.threed.Node:
        '''Create a new child node with given entity attached
        
        :param entity: Default entity attached to the node
        :returns: The new child node.'''
        ...
    
    @overload
    def create_child_node(self, node_name : str, entity : aspose.threed.Entity) -> aspose.threed.Node:
        '''Create a new child node with given node name
        
        :param node_name: The new child node's name
        :param entity: Default entity attached to the node
        :returns: The new child node.'''
        ...
    
    @overload
    def create_child_node(self, node_name : str, entity : aspose.threed.Entity, material : aspose.threed.shading.Material) -> aspose.threed.Node:
        '''Create a new child node with given node name, and attach specified entity and a material
        
        :param node_name: The new child node's name
        :param entity: Default entity attached to the node
        :param material: The material attached to the node
        :returns: The new child node.'''
        ...
    
    @overload
    def get_child(self, index : int) -> aspose.threed.Node:
        '''Gets the child node at specified index.
        
        :param index: Index.
        :returns: The child.'''
        ...
    
    @overload
    def get_child(self, node_name : str) -> aspose.threed.Node:
        '''Gets the child node with the specified name
        
        :param node_name: The child name to find.
        :returns: The child.'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def merge(self, node : aspose.threed.Node):
        '''Detach everything under the node and attach them to current node.'''
        ...
    
    def evaluate_global_transform(self, with_geometric_transform : bool) -> aspose.threed.utilities.Matrix4:
        '''Evaluate the global transform, include the geometric transform or not.
        
        :param with_geometric_transform: Whether the geometric transform is needed.
        :returns: The global transform matrix.'''
        ...
    
    def get_bounding_box(self) -> aspose.threed.utilities.BoundingBox:
        '''Calculate the bounding box of the node'''
        ...
    
    def add_entity(self, entity : aspose.threed.Entity):
        '''Add an entity to the node.
        
        :param entity: The entity to be attached to the node'''
        ...
    
    def add_child_node(self, node : aspose.threed.Node):
        '''Add a child node to this node
        
        :param node: The child node to be attached'''
        ...
    
    def select_single_object(self, path : str) -> any:
        '''Select single object under current node using XPath-like query syntax.'''
        ...
    
    def select_objects(self, path : str) -> List[any]:
        '''Select multiple objects under current node using XPath-like query syntax.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def asset_info(self) -> aspose.threed.AssetInfo:
        ...
    
    @asset_info.setter
    def asset_info(self, value : aspose.threed.AssetInfo):
        ...
    
    @property
    def visible(self) -> bool:
        '''Gets to show the node'''
        ...
    
    @visible.setter
    def visible(self, value : bool):
        '''Sets to show the node'''
        ...
    
    @property
    def child_nodes(self) -> List[aspose.threed.Node]:
        ...
    
    @property
    def entity(self) -> aspose.threed.Entity:
        '''Gets the first entity attached to this node, if sets, will clear other entities.'''
        ...
    
    @entity.setter
    def entity(self, value : aspose.threed.Entity):
        '''Sets the first entity attached to this node, if sets, will clear other entities.'''
        ...
    
    @property
    def excluded(self) -> bool:
        '''Gets whether to exclude this node and all child nodes/entities during exporting.'''
        ...
    
    @excluded.setter
    def excluded(self, value : bool):
        '''Sets whether to exclude this node and all child nodes/entities during exporting.'''
        ...
    
    @property
    def entities(self) -> List[aspose.threed.Entity]:
        '''Gets all node entities.'''
        ...
    
    @property
    def meta_datas(self) -> List[aspose.threed.CustomObject]:
        ...
    
    @property
    def materials(self) -> List[aspose.threed.shading.Material]:
        '''Gets the materials associated with this node.'''
        ...
    
    @property
    def material(self) -> aspose.threed.shading.Material:
        '''Gets the first material associated with this node, if sets, will clear other materials'''
        ...
    
    @material.setter
    def material(self, value : aspose.threed.shading.Material):
        '''Sets the first material associated with this node, if sets, will clear other materials'''
        ...
    
    @property
    def parent_node(self) -> aspose.threed.Node:
        ...
    
    @parent_node.setter
    def parent_node(self, value : aspose.threed.Node):
        ...
    
    @property
    def transform(self) -> aspose.threed.Transform:
        '''Gets the local transform.'''
        ...
    
    @property
    def global_transform(self) -> aspose.threed.GlobalTransform:
        ...
    
    ...

class Pose(A3DObject):
    '''The pose is used to store transformation matrix when the geometry is skinned.
    The pose is a set of :py:class:`aspose.threed.BonePose`, each :py:class:`aspose.threed.BonePose` saves the concrete transformation information of the bone node.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    @overload
    def add_bone_pose(self, node : aspose.threed.Node, matrix : aspose.threed.utilities.Matrix4, local_matrix : bool):
        '''Saves pose transformation matrix for the given bone node.
        
        :param node: Bone Node.
        :param matrix: Transformation matrix.
        :param local_matrix: If set to ``true`` means to use local matrix otherwise means global matrix.'''
        ...
    
    @overload
    def add_bone_pose(self, node : aspose.threed.Node, matrix : aspose.threed.utilities.Matrix4):
        '''Saves pose transformation matrix for the given bone node.
        Global transformation matrix is implied.
        
        :param node: Bone Node.
        :param matrix: Transformation matrix.'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def pose_type(self) -> aspose.threed.PoseType:
        ...
    
    @pose_type.setter
    def pose_type(self, value : aspose.threed.PoseType):
        ...
    
    @property
    def bone_poses(self) -> List[aspose.threed.BonePose]:
        ...
    
    ...

class Property(A3DObject):
    '''Class to hold user-defined properties.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_bind_point(self, anim : aspose.threed.animation.AnimationNode, create : bool) -> aspose.threed.animation.BindPoint:
        '''Gets the property bind point on specified animation instance.
        
        :param anim: On which animation to create the bind point.
        :param create: Create the property bind point if it's not found.
        :returns: The property bind point on specified animation instance'''
        ...
    
    def get_keyframe_sequence(self, anim : aspose.threed.animation.AnimationNode, create : bool) -> aspose.threed.animation.KeyframeSequence:
        '''Gets the keyframe sequence on specified animation instance.
        
        :param anim: On which animation to create the keyframe sequence.
        :param create: Create the keyframe sequence if it's not found.
        :returns: The keyframe sequence on specified animation instance'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def value(self) -> any:
        '''Gets the value.'''
        ...
    
    @value.setter
    def value(self, value : any):
        '''Sets the value.'''
        ...
    
    @property
    def value_type(self) -> Type:
        ...
    
    ...

class PropertyCollection:
    '''The collection of properties'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    def find_property(self, property : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property: Property name.
        :returns: The property.'''
        ...
    
    def get(self, property : str) -> any:
        ...
    
    @property
    def count(self) -> int:
        '''Gets the count of declared properties.'''
        ...
    
    def __getitem__(self, key : int) -> aspose.threed.Property:
        ...
    
    ...

class Scene(SceneObject):
    '''A scene is a top-level object that contains the nodes, geometries, materials, textures, animation, poses, sub-scenes and etc.
    Scene can have sub-scenes, acts as multiple-document support in files like collada/blender/fbx
    Node hierarchy can be accessed through :py:attr:`aspose.threed.Scene.root_node`:py:attr:`aspose.threed.Scene.library` is used to keep a reference of unattached objects during serialization(like meta data or custom objects) so it can be used as a library.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    @overload
    def open(self, stream : io.RawIOBase):
        '''Opens the scene from given stream
        
        :param stream: Input stream, user is responsible for closing the stream.'''
        ...
    
    @overload
    def open(self, file_name : str, options : aspose.threed.formats.LoadOptions):
        '''Opens the scene from given path using specified file format.
        
        :param file_name: File name.
        :param options: More detailed configuration to open the stream.'''
        ...
    
    @overload
    def open(self, file_name : str):
        '''Opens the scene from given path
        
        :param file_name: File name.'''
        ...
    
    @overload
    def save(self, stream : io.RawIOBase, format : aspose.threed.FileFormat):
        '''Saves the scene to stream using specified file format.
        
        :param stream: Input stream, user is responsible for closing the stream.
        :param format: Format.'''
        ...
    
    @overload
    def save(self, stream : io.RawIOBase, options : aspose.threed.formats.SaveOptions):
        '''Saves the scene to stream using specified file format.
        
        :param stream: Input stream, user is responsible for closing the stream.
        :param options: More detailed configuration to save the stream.'''
        ...
    
    @overload
    def save(self, file_name : str):
        '''Saves the scene to specified path using specified file format.
        
        :param file_name: File name.'''
        ...
    
    @overload
    def save(self, file_name : str, format : aspose.threed.FileFormat):
        '''Saves the scene to specified path using specified file format.
        
        :param file_name: File name.
        :param format: Format.'''
        ...
    
    @overload
    def save(self, file_name : str, options : aspose.threed.formats.SaveOptions):
        '''Saves the scene to specified path using specified file format.
        
        :param file_name: File name.
        :param options: More detailed configuration to save the stream.'''
        ...
    
    @overload
    def render(self, camera : aspose.threed.entities.Camera, file_name : str):
        '''Render the scene into external file from given camera's perspective.
        The default output size is 1024x768 and output format is png
        
        :param camera: From which camera's perspective to render the scene
        :param file_name: The file name of output file'''
        ...
    
    @overload
    def render(self, camera : aspose.threed.entities.Camera, file_name : str, size : aspose.threed.utilities.Vector2, format : str):
        '''Render the scene into external file from given camera's perspective.
        
        :param camera: From which camera's perspective to render the scene
        :param file_name: The file name of output file
        :param size: The size of final rendered image
        :param format: The image format of the output file'''
        ...
    
    @overload
    def render(self, camera : aspose.threed.entities.Camera, file_name : str, size : aspose.threed.utilities.Vector2, format : str, options : aspose.threed.ImageRenderOptions):
        '''Render the scene into external file from given camera's perspective.
        
        :param camera: From which camera's perspective to render the scene
        :param file_name: The file name of output file
        :param size: The size of final rendered image
        :param format: The image format of the output file
        :param options: The option to customize some internal settings.'''
        ...
    
    @overload
    def render(self, camera : aspose.threed.entities.Camera, bitmap : aspose.threed.render.TextureData):
        '''Render the scene into bitmap from given camera's perspective.
        
        :param camera: From which camera's perspective to render the scene
        :param bitmap: Target of the rendered result'''
        ...
    
    @overload
    def render(self, camera : aspose.threed.entities.Camera, bitmap : aspose.threed.render.TextureData, options : aspose.threed.ImageRenderOptions):
        '''Render the scene into bitmap from given camera's perspective.
        
        :param camera: From which camera's perspective to render the scene
        :param bitmap: Target of the rendered result
        :param options: The option to customize some internal settings.'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def get_animation_clip(self, name : str) -> aspose.threed.animation.AnimationClip:
        '''Gets a named :py:class:`aspose.threed.animation.AnimationClip`
        
        :param name: The :py:class:`aspose.threed.animation.AnimationClip`'s name to look up
        :returns: Returned AnimationClip'''
        ...
    
    def clear(self):
        '''Clears the scene content and restores the default settings.'''
        ...
    
    def create_animation_clip(self, name : str) -> aspose.threed.animation.AnimationClip:
        '''A shorthand function to create and register the :py:class:`aspose.threed.animation.AnimationClip`
        The first :py:class:`aspose.threed.animation.AnimationClip` will be assigned to the :py:attr:`aspose.threed.Scene.current_animation_clip`
        
        :param name: Animation clip's name'''
        ...
    
    @staticmethod
    def from_file(file_name : str) -> aspose.threed.Scene:
        '''Opens the scene from given path
        
        :param file_name: File name.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    @property
    def sub_scenes(self) -> List[aspose.threed.Scene]:
        ...
    
    @property
    def library(self) -> List[aspose.threed.A3DObject]:
        '''Objects that not directly used in scene hierarchy can be defined in Library.
        This is useful when you're using sub-scenes and put reusable components under sub-scenes.'''
        ...
    
    @property
    def animation_clips(self) -> List[aspose.threed.animation.AnimationClip]:
        ...
    
    @property
    def current_animation_clip(self) -> aspose.threed.animation.AnimationClip:
        ...
    
    @current_animation_clip.setter
    def current_animation_clip(self, value : aspose.threed.animation.AnimationClip):
        ...
    
    @property
    def asset_info(self) -> aspose.threed.AssetInfo:
        ...
    
    @asset_info.setter
    def asset_info(self, value : aspose.threed.AssetInfo):
        ...
    
    @property
    def poses(self) -> List[aspose.threed.Pose]:
        '''Gets all :py:class:`aspose.threed.Pose` used in this scene.'''
        ...
    
    @property
    def root_node(self) -> aspose.threed.Node:
        ...
    
    ...

class SceneObject(A3DObject):
    '''The root class of objects that will be stored inside a scene.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def scene(self) -> aspose.threed.Scene:
        '''Gets the scene that this object belongs to'''
        ...
    
    ...

class Transform(A3DObject):
    '''A transform contains information that allow access to object's translate/scale/rotation or transform matrix at minimum cost
    This is used by local transform.'''
    
    @overload
    def remove_property(self, property : aspose.threed.Property) -> bool:
        '''Removes a dynamic property.
        
        :param property: Which property to remove
        :returns: true if the property is successfully removed'''
        ...
    
    @overload
    def remove_property(self, property : str) -> bool:
        '''Remove the specified property identified by name'''
        ...
    
    def get_property(self, property : str) -> any:
        '''Get the value of specified property
        
        :param property: Property name
        :returns: The value of the found property'''
        ...
    
    def set_property(self, property : str, value : any):
        '''Sets the value of specified property
        
        :param property: Property name
        :param value: The value of the property'''
        ...
    
    def find_property(self, property_name : str) -> aspose.threed.Property:
        '''Finds the property.
        It can be a dynamic property (Created by CreateDynamicProperty/SetProperty)
        or native property(Identified by its name)
        
        :param property_name: Property name.
        :returns: The property.'''
        ...
    
    def set_geometric_translation(self, x : float, y : float, z : float) -> aspose.threed.Transform:
        '''Sets the geometric translation.
        Geometric transformation only affects the entities attached and leave the child nodes unaffected.
        It will be merged as local transformation when you export the geometric transformation to file types that does not support it.'''
        ...
    
    def set_geometric_scaling(self, sx : float, sy : float, sz : float) -> aspose.threed.Transform:
        '''Sets the geometric scaling.
        Geometric transformation only affects the entities attached and leave the child nodes unaffected.
        It will be merged as local transformation when you export the geometric transformation to file types that does not support it.'''
        ...
    
    def set_geometric_rotation(self, rx : float, ry : float, rz : float) -> aspose.threed.Transform:
        '''Sets the geometric Euler rotation(measured in degree).
        Geometric transformation only affects the entities attached and leave the child nodes unaffected.
        It will be merged as local transformation when you export the geometric transformation to file types that does not support it.'''
        ...
    
    def set_translation(self, tx : float, ty : float, tz : float) -> aspose.threed.Transform:
        '''Sets the translation of current transform.'''
        ...
    
    def set_scale(self, sx : float, sy : float, sz : float) -> aspose.threed.Transform:
        '''Sets the scale of current transform.'''
        ...
    
    def set_euler_angles(self, rx : float, ry : float, rz : float) -> aspose.threed.Transform:
        '''Sets the Euler angles in degrees of current transform.'''
        ...
    
    def set_rotation(self, rw : float, rx : float, ry : float, rz : float) -> aspose.threed.Transform:
        '''Sets the rotation(as quaternion components) of current transform.'''
        ...
    
    def set_pre_rotation(self, rx : float, ry : float, rz : float) -> aspose.threed.Transform:
        '''Sets the pre-rotation represented in degree'''
        ...
    
    def set_post_rotation(self, rx : float, ry : float, rz : float) -> aspose.threed.Transform:
        '''Sets the post-rotation represented in degree'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    @property
    def properties(self) -> aspose.threed.PropertyCollection:
        '''Gets the collection of all properties.'''
        ...
    
    @property
    def geometric_translation(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @geometric_translation.setter
    def geometric_translation(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def geometric_scaling(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @geometric_scaling.setter
    def geometric_scaling(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def geometric_rotation(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @geometric_rotation.setter
    def geometric_rotation(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def translation(self) -> aspose.threed.utilities.Vector3:
        '''Gets the translation'''
        ...
    
    @translation.setter
    def translation(self, value : aspose.threed.utilities.Vector3):
        '''Sets the translation'''
        ...
    
    @property
    def scale(self) -> aspose.threed.utilities.Vector3:
        '''Gets the scale'''
        ...
    
    @scale.setter
    def scale(self, value : aspose.threed.utilities.Vector3):
        '''Sets the scale'''
        ...
    
    @property
    def pre_rotation(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @pre_rotation.setter
    def pre_rotation(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def post_rotation(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @post_rotation.setter
    def post_rotation(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def euler_angles(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @euler_angles.setter
    def euler_angles(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def rotation(self) -> aspose.threed.utilities.Quaternion:
        '''Gets the rotation represented in quaternion.'''
        ...
    
    @rotation.setter
    def rotation(self, value : aspose.threed.utilities.Quaternion):
        '''Sets the rotation represented in quaternion.'''
        ...
    
    @property
    def transform_matrix(self) -> aspose.threed.utilities.Matrix4:
        ...
    
    @transform_matrix.setter
    def transform_matrix(self, value : aspose.threed.utilities.Matrix4):
        ...
    
    ...

class TrialException:
    '''This is raised in Scene.Open/Scene.Save when no licenses are applied.
    You can turn off this exception by setting SuppressTrialException to true.'''
    
    @classmethod
    @property
    def suppress_trial_exception(cls) -> bool:
        ...
    
    @classmethod
    @suppress_trial_exception.setter
    def suppress_trial_exception(cls, value : bool):
        ...
    
    ...

class Axis:
    '''The coordinate axis.'''
    
    @classmethod
    @property
    def X_AXIS(cls) -> Axis:
        '''The X axis.'''
        ...
    
    @classmethod
    @property
    def Y_AXIS(cls) -> Axis:
        '''The Y axis.'''
        ...
    
    @classmethod
    @property
    def Z_AXIS(cls) -> Axis:
        '''The Z axis.'''
        ...
    
    ...

class CoordinatedSystem:
    '''The left handed or right handed coordinate system.'''
    
    @classmethod
    @property
    def RIGHT_HANDED(cls) -> CoordinatedSystem:
        '''The right handed.'''
        ...
    
    @classmethod
    @property
    def LEFT_HANDED(cls) -> CoordinatedSystem:
        '''The left handed.'''
        ...
    
    ...

class FileContentType:
    '''File content type'''
    
    @classmethod
    @property
    def BINARY(cls) -> FileContentType:
        '''Binary format type, such as binary FBX, binary STL'''
        ...
    
    @classmethod
    @property
    def ASCII(cls) -> FileContentType:
        '''ASCII format type, such as ASCII FBX, ASCII STL'''
        ...
    
    ...

class PoseType:
    '''Pose type.'''
    
    @classmethod
    @property
    def BIND_POSE(cls) -> PoseType:
        '''The bind pose.'''
        ...
    
    @classmethod
    @property
    def SNAPSHOT(cls) -> PoseType:
        '''The rest pose, means it's a snapshot of the bind pose.'''
        ...
    
    ...

class PropertyFlags:
    '''Property's flags'''
    
    @classmethod
    @property
    def NONE(cls) -> PropertyFlags:
        '''The property has no flags'''
        ...
    
    @classmethod
    @property
    def NOT_SERIALIZABLE(cls) -> PropertyFlags:
        '''This property is not serializable'''
        ...
    
    @classmethod
    @property
    def USER_DEFINED(cls) -> PropertyFlags:
        '''This is a user defined property'''
        ...
    
    @classmethod
    @property
    def ANIMATABLE(cls) -> PropertyFlags:
        '''The property is animatable'''
        ...
    
    @classmethod
    @property
    def ANIMATED(cls) -> PropertyFlags:
        '''The property is animated'''
        ...
    
    @classmethod
    @property
    def HIDDEN(cls) -> PropertyFlags:
        '''The property is marked as hidden.'''
        ...
    
    ...

