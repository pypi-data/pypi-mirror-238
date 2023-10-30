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

class LambertMaterial(Material):
    '''Material for lambert shading model'''
    
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
    
    def get_texture(self, slot_name : str) -> aspose.threed.shading.TextureBase:
        '''Gets the texture from the specified slot, it can be material's property name or shader's parameter name
        
        :param slot_name: Slot name.
        :returns: The texture.'''
        ...
    
    def set_texture(self, slot_name : str, texture : aspose.threed.shading.TextureBase):
        '''Sets the texture to specified slot
        
        :param slot_name: Slot name.
        :param texture: Texture.'''
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
    
    @classmethod
    @property
    def MAP_SPECULAR(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_DIFFUSE(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_EMISSIVE(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_AMBIENT(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_NORMAL(cls) -> str:
        ...
    
    @property
    def emissive_color(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @emissive_color.setter
    def emissive_color(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def ambient_color(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @ambient_color.setter
    def ambient_color(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def diffuse_color(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @diffuse_color.setter
    def diffuse_color(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def transparent_color(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @transparent_color.setter
    def transparent_color(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def transparency(self) -> float:
        '''Gets the transparency factor.
        The factor should be ranged between 0(0%, fully opaque) and 1(100%, fully transparent)
        Any invalid factor value will be clamped.'''
        ...
    
    @transparency.setter
    def transparency(self, value : float):
        '''Sets the transparency factor.
        The factor should be ranged between 0(0%, fully opaque) and 1(100%, fully transparent)
        Any invalid factor value will be clamped.'''
        ...
    
    ...

class Material(aspose.threed.A3DObject):
    '''Material defines the parameters necessary for visual appearance of geometry.
    Aspose.3D provides shading model for :py:class:`aspose.threed.shading.LambertMaterial`, :py:class:`aspose.threed.shading.PhongMaterial` and :py:class:`aspose.threed.shading.ShaderMaterial`'''
    
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
    
    def get_texture(self, slot_name : str) -> aspose.threed.shading.TextureBase:
        '''Gets the texture from the specified slot, it can be material's property name or shader's parameter name
        
        :param slot_name: Slot name.
        :returns: The texture.'''
        ...
    
    def set_texture(self, slot_name : str, texture : aspose.threed.shading.TextureBase):
        '''Sets the texture to specified slot
        
        :param slot_name: Slot name.
        :param texture: Texture.'''
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
    
    @classmethod
    @property
    def MAP_SPECULAR(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_DIFFUSE(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_EMISSIVE(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_AMBIENT(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_NORMAL(cls) -> str:
        ...
    
    ...

class PbrMaterial(Material):
    '''Material for physically based rendering based on albedo color/metallic/roughness'''
    
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
    
    def get_texture(self, slot_name : str) -> aspose.threed.shading.TextureBase:
        '''Gets the texture from the specified slot, it can be material's property name or shader's parameter name
        
        :param slot_name: Slot name.
        :returns: The texture.'''
        ...
    
    def set_texture(self, slot_name : str, texture : aspose.threed.shading.TextureBase):
        '''Sets the texture to specified slot
        
        :param slot_name: Slot name.
        :param texture: Texture.'''
        ...
    
    @staticmethod
    def from_material(material : aspose.threed.shading.Material) -> aspose.threed.shading.PbrMaterial:
        '''Allow convert other material to PbrMaterial'''
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
    
    @classmethod
    @property
    def MAP_SPECULAR(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_DIFFUSE(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_EMISSIVE(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_AMBIENT(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_NORMAL(cls) -> str:
        ...
    
    @property
    def transparency(self) -> float:
        '''Gets the transparency factor.
        The factor should be ranged between 0(0%, fully opaque) and 1(100%, fully transparent)
        Any invalid factor value will be clamped.'''
        ...
    
    @transparency.setter
    def transparency(self, value : float):
        '''Sets the transparency factor.
        The factor should be ranged between 0(0%, fully opaque) and 1(100%, fully transparent)
        Any invalid factor value will be clamped.'''
        ...
    
    @property
    def normal_texture(self) -> aspose.threed.shading.TextureBase:
        ...
    
    @normal_texture.setter
    def normal_texture(self, value : aspose.threed.shading.TextureBase):
        ...
    
    @property
    def specular_texture(self) -> aspose.threed.shading.TextureBase:
        ...
    
    @specular_texture.setter
    def specular_texture(self, value : aspose.threed.shading.TextureBase):
        ...
    
    @property
    def albedo_texture(self) -> aspose.threed.shading.TextureBase:
        ...
    
    @albedo_texture.setter
    def albedo_texture(self, value : aspose.threed.shading.TextureBase):
        ...
    
    @property
    def albedo(self) -> aspose.threed.utilities.Vector3:
        '''Gets the base color of the material'''
        ...
    
    @albedo.setter
    def albedo(self, value : aspose.threed.utilities.Vector3):
        '''Sets the base color of the material'''
        ...
    
    @property
    def occlusion_texture(self) -> aspose.threed.shading.TextureBase:
        ...
    
    @occlusion_texture.setter
    def occlusion_texture(self, value : aspose.threed.shading.TextureBase):
        ...
    
    @property
    def occlusion_factor(self) -> float:
        ...
    
    @occlusion_factor.setter
    def occlusion_factor(self, value : float):
        ...
    
    @property
    def metallic_factor(self) -> float:
        ...
    
    @metallic_factor.setter
    def metallic_factor(self, value : float):
        ...
    
    @property
    def roughness_factor(self) -> float:
        ...
    
    @roughness_factor.setter
    def roughness_factor(self, value : float):
        ...
    
    @property
    def metallic_roughness(self) -> aspose.threed.shading.TextureBase:
        ...
    
    @metallic_roughness.setter
    def metallic_roughness(self, value : aspose.threed.shading.TextureBase):
        ...
    
    @property
    def emissive_texture(self) -> aspose.threed.shading.TextureBase:
        ...
    
    @emissive_texture.setter
    def emissive_texture(self, value : aspose.threed.shading.TextureBase):
        ...
    
    @property
    def emissive_color(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @emissive_color.setter
    def emissive_color(self, value : aspose.threed.utilities.Vector3):
        ...
    
    ...

class PbrSpecularMaterial(Material):
    '''Material for physically based rendering based on diffuse color/specular/glossiness'''
    
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
    
    def get_texture(self, slot_name : str) -> aspose.threed.shading.TextureBase:
        '''Gets the texture from the specified slot, it can be material's property name or shader's parameter name
        
        :param slot_name: Slot name.
        :returns: The texture.'''
        ...
    
    def set_texture(self, slot_name : str, texture : aspose.threed.shading.TextureBase):
        '''Sets the texture to specified slot
        
        :param slot_name: Slot name.
        :param texture: Texture.'''
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
    
    @classmethod
    @property
    def MAP_SPECULAR(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_DIFFUSE(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_EMISSIVE(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_AMBIENT(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_NORMAL(cls) -> str:
        ...
    
    @property
    def transparency(self) -> float:
        '''Gets the transparency factor.
        The factor should be ranged between 0(0%, fully opaque) and 1(100%, fully transparent)
        Any invalid factor value will be clamped.'''
        ...
    
    @transparency.setter
    def transparency(self, value : float):
        '''Sets the transparency factor.
        The factor should be ranged between 0(0%, fully opaque) and 1(100%, fully transparent)
        Any invalid factor value will be clamped.'''
        ...
    
    @property
    def normal_texture(self) -> aspose.threed.shading.TextureBase:
        ...
    
    @normal_texture.setter
    def normal_texture(self, value : aspose.threed.shading.TextureBase):
        ...
    
    @property
    def specular_glossiness_texture(self) -> aspose.threed.shading.TextureBase:
        ...
    
    @specular_glossiness_texture.setter
    def specular_glossiness_texture(self, value : aspose.threed.shading.TextureBase):
        ...
    
    @property
    def glossiness_factor(self) -> float:
        ...
    
    @glossiness_factor.setter
    def glossiness_factor(self, value : float):
        ...
    
    @property
    def specular(self) -> aspose.threed.utilities.Vector3:
        '''Gets the specular color of the material, default value is (1, 1, 1).'''
        ...
    
    @specular.setter
    def specular(self, value : aspose.threed.utilities.Vector3):
        '''Sets the specular color of the material, default value is (1, 1, 1).'''
        ...
    
    @property
    def diffuse_texture(self) -> aspose.threed.shading.TextureBase:
        ...
    
    @diffuse_texture.setter
    def diffuse_texture(self, value : aspose.threed.shading.TextureBase):
        ...
    
    @property
    def diffuse(self) -> aspose.threed.utilities.Vector3:
        '''Gets the diffuse color of the material, default value is (1, 1, 1)'''
        ...
    
    @diffuse.setter
    def diffuse(self, value : aspose.threed.utilities.Vector3):
        '''Sets the diffuse color of the material, default value is (1, 1, 1)'''
        ...
    
    @property
    def emissive_texture(self) -> aspose.threed.shading.TextureBase:
        ...
    
    @emissive_texture.setter
    def emissive_texture(self, value : aspose.threed.shading.TextureBase):
        ...
    
    @property
    def emissive_color(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @emissive_color.setter
    def emissive_color(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @classmethod
    @property
    def MAP_SPECULAR_GLOSSINESS(cls) -> str:
        ...
    
    ...

class PhongMaterial(LambertMaterial):
    '''Material for blinn-phong shading model.'''
    
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
    
    def get_texture(self, slot_name : str) -> aspose.threed.shading.TextureBase:
        '''Gets the texture from the specified slot, it can be material's property name or shader's parameter name
        
        :param slot_name: Slot name.
        :returns: The texture.'''
        ...
    
    def set_texture(self, slot_name : str, texture : aspose.threed.shading.TextureBase):
        '''Sets the texture to specified slot
        
        :param slot_name: Slot name.
        :param texture: Texture.'''
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
    
    @classmethod
    @property
    def MAP_SPECULAR(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_DIFFUSE(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_EMISSIVE(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_AMBIENT(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_NORMAL(cls) -> str:
        ...
    
    @property
    def emissive_color(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @emissive_color.setter
    def emissive_color(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def ambient_color(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @ambient_color.setter
    def ambient_color(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def diffuse_color(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @diffuse_color.setter
    def diffuse_color(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def transparent_color(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @transparent_color.setter
    def transparent_color(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def transparency(self) -> float:
        '''Gets the transparency factor.
        The factor should be ranged between 0(0%, fully opaque) and 1(100%, fully transparent)
        Any invalid factor value will be clamped.'''
        ...
    
    @transparency.setter
    def transparency(self, value : float):
        '''Sets the transparency factor.
        The factor should be ranged between 0(0%, fully opaque) and 1(100%, fully transparent)
        Any invalid factor value will be clamped.'''
        ...
    
    @property
    def specular_color(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @specular_color.setter
    def specular_color(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def specular_factor(self) -> float:
        ...
    
    @specular_factor.setter
    def specular_factor(self, value : float):
        ...
    
    @property
    def shininess(self) -> float:
        '''Gets the shininess, this controls the specular highlight's size.
        The formula of specular:
        SpecularColor * SpecularFactor * (N dot H) ^ Shininess'''
        ...
    
    @shininess.setter
    def shininess(self, value : float):
        '''Sets the shininess, this controls the specular highlight's size.
        The formula of specular:
        SpecularColor * SpecularFactor * (N dot H) ^ Shininess'''
        ...
    
    @property
    def reflection_color(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @reflection_color.setter
    def reflection_color(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def reflection_factor(self) -> float:
        ...
    
    @reflection_factor.setter
    def reflection_factor(self, value : float):
        ...
    
    ...

class ShaderMaterial(Material):
    '''A shader material allows to describe the material by external rendering engine or shader language.
    :py:class:`aspose.threed.shading.ShaderMaterial` uses :py:class:`aspose.threed.shading.ShaderTechnique` to describe the concrete rendering details,
    and the most suitable one will be used according to the final rendering platform.
    For example, your :py:class:`aspose.threed.shading.ShaderMaterial` instance can have two technique, one is defined by HLSL, and another is defined by GLSL
    Under non-window platform the GLSL should be used instead of HLSL'''
    
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
    
    def get_texture(self, slot_name : str) -> aspose.threed.shading.TextureBase:
        '''Gets the texture from the specified slot, it can be material's property name or shader's parameter name
        
        :param slot_name: Slot name.
        :returns: The texture.'''
        ...
    
    def set_texture(self, slot_name : str, texture : aspose.threed.shading.TextureBase):
        '''Sets the texture to specified slot
        
        :param slot_name: Slot name.
        :param texture: Texture.'''
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
    
    @classmethod
    @property
    def MAP_SPECULAR(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_DIFFUSE(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_EMISSIVE(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_AMBIENT(cls) -> str:
        ...
    
    @classmethod
    @property
    def MAP_NORMAL(cls) -> str:
        ...
    
    @property
    def techniques(self) -> List[aspose.threed.shading.ShaderTechnique]:
        '''Gets all available techniques defined in this material.'''
        ...
    
    ...

class ShaderTechnique:
    '''A shader technique represents a concrete rendering implementation.'''
    
    def add_binding(self, property : str, shader_parameter : str):
        '''Binds the dynamic property to shader parameter
        
        :param property: The name of the dynamic property.
        :param shader_parameter: The name of the shader parameter.'''
        ...
    
    @property
    def description(self) -> str:
        '''Gets the description of this technique'''
        ...
    
    @description.setter
    def description(self, value : str):
        '''Sets the description of this technique'''
        ...
    
    @property
    def shader_language(self) -> str:
        ...
    
    @shader_language.setter
    def shader_language(self, value : str):
        ...
    
    @property
    def shader_version(self) -> str:
        ...
    
    @shader_version.setter
    def shader_version(self, value : str):
        ...
    
    @property
    def shader_file(self) -> str:
        ...
    
    @shader_file.setter
    def shader_file(self, value : str):
        ...
    
    @property
    def shader_content(self) -> bytes:
        ...
    
    @shader_content.setter
    def shader_content(self, value : bytes):
        ...
    
    @property
    def shader_entry(self) -> str:
        ...
    
    @shader_entry.setter
    def shader_entry(self, value : str):
        ...
    
    @property
    def render_api(self) -> str:
        ...
    
    @render_api.setter
    def render_api(self, value : str):
        ...
    
    @property
    def render_api_version(self) -> str:
        ...
    
    @render_api_version.setter
    def render_api_version(self, value : str):
        ...
    
    ...

class Texture(TextureBase):
    '''This class defines the texture from an external file.'''
    
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
    
    def set_translation(self, u : float, v : float):
        '''Sets the UV translation.
        
        :param u: U.
        :param v: V.'''
        ...
    
    def set_scale(self, u : float, v : float):
        '''Sets the UV scale.
        
        :param u: U.
        :param v: V.'''
        ...
    
    def set_rotation(self, u : float, v : float):
        '''Sets the UV rotation.
        
        :param u: U.
        :param v: V.'''
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
    def alpha(self) -> float:
        '''Gets the default alpha value of the texture
        This is valid when the :py:attr:`aspose.threed.shading.TextureBase.alpha_source` is :py:attr:`aspose.threed.shading.AlphaSource.PIXEL_ALPHA`
        Default value is 1.0, valid value range is between 0 and 1'''
        ...
    
    @alpha.setter
    def alpha(self, value : float):
        '''Sets the default alpha value of the texture
        This is valid when the :py:attr:`aspose.threed.shading.TextureBase.alpha_source` is :py:attr:`aspose.threed.shading.AlphaSource.PIXEL_ALPHA`
        Default value is 1.0, valid value range is between 0 and 1'''
        ...
    
    @property
    def alpha_source(self) -> aspose.threed.shading.AlphaSource:
        ...
    
    @alpha_source.setter
    def alpha_source(self, value : aspose.threed.shading.AlphaSource):
        ...
    
    @property
    def wrap_mode_u(self) -> aspose.threed.shading.WrapMode:
        ...
    
    @wrap_mode_u.setter
    def wrap_mode_u(self, value : aspose.threed.shading.WrapMode):
        ...
    
    @property
    def wrap_mode_v(self) -> aspose.threed.shading.WrapMode:
        ...
    
    @wrap_mode_v.setter
    def wrap_mode_v(self, value : aspose.threed.shading.WrapMode):
        ...
    
    @property
    def wrap_mode_w(self) -> aspose.threed.shading.WrapMode:
        ...
    
    @wrap_mode_w.setter
    def wrap_mode_w(self, value : aspose.threed.shading.WrapMode):
        ...
    
    @property
    def min_filter(self) -> aspose.threed.shading.TextureFilter:
        ...
    
    @min_filter.setter
    def min_filter(self, value : aspose.threed.shading.TextureFilter):
        ...
    
    @property
    def mag_filter(self) -> aspose.threed.shading.TextureFilter:
        ...
    
    @mag_filter.setter
    def mag_filter(self, value : aspose.threed.shading.TextureFilter):
        ...
    
    @property
    def mip_filter(self) -> aspose.threed.shading.TextureFilter:
        ...
    
    @mip_filter.setter
    def mip_filter(self, value : aspose.threed.shading.TextureFilter):
        ...
    
    @property
    def uv_rotation(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @uv_rotation.setter
    def uv_rotation(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def uv_scale(self) -> aspose.threed.utilities.Vector2:
        ...
    
    @uv_scale.setter
    def uv_scale(self, value : aspose.threed.utilities.Vector2):
        ...
    
    @property
    def uv_translation(self) -> aspose.threed.utilities.Vector2:
        ...
    
    @uv_translation.setter
    def uv_translation(self, value : aspose.threed.utilities.Vector2):
        ...
    
    @property
    def enable_mip_map(self) -> bool:
        ...
    
    @enable_mip_map.setter
    def enable_mip_map(self, value : bool):
        ...
    
    @property
    def content(self) -> bytes:
        '''Gets the binary content of the texture.
        The embedded texture content is optional, user should load texture from external file if this is missing.'''
        ...
    
    @content.setter
    def content(self, value : bytes):
        '''Sets the binary content of the texture.
        The embedded texture content is optional, user should load texture from external file if this is missing.'''
        ...
    
    @property
    def file_name(self) -> str:
        ...
    
    @file_name.setter
    def file_name(self, value : str):
        ...
    
    ...

class TextureBase(aspose.threed.A3DObject):
    '''Base class for all concrete textures.
    Texture defines the look and feel of a geometry surface.'''
    
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
    
    def set_translation(self, u : float, v : float):
        '''Sets the UV translation.
        
        :param u: U.
        :param v: V.'''
        ...
    
    def set_scale(self, u : float, v : float):
        '''Sets the UV scale.
        
        :param u: U.
        :param v: V.'''
        ...
    
    def set_rotation(self, u : float, v : float):
        '''Sets the UV rotation.
        
        :param u: U.
        :param v: V.'''
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
    def alpha(self) -> float:
        '''Gets the default alpha value of the texture
        This is valid when the :py:attr:`aspose.threed.shading.TextureBase.alpha_source` is :py:attr:`aspose.threed.shading.AlphaSource.PIXEL_ALPHA`
        Default value is 1.0, valid value range is between 0 and 1'''
        ...
    
    @alpha.setter
    def alpha(self, value : float):
        '''Sets the default alpha value of the texture
        This is valid when the :py:attr:`aspose.threed.shading.TextureBase.alpha_source` is :py:attr:`aspose.threed.shading.AlphaSource.PIXEL_ALPHA`
        Default value is 1.0, valid value range is between 0 and 1'''
        ...
    
    @property
    def alpha_source(self) -> aspose.threed.shading.AlphaSource:
        ...
    
    @alpha_source.setter
    def alpha_source(self, value : aspose.threed.shading.AlphaSource):
        ...
    
    @property
    def wrap_mode_u(self) -> aspose.threed.shading.WrapMode:
        ...
    
    @wrap_mode_u.setter
    def wrap_mode_u(self, value : aspose.threed.shading.WrapMode):
        ...
    
    @property
    def wrap_mode_v(self) -> aspose.threed.shading.WrapMode:
        ...
    
    @wrap_mode_v.setter
    def wrap_mode_v(self, value : aspose.threed.shading.WrapMode):
        ...
    
    @property
    def wrap_mode_w(self) -> aspose.threed.shading.WrapMode:
        ...
    
    @wrap_mode_w.setter
    def wrap_mode_w(self, value : aspose.threed.shading.WrapMode):
        ...
    
    @property
    def min_filter(self) -> aspose.threed.shading.TextureFilter:
        ...
    
    @min_filter.setter
    def min_filter(self, value : aspose.threed.shading.TextureFilter):
        ...
    
    @property
    def mag_filter(self) -> aspose.threed.shading.TextureFilter:
        ...
    
    @mag_filter.setter
    def mag_filter(self, value : aspose.threed.shading.TextureFilter):
        ...
    
    @property
    def mip_filter(self) -> aspose.threed.shading.TextureFilter:
        ...
    
    @mip_filter.setter
    def mip_filter(self, value : aspose.threed.shading.TextureFilter):
        ...
    
    @property
    def uv_rotation(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @uv_rotation.setter
    def uv_rotation(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def uv_scale(self) -> aspose.threed.utilities.Vector2:
        ...
    
    @uv_scale.setter
    def uv_scale(self, value : aspose.threed.utilities.Vector2):
        ...
    
    @property
    def uv_translation(self) -> aspose.threed.utilities.Vector2:
        ...
    
    @uv_translation.setter
    def uv_translation(self, value : aspose.threed.utilities.Vector2):
        ...
    
    ...

class TextureSlot:
    '''Texture slot in :py:class:`aspose.threed.shading.Material`, can be enumerated through material instance.'''
    
    @property
    def slot_name(self) -> str:
        ...
    
    @property
    def texture(self) -> aspose.threed.shading.TextureBase:
        '''The texture that will be bounded to the material.'''
        ...
    
    ...

class AlphaSource:
    '''Defines whether the texture contains the alpha channel.'''
    
    @classmethod
    @property
    def NONE(cls) -> AlphaSource:
        '''No alpha is defined in the texture'''
        ...
    
    @classmethod
    @property
    def PIXEL_ALPHA(cls) -> AlphaSource:
        '''The alpha is defined by pixel's alpha channel'''
        ...
    
    @classmethod
    @property
    def FIXED_VALUE(cls) -> AlphaSource:
        '''The Alpha is a fixed value which is defined by :py:attr:`aspose.threed.shading.TextureBase.alpha`'''
        ...
    
    ...

class TextureFilter:
    '''Filter options during texture sampling.'''
    
    @classmethod
    @property
    def NONE(cls) -> TextureFilter:
        '''No minification, this is only used by minification filter.'''
        ...
    
    @classmethod
    @property
    def POINT(cls) -> TextureFilter:
        '''Use point sampling'''
        ...
    
    @classmethod
    @property
    def LINEAR(cls) -> TextureFilter:
        '''Use linear interpolation for sampling'''
        ...
    
    @classmethod
    @property
    def ANISOTROPIC(cls) -> TextureFilter:
        '''Use anisotropic interpolation for sampling, this is only used by minification filter.'''
        ...
    
    ...

class WrapMode:
    '''Texture's wrap mode.'''
    
    @classmethod
    @property
    def WRAP(cls) -> WrapMode:
        '''Tiles the texture on the model's surface, creating a repeating pattern.'''
        ...
    
    @classmethod
    @property
    def CLAMP(cls) -> WrapMode:
        '''Clamps the texture to the last pixel at the border.'''
        ...
    
    @classmethod
    @property
    def MIRROR(cls) -> WrapMode:
        '''The texture will be repeated, but it will be mirrored when the integer part of the coordinate is odd.'''
        ...
    
    @classmethod
    @property
    def MIRROR_ONCE(cls) -> WrapMode:
        '''The texture will be mirrored once, and then clamps to the maximum value.'''
        ...
    
    @classmethod
    @property
    def BORDER(cls) -> WrapMode:
        '''The coordinates that outside of the range [0.0, 1.0] are set to a specified border color.'''
        ...
    
    ...

