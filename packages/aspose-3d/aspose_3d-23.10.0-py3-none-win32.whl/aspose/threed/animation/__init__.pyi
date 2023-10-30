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

class AnimationChannel:
    '''A channel maps property's component field to a set of keyframe sequences'''
    
    def add_keyframe_sequence(self, sequence : aspose.threed.animation.KeyframeSequence):
        '''Adds keyframe sequence to this channel
        
        :param sequence: The keyframe sequence to add.'''
        ...
    
    @property
    def component_type(self) -> Type:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name of the channel'''
        ...
    
    @property
    def default_value(self) -> any:
        ...
    
    @default_value.setter
    def default_value(self, value : any):
        ...
    
    @property
    def keyframe_sequences(self) -> List[aspose.threed.animation.KeyframeSequence]:
        ...
    
    ...

class AnimationClip(aspose.threed.SceneObject):
    '''The Animation clip is a collection of animations.
    The scene can have one or more animation clips.'''
    
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
    
    def create_animation_node(self, node_name : str) -> aspose.threed.animation.AnimationNode:
        '''A shorthand function to create and register the animation node on current clip.
        
        :param node_name: New animation node's name'''
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
    def animations(self) -> List[aspose.threed.animation.AnimationNode]:
        '''Gets the animations contained inside the clip.'''
        ...
    
    @property
    def description(self) -> str:
        '''Gets the description of this animation clip'''
        ...
    
    @description.setter
    def description(self, value : str):
        '''Sets the description of this animation clip'''
        ...
    
    @property
    def start(self) -> float:
        '''Gets the time in seconds of the beginning of the clip.'''
        ...
    
    @start.setter
    def start(self, value : float):
        '''Sets the time in seconds of the beginning of the clip.'''
        ...
    
    @property
    def stop(self) -> float:
        '''Gets the time in seconds of the end of the clip.'''
        ...
    
    @stop.setter
    def stop(self, value : float):
        '''Sets the time in seconds of the end of the clip.'''
        ...
    
    ...

class AnimationNode(aspose.threed.A3DObject):
    '''Aspose.3D's supports animation hierarchy, each animation can be composed by several animations and animation's key-frame definition.
    
    :py:class:`aspose.threed.animation.AnimationNode` defines the transformation of a property value over time, for example, animation node can be used to control a node's transformation or other :py:class:`aspose.threed.A3DObject` object's numerical properties.'''
    
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
    def get_keyframe_sequence(self, target : aspose.threed.A3DObject, prop_name : str, channel_name : str, create : bool) -> aspose.threed.animation.KeyframeSequence:
        '''Gets the keyframe sequence on given property and channel.
        
        :param target: On which instance to create the keyframe sequence.
        :param prop_name: The property's name.
        :param channel_name: The channel name.
        :param create: If set to ``true`` create the animation sequence if it's not existing.
        :returns: The keyframe sequence.'''
        ...
    
    @overload
    def get_keyframe_sequence(self, target : aspose.threed.A3DObject, prop_name : str, create : bool) -> aspose.threed.animation.KeyframeSequence:
        '''Gets the keyframe sequence on given property.
        
        :param target: On which instance to create the keyframe sequence.
        :param prop_name: The property's name.
        :param create: If set to ``true``, create the sequence if it's not existing.
        :returns: The keyframe sequence.'''
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
    
    def find_bind_point(self, name : str) -> aspose.threed.animation.BindPoint:
        '''Finds the bind point by name.
        
        :param name: Bind point's name to find.
        :returns: The bind point.'''
        ...
    
    def get_bind_point(self, target : aspose.threed.A3DObject, prop_name : str, create : bool) -> aspose.threed.animation.BindPoint:
        '''Gets the animation bind point on given property.
        
        :param target: On which object to create the bind point.
        :param prop_name: The property's name.
        :param create: If set to ``true`` create the bind point if it's not existing.
        :returns: The bind point.'''
        ...
    
    def create_bind_point(self, obj : aspose.threed.A3DObject, prop_name : str) -> aspose.threed.animation.BindPoint:
        '''Creates a BindPoint based on the property data type.
        
        :param obj: Object.
        :param prop_name: Property name.
        :returns: The bind point instance or null if the property is not defined.'''
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
    def bind_points(self) -> List[aspose.threed.animation.BindPoint]:
        ...
    
    @property
    def sub_animations(self) -> List[aspose.threed.animation.AnimationNode]:
        ...
    
    ...

class BindPoint(aspose.threed.A3DObject):
    '''A :py:class:`aspose.threed.animation.BindPoint` is usually created on an object's property, some property types contains multiple component fields(like a Vector3 field),
    :py:class:`aspose.threed.animation.BindPoint` will generate channel for each component field and connects the field to one or more keyframe sequence instance(s) through the channels.'''
    
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
    def add_channel(self, name : str, value : any) -> bool:
        '''Adds the specified channel property.
        
        :param name: Name.
        :param value: Value.
        :returns: true, if channel was added, false otherwise.'''
        ...
    
    @overload
    def add_channel(self, name : str, type : Type, value : any) -> bool:
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
    
    def get_keyframe_sequence(self, channel_name : str) -> aspose.threed.animation.KeyframeSequence:
        '''Gets the first keyframe sequence in specified channel
        
        :param channel_name: The channel name to find
        :returns: First keyframe sequence with the channel name'''
        ...
    
    def get_keyframe_sequences(self, channel_name : str) -> List[aspose.threed.animation.KeyframeSequence]:
        '''Gets all keyframe sequences in specified channel
        
        :param channel_name: The channel name to find
        :returns: Keyframe sequence list with the channel name'''
        ...
    
    def create_keyframe_sequence(self, name : str) -> aspose.threed.animation.KeyframeSequence:
        '''Creates a new curve and connects it to the first channel of the curve mapping
        
        :param name: The new sequence's name.
        :returns: The keyframe sequence.'''
        ...
    
    def bind_keyframe_sequence(self, channel_name : str, sequence : aspose.threed.animation.KeyframeSequence):
        '''Bind the keyframe sequence to specified channel
        
        :param channel_name: Which channel the keyframe sequence will be bound to
        :param sequence: The keyframe sequence to bind'''
        ...
    
    def get_channel(self, channel_name : str) -> aspose.threed.animation.AnimationChannel:
        '''Gets channel by given name
        
        :param channel_name: The channel name to find
        :returns: Channel with the name'''
        ...
    
    def reset_channels(self):
        '''Empties the property channels of this animation curve mapping.'''
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
    def property(self) -> aspose.threed.Property:
        '''Gets the property associated with the CurveMapping'''
        ...
    
    @property
    def channels_count(self) -> int:
        ...
    
    ...

class Extrapolation:
    '''Extrapolation defines how to do when sampled value is out of the range which defined by the first and last key-frames.'''
    
    @property
    def type(self) -> aspose.threed.animation.ExtrapolationType:
        '''Gets and sets the sampling pattern of extrapolation'''
        ...
    
    @type.setter
    def type(self, value : aspose.threed.animation.ExtrapolationType):
        '''Gets and sets the sampling pattern of extrapolation'''
        ...
    
    @property
    def repeat_count(self) -> int:
        ...
    
    @repeat_count.setter
    def repeat_count(self, value : int):
        ...
    
    ...

class KeyFrame:
    '''A key frame is mainly defined by a time and a value, for some interpolation types, tangent/tension/bias/continuity is also used by calculating the final sampled value.
    Sampled values in a non-key-frame time position is interpolated by key-frames between the previous and next key-frames
    Value before/after the first/last key-frame are calculated by the :py:class:`aspose.threed.animation.Extrapolation` class.'''
    
    @property
    def time(self) -> float:
        '''Gets the time position of list.data[index] key frame, measured in seconds.'''
        ...
    
    @time.setter
    def time(self, value : float):
        '''Sets the time position of list.data[index] key frame, measured in seconds.'''
        ...
    
    @property
    def value(self) -> float:
        '''Gets the key-frame's value.'''
        ...
    
    @value.setter
    def value(self, value : float):
        '''Sets the key-frame's value.'''
        ...
    
    @property
    def interpolation(self) -> aspose.threed.animation.Interpolation:
        '''Gets the key's interpolation type, list.data[index] defines the algorithm how the sampled value is calculated.'''
        ...
    
    @interpolation.setter
    def interpolation(self, value : aspose.threed.animation.Interpolation):
        '''Sets the key's interpolation type, list.data[index] defines the algorithm how the sampled value is calculated.'''
        ...
    
    @property
    def tangent_weight_mode(self) -> aspose.threed.animation.WeightedMode:
        ...
    
    @tangent_weight_mode.setter
    def tangent_weight_mode(self, value : aspose.threed.animation.WeightedMode):
        ...
    
    @property
    def step_mode(self) -> aspose.threed.animation.StepMode:
        ...
    
    @step_mode.setter
    def step_mode(self, value : aspose.threed.animation.StepMode):
        ...
    
    @property
    def next_in_tangent(self) -> aspose.threed.utilities.Vector2:
        ...
    
    @next_in_tangent.setter
    def next_in_tangent(self, value : aspose.threed.utilities.Vector2):
        ...
    
    @property
    def out_tangent(self) -> aspose.threed.utilities.Vector2:
        ...
    
    @out_tangent.setter
    def out_tangent(self, value : aspose.threed.utilities.Vector2):
        ...
    
    @property
    def out_weight(self) -> float:
        ...
    
    @out_weight.setter
    def out_weight(self, value : float):
        ...
    
    @property
    def next_in_weight(self) -> float:
        ...
    
    @next_in_weight.setter
    def next_in_weight(self, value : float):
        ...
    
    @property
    def tension(self) -> float:
        '''Gets tension used in TCB spline'''
        ...
    
    @tension.setter
    def tension(self, value : float):
        '''Sets tension used in TCB spline'''
        ...
    
    @property
    def continuity(self) -> float:
        '''Gets the continuity used in TCB spline'''
        ...
    
    @continuity.setter
    def continuity(self, value : float):
        '''Sets the continuity used in TCB spline'''
        ...
    
    @property
    def bias(self) -> float:
        '''Gets the bias used in TCB spline'''
        ...
    
    @bias.setter
    def bias(self, value : float):
        '''Sets the bias used in TCB spline'''
        ...
    
    @property
    def independent_tangent(self) -> bool:
        ...
    
    @independent_tangent.setter
    def independent_tangent(self, value : bool):
        ...
    
    @property
    def flat(self) -> bool:
        '''Get or set if the key frame is flat.
        Key frame should be flat if next or previous key frame has the same value.
        Flat key frame has flat tangents and fixed interpolation.'''
        ...
    
    @flat.setter
    def flat(self, value : bool):
        '''Get or set if the key frame is flat.
        Key frame should be flat if next or previous key frame has the same value.
        Flat key frame has flat tangents and fixed interpolation.'''
        ...
    
    @property
    def time_independent_tangent(self) -> bool:
        ...
    
    @time_independent_tangent.setter
    def time_independent_tangent(self, value : bool):
        ...
    
    ...

class KeyframeSequence(aspose.threed.A3DObject):
    '''The sequence of key-frames, it describes the transformation of a sampled value over time.'''
    
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
    def add(self, time : float, value : float):
        '''Create a new key frame with specified value
        
        :param time: Time position(measured in seconds)
        :param value: The value at this time position'''
        ...
    
    @overload
    def add(self, time : float, value : float, interpolation : aspose.threed.animation.Interpolation):
        '''Create a new key frame with specified value
        
        :param time: Time position(measured in seconds)
        :param value: The value at this time position
        :param interpolation: The interpolation type of this key frame'''
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
    
    def reset(self):
        '''Removes all key frames and reset the post/pre behaviors.'''
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
    def bind_point(self) -> aspose.threed.animation.BindPoint:
        ...
    
    @property
    def key_frames(self) -> List[aspose.threed.animation.KeyFrame]:
        ...
    
    @property
    def post_behavior(self) -> aspose.threed.animation.Extrapolation:
        ...
    
    @property
    def pre_behavior(self) -> aspose.threed.animation.Extrapolation:
        ...
    
    ...

class ExtrapolationType:
    '''Extrapolation type.'''
    
    @classmethod
    @property
    def CONSTANT(cls) -> ExtrapolationType:
        '''Value will keep the same value of the last value'''
        ...
    
    @classmethod
    @property
    def GRADIENT(cls) -> ExtrapolationType:
        '''Value will keep the same slope by time'''
        ...
    
    @classmethod
    @property
    def CYCLE(cls) -> ExtrapolationType:
        '''The repetition.'''
        ...
    
    @classmethod
    @property
    def CYCLE_RELATIVE(cls) -> ExtrapolationType:
        '''Repeat the previous pattern based on the last value'''
        ...
    
    @classmethod
    @property
    def OSCILLATE(cls) -> ExtrapolationType:
        '''The mirror repetition.'''
        ...
    
    ...

class Interpolation:
    '''The key frame's interpolation type.'''
    
    @classmethod
    @property
    def CONSTANT(cls) -> Interpolation:
        '''The value will remains constant to the value of the first point until the next segment.'''
        ...
    
    @classmethod
    @property
    def LINEAR(cls) -> Interpolation:
        '''Linear interpolation is a straight line between two points.'''
        ...
    
    @classmethod
    @property
    def BEZIER(cls) -> Interpolation:
        '''A bezier or Hermite spline.'''
        ...
    
    @classmethod
    @property
    def B_SPLINE(cls) -> Interpolation:
        '''Basis splines are defined by a series of control points, for which the curve is guaranteed only to go through the first and the last point.'''
        ...
    
    @classmethod
    @property
    def CARDINAL_SPLINE(cls) -> Interpolation:
        '''A cardinal spline is a cubic Hermite spline whose tangents are defined by the endpoints and a tension parameter.'''
        ...
    
    @classmethod
    @property
    def TCB_SPLINE(cls) -> Interpolation:
        '''Also called Kochanek-Bartels spline, the behavior of tangent is defined by tension/bias/continuity'''
        ...
    
    ...

class StepMode:
    '''Interpolation step mode.'''
    
    @classmethod
    @property
    def PREVIOUS_VALUE(cls) -> StepMode:
        '''Curve value of a segment always uses the value from previous key frame'''
        ...
    
    @classmethod
    @property
    def NEXT_VALUE(cls) -> StepMode:
        '''Curve value of a segment always uses the value from the next key frame'''
        ...
    
    ...

class WeightedMode:
    '''Weighted mode.'''
    
    @classmethod
    @property
    def NONE(cls) -> WeightedMode:
        '''Both out and next in weights are not used.
        When calculation needs tangent information, default value(0.3333) will be used.'''
        ...
    
    @classmethod
    @property
    def OUT_WEIGHT(cls) -> WeightedMode:
        '''Out(right) tangent is weighted.'''
        ...
    
    @classmethod
    @property
    def NEXT_IN_WEIGHT(cls) -> WeightedMode:
        '''Next in(left) tangent is weighted.'''
        ...
    
    @classmethod
    @property
    def BOTH(cls) -> WeightedMode:
        '''Both out and next in tangents are weighted.'''
        ...
    
    ...

