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

class ArbitraryProfile(Profile):
    '''This class allows you to construct a 2D profile directly from arbitrary curve.'''
    
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
    
    @property
    def curve(self) -> aspose.threed.entities.Curve:
        '''The Curve used to construct the profile'''
        ...
    
    @curve.setter
    def curve(self, value : aspose.threed.entities.Curve):
        '''The Curve used to construct the profile'''
        ...
    
    ...

class CShape(ParameterizedProfile):
    '''IFC compatible C-shape profile that defined by parameters.
    The center position of the profile is in the center of the bounding box.'''
    
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
    
    def get_extent(self) -> aspose.threed.utilities.Vector2:
        '''Gets the extent in x and y dimension.'''
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
    
    @property
    def depth(self) -> float:
        '''Gets the depth of the profile.'''
        ...
    
    @depth.setter
    def depth(self, value : float):
        '''Sets the depth of the profile.'''
        ...
    
    @property
    def width(self) -> float:
        '''Gets the width of the profile.'''
        ...
    
    @width.setter
    def width(self, value : float):
        '''Sets the width of the profile.'''
        ...
    
    @property
    def girth(self) -> float:
        '''Gets the length of girth.'''
        ...
    
    @girth.setter
    def girth(self, value : float):
        '''Sets the length of girth.'''
        ...
    
    @property
    def wall_thickness(self) -> float:
        ...
    
    @wall_thickness.setter
    def wall_thickness(self, value : float):
        ...
    
    @property
    def internal_fillet_radius(self) -> float:
        ...
    
    @internal_fillet_radius.setter
    def internal_fillet_radius(self, value : float):
        ...
    
    ...

class CircleShape(ParameterizedProfile):
    '''IFC compatible circle profile, which can be used to construct a mesh through :py:class:`aspose.threed.entities.LinearExtrusion`'''
    
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
    
    def get_extent(self) -> aspose.threed.utilities.Vector2:
        '''Gets the extent in x and y dimension.'''
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
    
    @property
    def radius(self) -> float:
        '''Gets the radius of the circle.'''
        ...
    
    @radius.setter
    def radius(self, value : float):
        '''Sets the radius of the circle.'''
        ...
    
    ...

class EllipseShape(ParameterizedProfile):
    '''IFC compatible ellipse shape that defined by parameters.
    The center position of the profile is in the center of the bounding box.'''
    
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
    
    def get_extent(self) -> aspose.threed.utilities.Vector2:
        '''Gets the extent in x and y dimension.'''
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
    
    @property
    def semi_axis1(self) -> float:
        ...
    
    @semi_axis1.setter
    def semi_axis1(self, value : float):
        ...
    
    @property
    def semi_axis2(self) -> float:
        ...
    
    @semi_axis2.setter
    def semi_axis2(self, value : float):
        ...
    
    ...

class FontFile(aspose.threed.A3DObject):
    '''Font file contains definitions for glyphs, this is used to create text profile.'''
    
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
    
    @staticmethod
    def from_file(file_name : str) -> aspose.threed.profiles.FontFile:
        '''Load FontFile from file name
        
        :param file_name: Path to the font file
        :returns: FontFile instance'''
        ...
    
    @staticmethod
    def parse(bytes : bytes) -> aspose.threed.profiles.FontFile:
        '''Parse FontFile from bytes
        
        :param bytes: OTF font file raw content
        :returns: FontFile instance'''
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

class HShape(ParameterizedProfile):
    '''The :py:class:`aspose.threed.profiles.HShape` provides the defining parameters of an 'H' or 'I' shape.'''
    
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
    
    def get_extent(self) -> aspose.threed.utilities.Vector2:
        '''Gets the extent in x and y dimension.'''
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
    
    @property
    def overall_depth(self) -> float:
        ...
    
    @overall_depth.setter
    def overall_depth(self, value : float):
        ...
    
    @property
    def bottom_flange_width(self) -> float:
        ...
    
    @bottom_flange_width.setter
    def bottom_flange_width(self, value : float):
        ...
    
    @property
    def top_flange_width(self) -> float:
        ...
    
    @top_flange_width.setter
    def top_flange_width(self, value : float):
        ...
    
    @property
    def top_flange_thickness(self) -> float:
        ...
    
    @top_flange_thickness.setter
    def top_flange_thickness(self, value : float):
        ...
    
    @property
    def top_flange_edge_radius(self) -> float:
        ...
    
    @top_flange_edge_radius.setter
    def top_flange_edge_radius(self, value : float):
        ...
    
    @property
    def top_flange_fillet_radius(self) -> float:
        ...
    
    @top_flange_fillet_radius.setter
    def top_flange_fillet_radius(self, value : float):
        ...
    
    @property
    def bottom_flange_thickness(self) -> float:
        ...
    
    @bottom_flange_thickness.setter
    def bottom_flange_thickness(self, value : float):
        ...
    
    @property
    def web_thickness(self) -> float:
        ...
    
    @web_thickness.setter
    def web_thickness(self, value : float):
        ...
    
    @property
    def bottom_flange_fillet_radius(self) -> float:
        ...
    
    @bottom_flange_fillet_radius.setter
    def bottom_flange_fillet_radius(self, value : float):
        ...
    
    @property
    def bottom_flange_edge_radius(self) -> float:
        ...
    
    @bottom_flange_edge_radius.setter
    def bottom_flange_edge_radius(self, value : float):
        ...
    
    ...

class HollowCircleShape(CircleShape):
    '''IFC compatible hollow circle profile.'''
    
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
    
    def get_extent(self) -> aspose.threed.utilities.Vector2:
        '''Gets the extent in x and y dimension.'''
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
    
    @property
    def radius(self) -> float:
        '''Gets the radius of the circle.'''
        ...
    
    @radius.setter
    def radius(self, value : float):
        '''Sets the radius of the circle.'''
        ...
    
    @property
    def wall_thickness(self) -> float:
        ...
    
    @wall_thickness.setter
    def wall_thickness(self, value : float):
        ...
    
    ...

class HollowRectangleShape(RectangleShape):
    '''IFC compatible hollow rectangular shape with both inner/outer rounding corners.'''
    
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
    
    def get_extent(self) -> aspose.threed.utilities.Vector2:
        '''Gets the extent in x and y dimension.'''
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
    
    @property
    def rounding_radius(self) -> float:
        ...
    
    @rounding_radius.setter
    def rounding_radius(self, value : float):
        ...
    
    @property
    def x_dim(self) -> float:
        ...
    
    @x_dim.setter
    def x_dim(self, value : float):
        ...
    
    @property
    def y_dim(self) -> float:
        ...
    
    @y_dim.setter
    def y_dim(self, value : float):
        ...
    
    @property
    def wall_thickness(self) -> float:
        ...
    
    @wall_thickness.setter
    def wall_thickness(self, value : float):
        ...
    
    @property
    def inner_fillet_radius(self) -> float:
        ...
    
    @inner_fillet_radius.setter
    def inner_fillet_radius(self, value : float):
        ...
    
    ...

class LShape(ParameterizedProfile):
    '''IFC compatible L-shape profile that defined by parameters.'''
    
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
    
    def get_extent(self) -> aspose.threed.utilities.Vector2:
        '''Gets the extent in x and y dimension.'''
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
    
    @property
    def depth(self) -> float:
        '''Gets the depth of the profile.'''
        ...
    
    @depth.setter
    def depth(self, value : float):
        '''Sets the depth of the profile.'''
        ...
    
    @property
    def width(self) -> float:
        '''Gets the width of the profile.'''
        ...
    
    @width.setter
    def width(self, value : float):
        '''Sets the width of the profile.'''
        ...
    
    @property
    def thickness(self) -> float:
        '''Gets the thickness of the constant wall.'''
        ...
    
    @thickness.setter
    def thickness(self, value : float):
        '''Sets the thickness of the constant wall.'''
        ...
    
    @property
    def fillet_radius(self) -> float:
        ...
    
    @fillet_radius.setter
    def fillet_radius(self, value : float):
        ...
    
    @property
    def edge_radius(self) -> float:
        ...
    
    @edge_radius.setter
    def edge_radius(self, value : float):
        ...
    
    ...

class MirroredProfile(Profile):
    '''IFC compatible mirror profile.
    This profile defines a new profile by mirroring the base profile about the y axis.'''
    
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
    
    @property
    def base_profile(self) -> aspose.threed.profiles.Profile:
        ...
    
    ...

class ParameterizedProfile(Profile):
    '''The base class of all parameterized profiles.'''
    
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
    
    def get_extent(self) -> aspose.threed.utilities.Vector2:
        '''Gets the extent in x and y dimension.'''
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

class Profile(aspose.threed.Entity):
    '''2D Profile in xy plane'''
    
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

class RectangleShape(ParameterizedProfile):
    '''IFC compatible rectangular shape with rounding corners.'''
    
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
    
    def get_extent(self) -> aspose.threed.utilities.Vector2:
        '''Gets the extent in x and y dimension.'''
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
    
    @property
    def rounding_radius(self) -> float:
        ...
    
    @rounding_radius.setter
    def rounding_radius(self, value : float):
        ...
    
    @property
    def x_dim(self) -> float:
        ...
    
    @x_dim.setter
    def x_dim(self, value : float):
        ...
    
    @property
    def y_dim(self) -> float:
        ...
    
    @y_dim.setter
    def y_dim(self, value : float):
        ...
    
    ...

class TShape(ParameterizedProfile):
    '''IFC compatible T-shape defined by parameters.'''
    
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
    
    def get_extent(self) -> aspose.threed.utilities.Vector2:
        '''Gets the extent in x and y dimension.'''
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
    
    @property
    def depth(self) -> float:
        '''Gets the length of the web.'''
        ...
    
    @depth.setter
    def depth(self, value : float):
        '''Sets the length of the web.'''
        ...
    
    @property
    def flange_width(self) -> float:
        ...
    
    @flange_width.setter
    def flange_width(self, value : float):
        ...
    
    @property
    def web_thickness(self) -> float:
        ...
    
    @web_thickness.setter
    def web_thickness(self, value : float):
        ...
    
    @property
    def flange_thickness(self) -> float:
        ...
    
    @flange_thickness.setter
    def flange_thickness(self, value : float):
        ...
    
    @property
    def fillet_radius(self) -> float:
        ...
    
    @fillet_radius.setter
    def fillet_radius(self, value : float):
        ...
    
    @property
    def flange_edge_radius(self) -> float:
        ...
    
    @flange_edge_radius.setter
    def flange_edge_radius(self, value : float):
        ...
    
    @property
    def web_edge_radius(self) -> float:
        ...
    
    @web_edge_radius.setter
    def web_edge_radius(self, value : float):
        ...
    
    ...

class Text(Profile):
    '''Text profile, this profile describes contours using font and text.'''
    
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
    
    @property
    def content(self) -> str:
        '''Content of the text'''
        ...
    
    @content.setter
    def content(self, value : str):
        '''Content of the text'''
        ...
    
    @property
    def font(self) -> aspose.threed.profiles.FontFile:
        '''The font of the text.'''
        ...
    
    @font.setter
    def font(self, value : aspose.threed.profiles.FontFile):
        '''The font of the text.'''
        ...
    
    @property
    def font_size(self) -> float:
        ...
    
    @font_size.setter
    def font_size(self, value : float):
        ...
    
    ...

class TrapeziumShape(ParameterizedProfile):
    '''IFC compatible Trapezium shape defined by parameters.'''
    
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
    
    def get_extent(self) -> aspose.threed.utilities.Vector2:
        '''Gets the extent in x and y dimension.'''
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
    
    @property
    def bottom_x_dim(self) -> float:
        ...
    
    @bottom_x_dim.setter
    def bottom_x_dim(self, value : float):
        ...
    
    @property
    def top_x_dim(self) -> float:
        ...
    
    @top_x_dim.setter
    def top_x_dim(self, value : float):
        ...
    
    @property
    def y_dim(self) -> float:
        ...
    
    @y_dim.setter
    def y_dim(self, value : float):
        ...
    
    @property
    def top_x_offset(self) -> float:
        ...
    
    @top_x_offset.setter
    def top_x_offset(self, value : float):
        ...
    
    ...

class UShape(ParameterizedProfile):
    '''IFC compatible U-shape defined by parameters.'''
    
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
    
    def get_extent(self) -> aspose.threed.utilities.Vector2:
        '''Gets the extent in x and y dimension.'''
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
    
    @property
    def depth(self) -> float:
        '''Gets the length of web.'''
        ...
    
    @depth.setter
    def depth(self, value : float):
        '''Sets the length of web.'''
        ...
    
    @property
    def flange_width(self) -> float:
        ...
    
    @flange_width.setter
    def flange_width(self, value : float):
        ...
    
    @property
    def web_thickness(self) -> float:
        ...
    
    @web_thickness.setter
    def web_thickness(self, value : float):
        ...
    
    @property
    def flange_thickness(self) -> float:
        ...
    
    @flange_thickness.setter
    def flange_thickness(self, value : float):
        ...
    
    @property
    def fillet_radius(self) -> float:
        ...
    
    @fillet_radius.setter
    def fillet_radius(self, value : float):
        ...
    
    @property
    def edge_radius(self) -> float:
        ...
    
    @edge_radius.setter
    def edge_radius(self, value : float):
        ...
    
    ...

class ZShape(ParameterizedProfile):
    '''IFC compatible Z-shape profile defined by parameters.'''
    
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
    
    def get_extent(self) -> aspose.threed.utilities.Vector2:
        '''Gets the extent in x and y dimension.'''
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
    
    @property
    def depth(self) -> float:
        '''Gets the length of web.'''
        ...
    
    @depth.setter
    def depth(self, value : float):
        '''Sets the length of web.'''
        ...
    
    @property
    def flange_width(self) -> float:
        ...
    
    @flange_width.setter
    def flange_width(self, value : float):
        ...
    
    @property
    def web_thickness(self) -> float:
        ...
    
    @web_thickness.setter
    def web_thickness(self, value : float):
        ...
    
    @property
    def flange_thickness(self) -> float:
        ...
    
    @flange_thickness.setter
    def flange_thickness(self, value : float):
        ...
    
    @property
    def fillet_radius(self) -> float:
        ...
    
    @fillet_radius.setter
    def fillet_radius(self, value : float):
        ...
    
    @property
    def edge_radius(self) -> float:
        ...
    
    @edge_radius.setter
    def edge_radius(self, value : float):
        ...
    
    ...

