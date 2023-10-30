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

class Bone(aspose.threed.A3DObject):
    '''A bone defines the subset of the geometry's control point, and defined blend weight for each control point.
    The :py:class:`aspose.threed.deformers.Bone` object cannot be used directly, a :py:class:`aspose.threed.deformers.SkinDeformer` instance is used to deform the geometry, and :py:class:`aspose.threed.deformers.SkinDeformer` comes with a set of bones, each bone linked to a node.
    NOTE: A control point of a geometry can be bounded to more than one Bones.'''
    
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
    
    def get_weight(self, index : int) -> float:
        '''Gets the weight for control point specified by index
        
        :param index: Control point's index
        :returns: the weight at specified index, or 0 if the index is invalid'''
        ...
    
    def set_weight(self, index : int, weight : float):
        '''Sets the weight for control point specified by index
        
        :param index: Control point's index
        :param weight: New weight'''
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
    def weight_count(self) -> int:
        ...
    
    @property
    def transform(self) -> aspose.threed.utilities.Matrix4:
        '''Gets the transform matrix of the node containing the bone.'''
        ...
    
    @transform.setter
    def transform(self, value : aspose.threed.utilities.Matrix4):
        '''Sets the transform matrix of the node containing the bone.'''
        ...
    
    @property
    def bone_transform(self) -> aspose.threed.utilities.Matrix4:
        ...
    
    @bone_transform.setter
    def bone_transform(self, value : aspose.threed.utilities.Matrix4):
        ...
    
    @property
    def node(self) -> aspose.threed.Node:
        '''Gets the node. The bone node is the bone which skin attached to, the :py:class:`aspose.threed.deformers.SkinDeformer` will use bone node to influence the displacement of the control points.
        Bone node usually has a :py:class:`aspose.threed.entities.Skeleton` attached, but it's not required.
        Attached :py:class:`aspose.threed.entities.Skeleton` is usually used by DCC software to show skeleton to user.'''
        ...
    
    @node.setter
    def node(self, value : aspose.threed.Node):
        '''Sets the node. The bone node is the bone which skin attached to, the :py:class:`aspose.threed.deformers.SkinDeformer` will use bone node to influence the displacement of the control points.
        Bone node usually has a :py:class:`aspose.threed.entities.Skeleton` attached, but it's not required.
        Attached :py:class:`aspose.threed.entities.Skeleton` is usually used by DCC software to show skeleton to user.'''
        ...
    
    def __getitem__(self, key : int) -> float:
        ...
    
    def __setitem__(self, key : int, value : float):
        ...
    
    ...

class Deformer(aspose.threed.A3DObject):
    '''Base class for :py:class:`aspose.threed.deformers.SkinDeformer` and :py:class:`aspose.threed.deformers.MorphTargetDeformer`'''
    
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
    def owner(self) -> aspose.threed.entities.Geometry:
        '''Gets the geometry which owns this deformer'''
        ...
    
    ...

class MorphTargetChannel(aspose.threed.A3DObject):
    '''A MorphTargetChannel is used by :py:class:`aspose.threed.deformers.MorphTargetDeformer` to organize the target geometries.
    Some file formats like FBX support multiple channels in parallel.'''
    
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
    
    def get_weight(self, target : aspose.threed.entities.Shape) -> float:
        '''Gets the weight for the specified target, if the target is not belongs to this channel, default value 0 is returned.'''
        ...
    
    def set_weight(self, target : aspose.threed.entities.Shape, weight : float):
        '''Sets the weight for the specified target, default value is 1, range should between 0~1'''
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
    def weights(self) -> List[float]:
        '''Gets the full weight values of target geometries.'''
        ...
    
    @property
    def channel_weight(self) -> float:
        ...
    
    @channel_weight.setter
    def channel_weight(self, value : float):
        ...
    
    @property
    def targets(self) -> List[aspose.threed.entities.Shape]:
        '''Gets all targets associated with the channel.'''
        ...
    
    @classmethod
    @property
    def DEFAULT_WEIGHT(cls) -> float:
        ...
    
    ...

class MorphTargetDeformer(Deformer):
    '''MorphTargetDeformer provides per-vertex animation.
    MorphTargetDeformer organize all targets via :py:class:`aspose.threed.deformers.MorphTargetChannel`, each channel can organize multiple targets.
    A common use of morph target deformer is to apply facial expression to a character.
    More details can be found at https://en.wikipedia.org/wiki/Morph_target_animation'''
    
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
    def owner(self) -> aspose.threed.entities.Geometry:
        '''Gets the geometry which owns this deformer'''
        ...
    
    @property
    def channels(self) -> List[aspose.threed.deformers.MorphTargetChannel]:
        '''Gets all channels contained in this deformer'''
        ...
    
    ...

class SkinDeformer(Deformer):
    '''A skin deformer contains multiple bones to work, each bone blends a part of the geometry by control point's weights.'''
    
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
    def owner(self) -> aspose.threed.entities.Geometry:
        '''Gets the geometry which owns this deformer'''
        ...
    
    @property
    def bones(self) -> List[aspose.threed.deformers.Bone]:
        '''Gets all bones that the skin deformer contains'''
        ...
    
    ...

