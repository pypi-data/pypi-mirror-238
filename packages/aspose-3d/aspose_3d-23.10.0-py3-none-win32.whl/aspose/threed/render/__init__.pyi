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

class DescriptorSetUpdater:
    '''This class allows to update the :py:class:`aspose.threed.render.IDescriptorSet` in a chain operation.'''
    
    @overload
    def bind(self, buffer : aspose.threed.render.IBuffer, offset : int, size : int) -> aspose.threed.render.DescriptorSetUpdater:
        '''Bind the buffer to current descriptor set
        
        :param buffer: Which buffer to bind
        :param offset: Offset of the buffer to bind
        :param size: Size of the buffer to bind
        :returns: Return current instance for chaining operation'''
        ...
    
    @overload
    def bind(self, buffer : aspose.threed.render.IBuffer) -> aspose.threed.render.DescriptorSetUpdater:
        '''Bind the entire buffer to current descriptor
        
        :returns: Return current instance for chaining operation'''
        ...
    
    @overload
    def bind(self, binding : int, buffer : aspose.threed.render.IBuffer) -> aspose.threed.render.DescriptorSetUpdater:
        '''Bind the buffer to current descriptor set at specified binding location.
        
        :param binding: Binding location
        :param buffer: The entire buffer to bind
        :returns: Return current instance for chaining operation'''
        ...
    
    @overload
    def bind(self, binding : int, buffer : aspose.threed.render.IBuffer, offset : int, size : int) -> aspose.threed.render.DescriptorSetUpdater:
        '''Bind the buffer to current descriptor set at specified binding location.
        
        :param binding: Binding location
        :param buffer: The buffer to bind
        :param offset: Offset of the buffer to bind
        :param size: Size of the buffer to bind
        :returns: Return current instance for chaining operation'''
        ...
    
    @overload
    def bind(self, texture : aspose.threed.render.ITextureUnit) -> aspose.threed.render.DescriptorSetUpdater:
        '''Bind the texture unit to current descriptor set
        
        :param texture: The texture unit to bind
        :returns: Return current instance for chaining operation'''
        ...
    
    @overload
    def bind(self, binding : int, texture : aspose.threed.render.ITextureUnit) -> aspose.threed.render.DescriptorSetUpdater:
        '''Bind the texture unit to current descriptor set
        
        :param binding: The binding location
        :param texture: The texture unit to bind
        :returns: Return current instance for chaining operation'''
        ...
    
    ...

class DriverException:
    '''The exception raised by internal rendering drivers.'''
    
    @property
    def error_code(self) -> int:
        ...
    
    ...

class EntityRenderer:
    '''Subclass this to implement rendering for different kind of entities.'''
    
    def initialize(self, renderer : aspose.threed.render.Renderer):
        '''Initialize the entity renderer'''
        ...
    
    def reset_scene_cache(self):
        '''The scene has changed or removed, need to dispose scene-level render resources in this'''
        ...
    
    def frame_begin(self, renderer : aspose.threed.render.Renderer, render_queue : aspose.threed.render.IRenderQueue):
        '''Begin rendering a frame
        
        :param renderer: Current renderer
        :param render_queue: Render queue'''
        ...
    
    def frame_end(self, renderer : aspose.threed.render.Renderer, render_queue : aspose.threed.render.IRenderQueue):
        '''Ends rendering a frame
        
        :param renderer: Current renderer
        :param render_queue: Render queue'''
        ...
    
    def prepare_render_queue(self, renderer : aspose.threed.render.Renderer, queue : aspose.threed.render.IRenderQueue, node : aspose.threed.Node, entity : aspose.threed.Entity):
        '''Prepare rendering commands for specified node/entity pair.
        
        :param renderer: The current renderer instance
        :param queue: The render queue used to manage render tasks
        :param node: Current node
        :param entity: The entity that need to be rendered'''
        ...
    
    def render_entity(self, renderer : aspose.threed.render.Renderer, command_list : aspose.threed.render.ICommandList, node : aspose.threed.Node, renderable_resource : any, sub_entity : int):
        '''Each render task pushed to the :py:class:`aspose.threed.render.IRenderQueue` will have a corresponding RenderEntity call
        to perform the concrete rendering job.
        
        :param renderer: The renderer
        :param command_list: The commandList used to record the rendering commands
        :param node: The same node that passed to PrepareRenderQueue of the entity that will be rendered
        :param renderable_resource: The custom object that passed to IRenderQueue during the PrepareRenderQueue
        :param sub_entity: The index of the sub entity that passed to IRenderQueue'''
        ...
    
    def dispose(self):
        '''The entity renderer is being disposed, release shared resources.'''
        ...
    
    ...

class EntityRendererKey:
    '''The key of registered entity renderer'''
    
    ...

class GLSLSource(ShaderSource):
    '''The source code of shaders in GLSL'''
    
    def define_include(self, file_name : str, content : str):
        '''Define virtual file for #include in GLSL source code
        
        :param file_name: File name of the virtual file'''
        ...
    
    @property
    def compute_shader(self) -> str:
        ...
    
    @compute_shader.setter
    def compute_shader(self, value : str):
        ...
    
    @property
    def geometry_shader(self) -> str:
        ...
    
    @geometry_shader.setter
    def geometry_shader(self, value : str):
        ...
    
    @property
    def vertex_shader(self) -> str:
        ...
    
    @vertex_shader.setter
    def vertex_shader(self, value : str):
        ...
    
    @property
    def fragment_shader(self) -> str:
        ...
    
    @fragment_shader.setter
    def fragment_shader(self, value : str):
        ...
    
    ...

class IBuffer:
    '''The base interface of all managed buffers used in rendering'''
    
    def load_data(self, data : bytes):
        '''Load the data into current buffer'''
        ...
    
    @property
    def size(self) -> int:
        '''Size of this buffer in bytes'''
        ...
    
    ...

class ICommandList:
    '''Encodes a sequence of commands which will be sent to GPU to render.'''
    
    @overload
    def draw(self, start : int, count : int):
        '''Draw without index buffer'''
        ...
    
    @overload
    def draw(self):
        '''Draw without index buffer'''
        ...
    
    @overload
    def draw_index(self):
        '''Issue an indexed draw into a command list'''
        ...
    
    @overload
    def draw_index(self, start : int, count : int):
        '''Issue an indexed draw into a command list
        
        :param start: The first index to draw
        :param count: The count of indices to draw'''
        ...
    
    @overload
    def push_constants(self, stage : aspose.threed.render.ShaderStage, data : bytes):
        '''Push the constant to the pipeline
        
        :param stage: Which shader stage will consume the constant data
        :param data: The data that will be sent to the shader'''
        ...
    
    @overload
    def push_constants(self, stage : aspose.threed.render.ShaderStage, data : bytes, size : int):
        '''Push the constant to the pipeline
        
        :param stage: Which shader stage will consume the constant data
        :param data: The data that will be sent to the shader
        :param size: Bytes to write to the pipeline'''
        ...
    
    def bind_pipeline(self, pipeline : aspose.threed.render.IPipeline):
        '''Bind the pipeline instance for rendering'''
        ...
    
    def bind_vertex_buffer(self, vertex_buffer : aspose.threed.render.IVertexBuffer):
        '''Bind the vertex buffer for rendering'''
        ...
    
    def bind_index_buffer(self, index_buffer : aspose.threed.render.IIndexBuffer):
        '''Bind the index buffer for rendering'''
        ...
    
    def bind_descriptor_set(self, descriptor_set : aspose.threed.render.IDescriptorSet):
        '''Bind the descriptor set to current pipeline'''
        ...
    
    ...

class IDescriptorSet:
    '''The descriptor sets describes different resources that can be used to bind to the render pipeline like buffers, textures'''
    
    def begin_update(self) -> aspose.threed.render.DescriptorSetUpdater:
        '''Begin to update the descriptor set'''
        ...
    
    ...

class IIndexBuffer(IBuffer):
    '''The index buffer describes the geometry used in rendering pipeline.'''
    
    @overload
    def load_data(self, mesh : aspose.threed.entities.TriMesh):
        '''Load indice data from :py:class:`aspose.threed.entities.TriMesh`'''
        ...
    
    @overload
    def load_data(self, indices : List[int]):
        '''Load indice data'''
        ...
    
    @overload
    def load_data(self, indices : List[int]):
        '''Load indice data'''
        ...
    
    @overload
    def load_data(self, indices : List[int]):
        '''Load indice data'''
        ...
    
    @overload
    def load_data(self, data : bytes):
        '''Load the data into current buffer'''
        ...
    
    @property
    def index_data_type(self) -> aspose.threed.render.IndexDataType:
        ...
    
    @property
    def count(self) -> int:
        '''Gets the number of index in this buffer.'''
        ...
    
    @property
    def size(self) -> int:
        '''Size of this buffer in bytes'''
        ...
    
    ...

class IPipeline:
    '''The pre-baked sequence of operations to draw in GPU side.'''
    
    ...

class IRenderQueue:
    '''Entity renderer uses this queue to manage render tasks.'''
    
    def add(self, group_id : aspose.threed.render.RenderQueueGroupId, pipeline : aspose.threed.render.IPipeline, renderable_resource : any, sub_entity : int):
        '''Add render task to the render queue.
        
        :param group_id: Which group of the queue the render task will be in
        :param pipeline: The pipeline instance used for this render task
        :param renderable_resource: Custom object that will be sent to :py:func:`aspose.threed.render.EntityRenderer.render_entity`
        :param sub_entity: The index of sub entities, useful when the entity is consisting of more than one sub renderable components.'''
        ...
    
    ...

class IRenderTarget:
    '''The base interface of render target'''
    
    @overload
    def create_viewport(self, camera : aspose.threed.entities.Camera, background_color : aspose.threed.utilities.Vector3, rect : aspose.threed.utilities.RelativeRectangle) -> aspose.threed.render.Viewport:
        '''Create a viewport with specified background color and position/size in specified camera perspective.
        
        :param camera: The camera
        :param background_color: The background of the viewport
        :param rect: Position and size of the viewport'''
        ...
    
    @overload
    def create_viewport(self, camera : aspose.threed.entities.Camera, rect : aspose.threed.utilities.RelativeRectangle) -> aspose.threed.render.Viewport:
        '''Create a viewport with position/size in specified camera perspective.
        
        :param camera: The camera
        :param rect: Position and size of the viewport'''
        ...
    
    @overload
    def create_viewport(self, camera : aspose.threed.entities.Camera) -> aspose.threed.render.Viewport:
        '''Create a viewport in specified camera perspective.
        
        :param camera: The camera'''
        ...
    
    @property
    def size(self) -> aspose.threed.utilities.Vector2:
        '''Gets the size of the render target.'''
        ...
    
    @size.setter
    def size(self, value : aspose.threed.utilities.Vector2):
        '''Sets the size of the render target.'''
        ...
    
    @property
    def viewports(self) -> List[aspose.threed.render.Viewport]:
        '''Gets all viewports that associated with this render target.'''
        ...
    
    ...

class IRenderTexture(IRenderTarget):
    '''The interface of render texture'''
    
    @overload
    def create_viewport(self, camera : aspose.threed.entities.Camera, background_color : aspose.threed.utilities.Vector3, rect : aspose.threed.utilities.RelativeRectangle) -> aspose.threed.render.Viewport:
        '''Create a viewport with specified background color and position/size in specified camera perspective.
        
        :param camera: The camera
        :param background_color: The background of the viewport
        :param rect: Position and size of the viewport'''
        ...
    
    @overload
    def create_viewport(self, camera : aspose.threed.entities.Camera, rect : aspose.threed.utilities.RelativeRectangle) -> aspose.threed.render.Viewport:
        '''Create a viewport with position/size in specified camera perspective.
        
        :param camera: The camera
        :param rect: Position and size of the viewport'''
        ...
    
    @overload
    def create_viewport(self, camera : aspose.threed.entities.Camera) -> aspose.threed.render.Viewport:
        '''Create a viewport in specified camera perspective.
        
        :param camera: The camera'''
        ...
    
    @property
    def targets(self) -> List[aspose.threed.render.ITextureUnit]:
        '''Color output targets.'''
        ...
    
    @property
    def depth_texture(self) -> aspose.threed.render.ITextureUnit:
        ...
    
    @property
    def size(self) -> aspose.threed.utilities.Vector2:
        '''Gets the size of the render target.'''
        ...
    
    @size.setter
    def size(self, value : aspose.threed.utilities.Vector2):
        '''Sets the size of the render target.'''
        ...
    
    @property
    def viewports(self) -> List[aspose.threed.render.Viewport]:
        '''Gets all viewports that associated with this render target.'''
        ...
    
    ...

class IRenderWindow(IRenderTarget):
    '''IRenderWindow represents the native window created by operating system that supports rendering.'''
    
    @overload
    def create_viewport(self, camera : aspose.threed.entities.Camera, background_color : aspose.threed.utilities.Vector3, rect : aspose.threed.utilities.RelativeRectangle) -> aspose.threed.render.Viewport:
        '''Create a viewport with specified background color and position/size in specified camera perspective.
        
        :param camera: The camera
        :param background_color: The background of the viewport
        :param rect: Position and size of the viewport'''
        ...
    
    @overload
    def create_viewport(self, camera : aspose.threed.entities.Camera, rect : aspose.threed.utilities.RelativeRectangle) -> aspose.threed.render.Viewport:
        '''Create a viewport with position/size in specified camera perspective.
        
        :param camera: The camera
        :param rect: Position and size of the viewport'''
        ...
    
    @overload
    def create_viewport(self, camera : aspose.threed.entities.Camera) -> aspose.threed.render.Viewport:
        '''Create a viewport in specified camera perspective.
        
        :param camera: The camera'''
        ...
    
    @property
    def size(self) -> aspose.threed.utilities.Vector2:
        '''Gets the size of the render target.'''
        ...
    
    @size.setter
    def size(self, value : aspose.threed.utilities.Vector2):
        '''Sets the size of the render target.'''
        ...
    
    @property
    def viewports(self) -> List[aspose.threed.render.Viewport]:
        '''Gets all viewports that associated with this render target.'''
        ...
    
    ...

class ITexture1D(ITextureUnit):
    '''1D texture'''
    
    @overload
    def save(self, path : str, format : str):
        '''Save the texture content to external file.
        
        :param path: File name to save.
        :param format: Image format'''
        ...
    
    @overload
    def save(self, bitmap : aspose.threed.render.TextureData):
        '''Save the texture content to external file.
        
        :param bitmap: Result bitmap to save.'''
        ...
    
    def load(self, bitmap : aspose.threed.render.TextureData):
        '''Load texture content from specified Bitmap'''
        ...
    
    def to_bitmap(self) -> aspose.threed.render.TextureData:
        '''Convert the texture unit to :py:class:`aspose.threed.render.TextureData` instance'''
        ...
    
    @property
    def type(self) -> aspose.threed.render.TextureType:
        '''Gets the type of this texture unit.'''
        ...
    
    @property
    def width(self) -> int:
        '''Gets the width of this texture.'''
        ...
    
    @property
    def height(self) -> int:
        '''Gets the height of this texture.'''
        ...
    
    @property
    def depth(self) -> int:
        '''Gets the height of this texture, for none-3D texture it's always 1.'''
        ...
    
    @property
    def u_wrap(self) -> aspose.threed.shading.WrapMode:
        ...
    
    @u_wrap.setter
    def u_wrap(self, value : aspose.threed.shading.WrapMode):
        ...
    
    @property
    def v_wrap(self) -> aspose.threed.shading.WrapMode:
        ...
    
    @v_wrap.setter
    def v_wrap(self, value : aspose.threed.shading.WrapMode):
        ...
    
    @property
    def w_wrap(self) -> aspose.threed.shading.WrapMode:
        ...
    
    @w_wrap.setter
    def w_wrap(self, value : aspose.threed.shading.WrapMode):
        ...
    
    @property
    def minification(self) -> aspose.threed.shading.TextureFilter:
        '''Gets the filter mode for minification.'''
        ...
    
    @minification.setter
    def minification(self, value : aspose.threed.shading.TextureFilter):
        '''Sets the filter mode for minification.'''
        ...
    
    @property
    def magnification(self) -> aspose.threed.shading.TextureFilter:
        '''Gets the filter mode for magnification.'''
        ...
    
    @magnification.setter
    def magnification(self, value : aspose.threed.shading.TextureFilter):
        '''Sets the filter mode for magnification.'''
        ...
    
    @property
    def mipmap(self) -> aspose.threed.shading.TextureFilter:
        '''Gets the filter mode for mipmap.'''
        ...
    
    @mipmap.setter
    def mipmap(self, value : aspose.threed.shading.TextureFilter):
        '''Sets the filter mode for mipmap.'''
        ...
    
    @property
    def scroll(self) -> aspose.threed.utilities.Vector2:
        '''Gets the scroll of the UV coordinate.'''
        ...
    
    @scroll.setter
    def scroll(self, value : aspose.threed.utilities.Vector2):
        '''Sets the scroll of the UV coordinate.'''
        ...
    
    @property
    def scale(self) -> aspose.threed.utilities.Vector2:
        '''Gets the scale of the UV coordinate.'''
        ...
    
    @scale.setter
    def scale(self, value : aspose.threed.utilities.Vector2):
        '''Sets the scale of the UV coordinate.'''
        ...
    
    ...

class ITexture2D(ITextureUnit):
    '''2D texture'''
    
    @overload
    def save(self, path : str, format : str):
        '''Save the texture content to external file.
        
        :param path: File name to save.
        :param format: Image format'''
        ...
    
    @overload
    def save(self, bitmap : aspose.threed.render.TextureData):
        '''Save the texture content to external file.
        
        :param bitmap: Result bitmap to save.'''
        ...
    
    def load(self, bitmap : aspose.threed.render.TextureData):
        '''Load texture content from specified Bitmap'''
        ...
    
    def to_bitmap(self) -> aspose.threed.render.TextureData:
        '''Convert the texture unit to :py:class:`aspose.threed.render.TextureData` instance'''
        ...
    
    @property
    def type(self) -> aspose.threed.render.TextureType:
        '''Gets the type of this texture unit.'''
        ...
    
    @property
    def width(self) -> int:
        '''Gets the width of this texture.'''
        ...
    
    @property
    def height(self) -> int:
        '''Gets the height of this texture.'''
        ...
    
    @property
    def depth(self) -> int:
        '''Gets the height of this texture, for none-3D texture it's always 1.'''
        ...
    
    @property
    def u_wrap(self) -> aspose.threed.shading.WrapMode:
        ...
    
    @u_wrap.setter
    def u_wrap(self, value : aspose.threed.shading.WrapMode):
        ...
    
    @property
    def v_wrap(self) -> aspose.threed.shading.WrapMode:
        ...
    
    @v_wrap.setter
    def v_wrap(self, value : aspose.threed.shading.WrapMode):
        ...
    
    @property
    def w_wrap(self) -> aspose.threed.shading.WrapMode:
        ...
    
    @w_wrap.setter
    def w_wrap(self, value : aspose.threed.shading.WrapMode):
        ...
    
    @property
    def minification(self) -> aspose.threed.shading.TextureFilter:
        '''Gets the filter mode for minification.'''
        ...
    
    @minification.setter
    def minification(self, value : aspose.threed.shading.TextureFilter):
        '''Sets the filter mode for minification.'''
        ...
    
    @property
    def magnification(self) -> aspose.threed.shading.TextureFilter:
        '''Gets the filter mode for magnification.'''
        ...
    
    @magnification.setter
    def magnification(self, value : aspose.threed.shading.TextureFilter):
        '''Sets the filter mode for magnification.'''
        ...
    
    @property
    def mipmap(self) -> aspose.threed.shading.TextureFilter:
        '''Gets the filter mode for mipmap.'''
        ...
    
    @mipmap.setter
    def mipmap(self, value : aspose.threed.shading.TextureFilter):
        '''Sets the filter mode for mipmap.'''
        ...
    
    @property
    def scroll(self) -> aspose.threed.utilities.Vector2:
        '''Gets the scroll of the UV coordinate.'''
        ...
    
    @scroll.setter
    def scroll(self, value : aspose.threed.utilities.Vector2):
        '''Sets the scroll of the UV coordinate.'''
        ...
    
    @property
    def scale(self) -> aspose.threed.utilities.Vector2:
        '''Gets the scale of the UV coordinate.'''
        ...
    
    @scale.setter
    def scale(self, value : aspose.threed.utilities.Vector2):
        '''Sets the scale of the UV coordinate.'''
        ...
    
    ...

class ITextureCodec:
    '''Codec for textures'''
    
    def get_decoders(self) -> List[aspose.threed.render.ITextureDecoder]:
        '''Gets supported texture decoders.'''
        ...
    
    def get_encoders(self) -> List[aspose.threed.render.ITextureEncoder]:
        '''Gets supported texture encoders.'''
        ...
    
    ...

class ITextureCubemap(ITextureUnit):
    '''Cube map texture'''
    
    def load(self, face : aspose.threed.render.CubeFace, data : aspose.threed.render.TextureData):
        '''Load the data into specified face'''
        ...
    
    def save(self, side : aspose.threed.render.CubeFace, bitmap : aspose.threed.render.TextureData):
        '''Save the specified side to memory'''
        ...
    
    def to_bitmap(self, side : aspose.threed.render.CubeFace) -> aspose.threed.render.TextureData:
        '''Convert the texture unit to :py:class:`aspose.threed.render.TextureData` instance'''
        ...
    
    @property
    def type(self) -> aspose.threed.render.TextureType:
        '''Gets the type of this texture unit.'''
        ...
    
    @property
    def width(self) -> int:
        '''Gets the width of this texture.'''
        ...
    
    @property
    def height(self) -> int:
        '''Gets the height of this texture.'''
        ...
    
    @property
    def depth(self) -> int:
        '''Gets the height of this texture, for none-3D texture it's always 1.'''
        ...
    
    @property
    def u_wrap(self) -> aspose.threed.shading.WrapMode:
        ...
    
    @u_wrap.setter
    def u_wrap(self, value : aspose.threed.shading.WrapMode):
        ...
    
    @property
    def v_wrap(self) -> aspose.threed.shading.WrapMode:
        ...
    
    @v_wrap.setter
    def v_wrap(self, value : aspose.threed.shading.WrapMode):
        ...
    
    @property
    def w_wrap(self) -> aspose.threed.shading.WrapMode:
        ...
    
    @w_wrap.setter
    def w_wrap(self, value : aspose.threed.shading.WrapMode):
        ...
    
    @property
    def minification(self) -> aspose.threed.shading.TextureFilter:
        '''Gets the filter mode for minification.'''
        ...
    
    @minification.setter
    def minification(self, value : aspose.threed.shading.TextureFilter):
        '''Sets the filter mode for minification.'''
        ...
    
    @property
    def magnification(self) -> aspose.threed.shading.TextureFilter:
        '''Gets the filter mode for magnification.'''
        ...
    
    @magnification.setter
    def magnification(self, value : aspose.threed.shading.TextureFilter):
        '''Sets the filter mode for magnification.'''
        ...
    
    @property
    def mipmap(self) -> aspose.threed.shading.TextureFilter:
        '''Gets the filter mode for mipmap.'''
        ...
    
    @mipmap.setter
    def mipmap(self, value : aspose.threed.shading.TextureFilter):
        '''Sets the filter mode for mipmap.'''
        ...
    
    @property
    def scroll(self) -> aspose.threed.utilities.Vector2:
        '''Gets the scroll of the UV coordinate.'''
        ...
    
    @scroll.setter
    def scroll(self, value : aspose.threed.utilities.Vector2):
        '''Sets the scroll of the UV coordinate.'''
        ...
    
    @property
    def scale(self) -> aspose.threed.utilities.Vector2:
        '''Gets the scale of the UV coordinate.'''
        ...
    
    @scale.setter
    def scale(self, value : aspose.threed.utilities.Vector2):
        '''Sets the scale of the UV coordinate.'''
        ...
    
    ...

class ITextureDecoder:
    '''External texture decoder should implement this interface for decoding.'''
    
    def decode(self, stream : io.RawIOBase, reverse_y : bool) -> aspose.threed.render.TextureData:
        '''Decode texture from stream, return null if failed to decode.
        
        :param stream: Texture data source stream
        :param reverse_y: Flip the texture
        :returns: Decoded texture data or null if not supported.'''
        ...
    
    ...

class ITextureEncoder:
    '''External texture encoder should implement this interface for encoding.'''
    
    def encode(self, texture : aspose.threed.render.TextureData, stream : io.RawIOBase):
        '''Encode texture data into stream
        
        :param texture: The texture data to be encoded
        :param stream: The output stream'''
        ...
    
    @property
    def file_extension(self) -> str:
        ...
    
    ...

class ITextureUnit:
    ''':py:class:`aspose.threed.render.ITextureUnit` represents a texture in the memory that shared between GPU and CPU and can be sampled by the shader,
    where the :py:class:`aspose.threed.shading.Texture` only represents a reference to an external file.
    More details can be found https://en.wikipedia.org/wiki/Texture_mapping_unit'''
    
    @property
    def type(self) -> aspose.threed.render.TextureType:
        '''Gets the type of this texture unit.'''
        ...
    
    @property
    def width(self) -> int:
        '''Gets the width of this texture.'''
        ...
    
    @property
    def height(self) -> int:
        '''Gets the height of this texture.'''
        ...
    
    @property
    def depth(self) -> int:
        '''Gets the height of this texture, for none-3D texture it's always 1.'''
        ...
    
    @property
    def u_wrap(self) -> aspose.threed.shading.WrapMode:
        ...
    
    @u_wrap.setter
    def u_wrap(self, value : aspose.threed.shading.WrapMode):
        ...
    
    @property
    def v_wrap(self) -> aspose.threed.shading.WrapMode:
        ...
    
    @v_wrap.setter
    def v_wrap(self, value : aspose.threed.shading.WrapMode):
        ...
    
    @property
    def w_wrap(self) -> aspose.threed.shading.WrapMode:
        ...
    
    @w_wrap.setter
    def w_wrap(self, value : aspose.threed.shading.WrapMode):
        ...
    
    @property
    def minification(self) -> aspose.threed.shading.TextureFilter:
        '''Gets the filter mode for minification.'''
        ...
    
    @minification.setter
    def minification(self, value : aspose.threed.shading.TextureFilter):
        '''Sets the filter mode for minification.'''
        ...
    
    @property
    def magnification(self) -> aspose.threed.shading.TextureFilter:
        '''Gets the filter mode for magnification.'''
        ...
    
    @magnification.setter
    def magnification(self, value : aspose.threed.shading.TextureFilter):
        '''Sets the filter mode for magnification.'''
        ...
    
    @property
    def mipmap(self) -> aspose.threed.shading.TextureFilter:
        '''Gets the filter mode for mipmap.'''
        ...
    
    @mipmap.setter
    def mipmap(self, value : aspose.threed.shading.TextureFilter):
        '''Sets the filter mode for mipmap.'''
        ...
    
    @property
    def scroll(self) -> aspose.threed.utilities.Vector2:
        '''Gets the scroll of the UV coordinate.'''
        ...
    
    @scroll.setter
    def scroll(self, value : aspose.threed.utilities.Vector2):
        '''Sets the scroll of the UV coordinate.'''
        ...
    
    @property
    def scale(self) -> aspose.threed.utilities.Vector2:
        '''Gets the scale of the UV coordinate.'''
        ...
    
    @scale.setter
    def scale(self, value : aspose.threed.utilities.Vector2):
        '''Sets the scale of the UV coordinate.'''
        ...
    
    ...

class IVertexBuffer(IBuffer):
    '''The vertex buffer holds the polygon vertex data that will be sent to rendering pipeline'''
    
    @overload
    def load_data(self, mesh : aspose.threed.entities.TriMesh):
        '''Load vertex data from :py:class:`aspose.threed.entities.TriMesh`'''
        ...
    
    @overload
    def load_data(self, array : Array):
        ...
    
    @overload
    def load_data(self, data : bytes):
        '''Load the data into current buffer'''
        ...
    
    @property
    def vertex_declaration(self) -> aspose.threed.utilities.VertexDeclaration:
        ...
    
    @property
    def size(self) -> int:
        '''Size of this buffer in bytes'''
        ...
    
    ...

class InitializationException:
    '''Exceptions in render pipeline initialization'''
    
    ...

class PixelMapping:
    
    @property
    def stride(self) -> int:
        '''Bytes of pixels in a row.'''
        ...
    
    @property
    def height(self) -> int:
        '''Rows of the pixels'''
        ...
    
    @property
    def width(self) -> int:
        '''Columns of the pixels'''
        ...
    
    @property
    def data(self) -> bytes:
        '''The mapped bytes of pixels.'''
        ...
    
    ...

class PostProcessing(aspose.threed.A3DObject):
    '''The post-processing effects'''
    
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
    def input(self) -> aspose.threed.render.ITextureUnit:
        '''Input of this post-processing'''
        ...
    
    @input.setter
    def input(self, value : aspose.threed.render.ITextureUnit):
        '''Input of this post-processing'''
        ...
    
    ...

class PushConstant:
    '''A utility to provide data to shader through push constant.'''
    
    @overload
    def write(self, mat : aspose.threed.utilities.FMatrix4) -> aspose.threed.render.PushConstant:
        '''Write the matrix to the constant
        
        :param mat: The matrix to write'''
        ...
    
    @overload
    def write(self, n : int) -> aspose.threed.render.PushConstant:
        '''Write a int value to the constant'''
        ...
    
    @overload
    def write(self, f : float) -> aspose.threed.render.PushConstant:
        '''Write a float value to the constant'''
        ...
    
    @overload
    def write(self, vec : aspose.threed.utilities.FVector4) -> aspose.threed.render.PushConstant:
        '''Write a 4-component vector to the constant'''
        ...
    
    @overload
    def write(self, vec : aspose.threed.utilities.FVector3) -> aspose.threed.render.PushConstant:
        '''Write a 3-component vector to the constant'''
        ...
    
    @overload
    def write(self, x : float, y : float, z : float, w : float) -> aspose.threed.render.PushConstant:
        '''Write a 4-component vector to the constant'''
        ...
    
    def commit(self, stage : aspose.threed.render.ShaderStage, command_list : aspose.threed.render.ICommandList) -> aspose.threed.render.PushConstant:
        '''Commit prepared data to graphics pipeline.'''
        ...
    
    ...

class RenderFactory:
    '''RenderFactory creates all resources that represented in rendering pipeline.'''
    
    @overload
    def create_render_texture(self, parameters : aspose.threed.render.RenderParameters, targets : int, width : int, height : int) -> aspose.threed.render.IRenderTexture:
        '''Create a render target that renders to the texture
        
        :param parameters: Render parameters to create the render texture
        :param targets: How many color output targets
        :param width: The width of the render texture
        :param height: The height of the render texture'''
        ...
    
    @overload
    def create_render_texture(self, parameters : aspose.threed.render.RenderParameters, width : int, height : int) -> aspose.threed.render.IRenderTexture:
        '''Create a render target contains 1 targets that renders to the texture
        
        :param parameters: Render parameters to create the render texture
        :param width: The width of the render texture
        :param height: The height of the render texture'''
        ...
    
    @overload
    def create_texture_unit(self, texture_type : aspose.threed.render.TextureType) -> aspose.threed.render.ITextureUnit:
        '''Create a texture unit that can be accessed by shader.
        
        :param texture_type: Type of the texture'''
        ...
    
    @overload
    def create_texture_unit(self) -> aspose.threed.render.ITextureUnit:
        '''Create a 2D texture unit that can be accessed by shader.'''
        ...
    
    def create_descriptor_set(self, shader : aspose.threed.render.ShaderProgram) -> aspose.threed.render.IDescriptorSet:
        '''Create the descriptor set for specified shader program.
        
        :param shader: The shader program
        :returns: A new descriptor set instance'''
        ...
    
    def create_cube_render_texture(self, parameters : aspose.threed.render.RenderParameters, width : int, height : int) -> aspose.threed.render.IRenderTexture:
        '''Create a render target contains 1 cube texture
        
        :param parameters: Render parameters to create the render texture
        :param width: The width of the render texture
        :param height: The height of the render texture'''
        ...
    
    def create_render_window(self, parameters : aspose.threed.render.RenderParameters, handle : aspose.threed.render.WindowHandle) -> aspose.threed.render.IRenderWindow:
        '''Create a render target that renders to the native window.
        
        :param parameters: Render parameters to create the render window
        :param handle: The handle of the window to render'''
        ...
    
    def create_vertex_buffer(self, declaration : aspose.threed.utilities.VertexDeclaration) -> aspose.threed.render.IVertexBuffer:
        '''Create an :py:class:`aspose.threed.render.IVertexBuffer` instance to store polygon's vertex information.'''
        ...
    
    def create_index_buffer(self) -> aspose.threed.render.IIndexBuffer:
        '''Create an :py:class:`aspose.threed.render.IIndexBuffer` instance to store polygon's face information.'''
        ...
    
    def create_shader_program(self, shader_source : aspose.threed.render.ShaderSource) -> aspose.threed.render.ShaderProgram:
        '''Create a :py:class:`aspose.threed.render.ShaderProgram` object
        
        :param shader_source: The source code of the shader'''
        ...
    
    def create_pipeline(self, shader : aspose.threed.render.ShaderProgram, render_state : aspose.threed.render.RenderState, vertex_declaration : aspose.threed.utilities.VertexDeclaration, draw_operation : aspose.threed.render.DrawOperation) -> aspose.threed.render.IPipeline:
        '''Create a preconfigured graphics pipeline with preconfigured shader/render state/vertex declaration and draw operations.
        
        :param shader: The shader used in the rendering
        :param render_state: The render state used in the rendering
        :param vertex_declaration: The vertex declaration of input vertex data
        :param draw_operation: Draw operation
        :returns: A new pipeline instance'''
        ...
    
    def create_uniform_buffer(self, size : int) -> aspose.threed.render.IBuffer:
        '''Create a new uniform buffer in GPU side with pre-allocated size.
        
        :param size: The size of the uniform buffer
        :returns: The uniform buffer instance'''
        ...
    
    ...

class RenderParameters:
    '''Describe the parameters of the render target'''
    
    @property
    def double_buffering(self) -> bool:
        ...
    
    @double_buffering.setter
    def double_buffering(self, value : bool):
        ...
    
    @property
    def color_bits(self) -> int:
        ...
    
    @color_bits.setter
    def color_bits(self, value : int):
        ...
    
    @property
    def depth_bits(self) -> int:
        ...
    
    @depth_bits.setter
    def depth_bits(self, value : int):
        ...
    
    @property
    def stencil_bits(self) -> int:
        ...
    
    @stencil_bits.setter
    def stencil_bits(self, value : int):
        ...
    
    ...

class RenderResource:
    '''The abstract class of all render resources
    All render resources will be disposed when the renderer is released.
    Classes like :py:class:`aspose.threed.entities.Mesh`/:py:class:`aspose.threed.shading.Texture` will have a corresponding RenderResource'''
    
    ...

class RenderState:
    '''Render state for building the pipeline
    The changes made on render state will not affect the created pipeline instances.'''
    
    def compare_to(self, other : aspose.threed.render.RenderState) -> int:
        '''Compare the render state with another instance'''
        ...
    
    @property
    def blend(self) -> bool:
        '''Enable or disable the fragment blending.'''
        ...
    
    @blend.setter
    def blend(self, value : bool):
        '''Enable or disable the fragment blending.'''
        ...
    
    @property
    def blend_color(self) -> aspose.threed.utilities.FVector4:
        ...
    
    @blend_color.setter
    def blend_color(self, value : aspose.threed.utilities.FVector4):
        ...
    
    @property
    def source_blend_factor(self) -> aspose.threed.render.BlendFactor:
        ...
    
    @source_blend_factor.setter
    def source_blend_factor(self, value : aspose.threed.render.BlendFactor):
        ...
    
    @property
    def destination_blend_factor(self) -> aspose.threed.render.BlendFactor:
        ...
    
    @destination_blend_factor.setter
    def destination_blend_factor(self, value : aspose.threed.render.BlendFactor):
        ...
    
    @property
    def cull_face(self) -> bool:
        ...
    
    @cull_face.setter
    def cull_face(self, value : bool):
        ...
    
    @property
    def cull_face_mode(self) -> aspose.threed.render.CullFaceMode:
        ...
    
    @cull_face_mode.setter
    def cull_face_mode(self, value : aspose.threed.render.CullFaceMode):
        ...
    
    @property
    def front_face(self) -> aspose.threed.render.FrontFace:
        ...
    
    @front_face.setter
    def front_face(self, value : aspose.threed.render.FrontFace):
        ...
    
    @property
    def depth_test(self) -> bool:
        ...
    
    @depth_test.setter
    def depth_test(self, value : bool):
        ...
    
    @property
    def depth_mask(self) -> bool:
        ...
    
    @depth_mask.setter
    def depth_mask(self, value : bool):
        ...
    
    @property
    def depth_function(self) -> aspose.threed.render.CompareFunction:
        ...
    
    @depth_function.setter
    def depth_function(self, value : aspose.threed.render.CompareFunction):
        ...
    
    @property
    def stencil_test(self) -> bool:
        ...
    
    @stencil_test.setter
    def stencil_test(self, value : bool):
        ...
    
    @property
    def stencil_reference(self) -> int:
        ...
    
    @stencil_reference.setter
    def stencil_reference(self, value : int):
        ...
    
    @property
    def stencil_mask(self) -> int:
        ...
    
    @stencil_mask.setter
    def stencil_mask(self, value : int):
        ...
    
    @property
    def stencil_front_face(self) -> aspose.threed.render.StencilState:
        ...
    
    @property
    def stencil_back_face(self) -> aspose.threed.render.StencilState:
        ...
    
    @property
    def scissor_test(self) -> bool:
        ...
    
    @scissor_test.setter
    def scissor_test(self, value : bool):
        ...
    
    @property
    def polygon_mode(self) -> aspose.threed.render.PolygonMode:
        ...
    
    @polygon_mode.setter
    def polygon_mode(self, value : aspose.threed.render.PolygonMode):
        ...
    
    ...

class Renderer:
    '''The context about renderer.'''
    
    def clear_cache(self):
        '''Manually clear the cache.
        Aspose.3D will cache some objects like materials/geometries into internal types that compatible with the render pipeline.
        This should be manually called when scene has major changes.'''
        ...
    
    def get_post_processing(self, name : str) -> aspose.threed.render.PostProcessing:
        '''Gets a built-in post-processor that supported by the renderer.'''
        ...
    
    def execute(self, post_processing : aspose.threed.render.PostProcessing, result : aspose.threed.render.IRenderTarget):
        '''Execute an post processing on specified render target'''
        ...
    
    @staticmethod
    def create_renderer() -> aspose.threed.render.Renderer:
        '''Creates a new :py:class:`aspose.threed.render.Renderer` with default profile.'''
        ...
    
    def register_entity_renderer(self, renderer : aspose.threed.render.EntityRenderer):
        '''Register the entity renderer for specified entity'''
        ...
    
    def render(self, render_target : aspose.threed.render.IRenderTarget):
        '''Render the specified target'''
        ...
    
    @property
    def shader_set(self) -> aspose.threed.render.ShaderSet:
        ...
    
    @shader_set.setter
    def shader_set(self, value : aspose.threed.render.ShaderSet):
        ...
    
    @property
    def variables(self) -> aspose.threed.render.RendererVariableManager:
        '''Access to the internal variables used for rendering'''
        ...
    
    @property
    def preset_shaders(self) -> aspose.threed.render.PresetShaders:
        ...
    
    @preset_shaders.setter
    def preset_shaders(self, value : aspose.threed.render.PresetShaders):
        ...
    
    @property
    def render_factory(self) -> aspose.threed.render.RenderFactory:
        ...
    
    @property
    def asset_directories(self) -> List[str]:
        ...
    
    @property
    def post_processings(self) -> List[aspose.threed.render.PostProcessing]:
        ...
    
    @property
    def enable_shadows(self) -> bool:
        ...
    
    @enable_shadows.setter
    def enable_shadows(self, value : bool):
        ...
    
    @property
    def render_target(self) -> aspose.threed.render.IRenderTarget:
        ...
    
    @property
    def node(self) -> aspose.threed.Node:
        '''Gets the :py:attr:`aspose.threed.render.Renderer.node` instance used to provide world transform matrix.'''
        ...
    
    @node.setter
    def node(self, value : aspose.threed.Node):
        '''Sets the :py:attr:`aspose.threed.render.Renderer.node` instance used to provide world transform matrix.'''
        ...
    
    @property
    def frustum(self) -> aspose.threed.entities.Frustum:
        '''Gets the frustum that used to provide view matrix.'''
        ...
    
    @frustum.setter
    def frustum(self, value : aspose.threed.entities.Frustum):
        '''Sets the frustum that used to provide view matrix.'''
        ...
    
    @property
    def render_stage(self) -> aspose.threed.render.RenderStage:
        ...
    
    @property
    def material(self) -> aspose.threed.shading.Material:
        '''Gets the material that used to provide material information used by shaders.'''
        ...
    
    @material.setter
    def material(self, value : aspose.threed.shading.Material):
        '''Sets the material that used to provide material information used by shaders.'''
        ...
    
    @property
    def shader(self) -> aspose.threed.render.ShaderProgram:
        '''Gets the shader instance used for rendering the geometry.'''
        ...
    
    @shader.setter
    def shader(self, value : aspose.threed.render.ShaderProgram):
        '''Sets the shader instance used for rendering the geometry.'''
        ...
    
    @property
    def fallback_entity_renderer(self) -> aspose.threed.render.EntityRenderer:
        ...
    
    @fallback_entity_renderer.setter
    def fallback_entity_renderer(self, value : aspose.threed.render.EntityRenderer):
        ...
    
    ...

class RendererVariableManager:
    '''This class manages variables used in rendering'''
    
    @property
    def world_time(self) -> float:
        ...
    
    @property
    def shadow_caster(self) -> aspose.threed.utilities.FVector3:
        ...
    
    @shadow_caster.setter
    def shadow_caster(self, value : aspose.threed.utilities.FVector3):
        ...
    
    @property
    def shadowmap(self) -> aspose.threed.render.ITextureUnit:
        '''The depth texture used for shadow mapping'''
        ...
    
    @shadowmap.setter
    def shadowmap(self, value : aspose.threed.render.ITextureUnit):
        '''The depth texture used for shadow mapping'''
        ...
    
    @property
    def matrix_light_space(self) -> aspose.threed.utilities.FMatrix4:
        ...
    
    @matrix_light_space.setter
    def matrix_light_space(self, value : aspose.threed.utilities.FMatrix4):
        ...
    
    @property
    def matrix_view_projection(self) -> aspose.threed.utilities.FMatrix4:
        ...
    
    @property
    def matrix_world_view_projection(self) -> aspose.threed.utilities.FMatrix4:
        ...
    
    @property
    def matrix_world(self) -> aspose.threed.utilities.FMatrix4:
        ...
    
    @property
    def matrix_world_normal(self) -> aspose.threed.utilities.FMatrix4:
        ...
    
    @property
    def matrix_projection(self) -> aspose.threed.utilities.FMatrix4:
        ...
    
    @matrix_projection.setter
    def matrix_projection(self, value : aspose.threed.utilities.FMatrix4):
        ...
    
    @property
    def matrix_view(self) -> aspose.threed.utilities.FMatrix4:
        ...
    
    @matrix_view.setter
    def matrix_view(self, value : aspose.threed.utilities.FMatrix4):
        ...
    
    @property
    def camera_position(self) -> aspose.threed.utilities.FVector3:
        ...
    
    @camera_position.setter
    def camera_position(self, value : aspose.threed.utilities.FVector3):
        ...
    
    @property
    def depth_bias(self) -> float:
        ...
    
    @depth_bias.setter
    def depth_bias(self, value : float):
        ...
    
    @property
    def viewport_size(self) -> aspose.threed.utilities.FVector2:
        ...
    
    @property
    def world_ambient(self) -> aspose.threed.utilities.FVector3:
        ...
    
    ...

class SPIRVSource(ShaderSource):
    '''The compiled shader in SPIR-V format.'''
    
    @property
    def maximum_descriptor_sets(self) -> int:
        ...
    
    @maximum_descriptor_sets.setter
    def maximum_descriptor_sets(self, value : int):
        ...
    
    @property
    def compute_shader(self) -> bytes:
        ...
    
    @compute_shader.setter
    def compute_shader(self, value : bytes):
        ...
    
    @property
    def geometry_shader(self) -> bytes:
        ...
    
    @geometry_shader.setter
    def geometry_shader(self, value : bytes):
        ...
    
    @property
    def vertex_shader(self) -> bytes:
        ...
    
    @vertex_shader.setter
    def vertex_shader(self, value : bytes):
        ...
    
    @property
    def fragment_shader(self) -> bytes:
        ...
    
    @fragment_shader.setter
    def fragment_shader(self, value : bytes):
        ...
    
    ...

class ShaderException:
    '''Shader related exceptions'''
    
    ...

class ShaderProgram:
    '''The shader program'''
    
    ...

class ShaderSet:
    '''Shader programs for each kind of materials'''
    
    @property
    def lambert(self) -> aspose.threed.render.ShaderProgram:
        '''Gets the shader that used to render the lambert material'''
        ...
    
    @lambert.setter
    def lambert(self, value : aspose.threed.render.ShaderProgram):
        '''Sets the shader that used to render the lambert material'''
        ...
    
    @property
    def phong(self) -> aspose.threed.render.ShaderProgram:
        '''Gets the shader that used to render the phong material'''
        ...
    
    @phong.setter
    def phong(self, value : aspose.threed.render.ShaderProgram):
        '''Sets the shader that used to render the phong material'''
        ...
    
    @property
    def pbr(self) -> aspose.threed.render.ShaderProgram:
        '''Gets the shader that used to render the PBR material'''
        ...
    
    @pbr.setter
    def pbr(self, value : aspose.threed.render.ShaderProgram):
        '''Sets the shader that used to render the PBR material'''
        ...
    
    @property
    def fallback(self) -> aspose.threed.render.ShaderProgram:
        '''Gets the fallback shader when required shader is unavailable'''
        ...
    
    @fallback.setter
    def fallback(self, value : aspose.threed.render.ShaderProgram):
        '''Sets the fallback shader when required shader is unavailable'''
        ...
    
    ...

class ShaderSource:
    '''The source code of shader'''
    
    ...

class ShaderVariable:
    '''Shader variable'''
    
    @property
    def name(self) -> str:
        '''Gets the name of this variable'''
        ...
    
    ...

class StencilState:
    '''Stencil states per face.'''
    
    @property
    def compare(self) -> aspose.threed.render.CompareFunction:
        '''Gets the compare function used in stencil test'''
        ...
    
    @compare.setter
    def compare(self, value : aspose.threed.render.CompareFunction):
        '''Sets the compare function used in stencil test'''
        ...
    
    @property
    def fail_action(self) -> aspose.threed.render.StencilAction:
        ...
    
    @fail_action.setter
    def fail_action(self, value : aspose.threed.render.StencilAction):
        ...
    
    @property
    def depth_fail_action(self) -> aspose.threed.render.StencilAction:
        ...
    
    @depth_fail_action.setter
    def depth_fail_action(self, value : aspose.threed.render.StencilAction):
        ...
    
    @property
    def pass_action(self) -> aspose.threed.render.StencilAction:
        ...
    
    @pass_action.setter
    def pass_action(self, value : aspose.threed.render.StencilAction):
        ...
    
    ...

class TextureCodec:
    '''Class to manage encoders and decoders for textures.'''
    
    @staticmethod
    def get_supported_encoder_formats() -> List[str]:
        '''Gets all supported encoder formats'''
        ...
    
    @staticmethod
    def register_codec(codec : aspose.threed.render.ITextureCodec):
        '''Register a set of texture encoders and decoders'''
        ...
    
    @staticmethod
    def encode(texture : aspose.threed.render.TextureDatastream : io.RawIOBase, format : str):
        '''Encode texture data into stream using specified format
        
        :param texture: The texture to be encoded
        :param stream: The output stream
        :param format: The image format of encoded data, like png/jpg'''
        ...
    
    @staticmethod
    def decode(stream : io.RawIOBasereverse_y : bool) -> aspose.threed.render.TextureData:
        '''Decode texture data from stream'''
        ...
    
    ...

class TextureData:
    '''This class contains the raw data and format definition of a texture.'''
    
    @overload
    def save(self, stream : io.RawIOBase, format : str):
        '''Save texture data into specified image format
        
        :param stream: The stream that holds the saved image
        :param format: Image format, usually file extension'''
        ...
    
    @overload
    def save(self, file_name : str):
        '''Save texture data into image file
        
        :param file_name: The file name of where the image will be saved.'''
        ...
    
    @overload
    def save(self, file_name : str, format : str):
        '''Save texture data into image file
        
        :param file_name: The file name of where the image will be saved.
        :param format: Image format of the output file.'''
        ...
    
    @overload
    def map_pixels(self, map_mode : aspose.threed.render.PixelMapMode) -> aspose.threed.render.PixelMapping:
        '''Map all pixels for read/write
        
        :param map_mode: Map mode'''
        ...
    
    @overload
    def map_pixels(self, map_mode : aspose.threed.render.PixelMapMode, format : aspose.threed.render.PixelFormat) -> aspose.threed.render.PixelMapping:
        '''Map all pixels for read/write in given pixel format
        
        :param map_mode: Map mode
        :param format: Pixel format'''
        ...
    
    @overload
    def map_pixels(self, rect : aspose.threed.utilities.Rect, map_mode : aspose.threed.render.PixelMapMode, format : aspose.threed.render.PixelFormat) -> aspose.threed.render.PixelMapping:
        '''Map pixels addressed by rect for reading/writing in given pixel format
        
        :param rect: The area of pixels to be accessed
        :param map_mode: Map mode
        :param format: Pixel format
        :returns: Returns a mapping object, it should be disposed when no longer needed.'''
        ...
    
    @staticmethod
    def from_stream(stream : io.RawIOBase) -> aspose.threed.render.TextureData:
        '''Load a texture from stream'''
        ...
    
    @staticmethod
    def from_file(file_name : str) -> aspose.threed.render.TextureData:
        '''Load a texture from file'''
        ...
    
    def transform_pixel_format(self, pixel_format : aspose.threed.render.PixelFormat):
        '''Transform pixel's layout to new pixel format.
        
        :param pixel_format: Destination pixel format'''
        ...
    
    @property
    def data(self) -> bytes:
        '''Raw bytes of pixel data'''
        ...
    
    @property
    def width(self) -> int:
        '''Number of horizontal pixels'''
        ...
    
    @property
    def height(self) -> int:
        '''Number of vertical pixels'''
        ...
    
    @property
    def stride(self) -> int:
        '''Number of bytes of a scanline.'''
        ...
    
    @property
    def bytes_per_pixel(self) -> int:
        ...
    
    @property
    def pixel_format(self) -> aspose.threed.render.PixelFormat:
        ...
    
    ...

class Viewport:
    '''A :py:class:`aspose.threed.render.IRenderTarget` contains at least one viewport for rendering the scene.'''
    
    @property
    def frustum(self) -> aspose.threed.entities.Frustum:
        '''Gets the camera of this :py:class:`aspose.threed.render.Viewport`'''
        ...
    
    @frustum.setter
    def frustum(self, value : aspose.threed.entities.Frustum):
        '''Sets the camera of this :py:class:`aspose.threed.render.Viewport`'''
        ...
    
    @property
    def enabled(self) -> bool:
        '''Enable or disable this viewport.'''
        ...
    
    @enabled.setter
    def enabled(self, value : bool):
        '''Enable or disable this viewport.'''
        ...
    
    @property
    def render_target(self) -> aspose.threed.render.IRenderTarget:
        ...
    
    @property
    def area(self) -> aspose.threed.utilities.RelativeRectangle:
        '''Gets the area of the viewport in render target.'''
        ...
    
    @area.setter
    def area(self, value : aspose.threed.utilities.RelativeRectangle):
        '''Sets the area of the viewport in render target.'''
        ...
    
    @property
    def z_order(self) -> int:
        ...
    
    @z_order.setter
    def z_order(self, value : int):
        ...
    
    @property
    def background_color(self) -> aspose.threed.utilities.Vector3:
        ...
    
    @background_color.setter
    def background_color(self, value : aspose.threed.utilities.Vector3):
        ...
    
    @property
    def depth_clear(self) -> float:
        ...
    
    @depth_clear.setter
    def depth_clear(self, value : float):
        ...
    
    ...

class WindowHandle:
    '''Encapsulated window handle for different platforms.'''
    
    ...

class BlendFactor:
    '''Blend factor specify pixel arithmetic.'''
    
    @classmethod
    @property
    def ZERO(cls) -> BlendFactor:
        '''The blend factor is vec4(0)'''
        ...
    
    @classmethod
    @property
    def ONE(cls) -> BlendFactor:
        '''The blend factor is vec4(1)'''
        ...
    
    @classmethod
    @property
    def SRC_COLOR(cls) -> BlendFactor:
        '''The blend factor is src.rgba'''
        ...
    
    @classmethod
    @property
    def ONE_MINUS_SRC_COLOR(cls) -> BlendFactor:
        '''The blend factor is vec4(1) - src.rgba'''
        ...
    
    @classmethod
    @property
    def DST_COLOR(cls) -> BlendFactor:
        '''The blend factor is dst.rgba'''
        ...
    
    @classmethod
    @property
    def ONE_MINUS_DST_COLOR(cls) -> BlendFactor:
        '''The blend factor is vec4(1) - dst.rgba'''
        ...
    
    @classmethod
    @property
    def SRC_ALPHA(cls) -> BlendFactor:
        '''The blend factor is vec4(src.a)'''
        ...
    
    @classmethod
    @property
    def ONE_MINUS_SRC_ALPHA(cls) -> BlendFactor:
        '''The blend factor is vec4(1 - src.a)'''
        ...
    
    @classmethod
    @property
    def DST_ALPHA(cls) -> BlendFactor:
        '''The blend factor is vec4(dst.a)'''
        ...
    
    @classmethod
    @property
    def ONE_MINUS_DST_ALPHA(cls) -> BlendFactor:
        '''The blend factor is vec4(1 - dst.a)'''
        ...
    
    @classmethod
    @property
    def CONSTANT_COLOR(cls) -> BlendFactor:
        '''The blend factor is c where c is specified in :py:attr:`aspose.threed.render.RenderState.blend_color`'''
        ...
    
    @classmethod
    @property
    def ONE_MINUS_CONSTANT_COLOR(cls) -> BlendFactor:
        '''The blend factor is vec4(1) - c where c is specified in :py:attr:`aspose.threed.render.RenderState.blend_color`'''
        ...
    
    @classmethod
    @property
    def CONSTANT_ALPHA(cls) -> BlendFactor:
        '''The blend factor is vec4(c.a) where c is specified in :py:attr:`aspose.threed.render.RenderState.blend_color`'''
        ...
    
    @classmethod
    @property
    def ONE_MINUS_CONSTANT_ALPHA(cls) -> BlendFactor:
        '''The blend factor is vec4(1 - c.a) where c is specified in :py:attr:`aspose.threed.render.RenderState.blend_color`'''
        ...
    
    @classmethod
    @property
    def SRC_ALPHA_SATURATE(cls) -> BlendFactor:
        '''The blend factor is min(src.a, 1 - dst.a)'''
        ...
    
    ...

class CompareFunction:
    '''The compare function used in depth/stencil testing.'''
    
    @classmethod
    @property
    def NEVER(cls) -> CompareFunction:
        '''Never passes'''
        ...
    
    @classmethod
    @property
    def LESS(cls) -> CompareFunction:
        '''Pass if the incoming value is less than the stored value.'''
        ...
    
    @classmethod
    @property
    def EQUAL(cls) -> CompareFunction:
        '''Pass if the incoming value is equal to the stored value.'''
        ...
    
    @classmethod
    @property
    def L_EQUAL(cls) -> CompareFunction:
        '''Pass if the incoming value is less than or equal to the stored value.'''
        ...
    
    @classmethod
    @property
    def GREATER(cls) -> CompareFunction:
        '''Pass if the incoming value is greater than the stored value.'''
        ...
    
    @classmethod
    @property
    def NOT_EQUAL(cls) -> CompareFunction:
        '''Pass if the incoming value is not equal to the stored value.'''
        ...
    
    @classmethod
    @property
    def G_EQUAL(cls) -> CompareFunction:
        '''Pass if the incoming value is greater than or equal to the stored value.'''
        ...
    
    @classmethod
    @property
    def ALWAYS(cls) -> CompareFunction:
        '''Always passes'''
        ...
    
    ...

class CubeFace:
    '''Each face of the cube map texture'''
    
    @classmethod
    @property
    def POSITIVE_X(cls) -> CubeFace:
        '''The +X face'''
        ...
    
    @classmethod
    @property
    def NEGATIVE_X(cls) -> CubeFace:
        '''The -X face'''
        ...
    
    @classmethod
    @property
    def POSITIVE_Y(cls) -> CubeFace:
        '''The +Y face'''
        ...
    
    @classmethod
    @property
    def NEGATIVE_Y(cls) -> CubeFace:
        '''The -Y face'''
        ...
    
    @classmethod
    @property
    def POSITIVE_Z(cls) -> CubeFace:
        '''The +Z face'''
        ...
    
    @classmethod
    @property
    def NEGATIVE_Z(cls) -> CubeFace:
        '''The -Z face'''
        ...
    
    ...

class CullFaceMode:
    '''What face to cull'''
    
    @classmethod
    @property
    def BACK(cls) -> CullFaceMode:
        '''Only back faces are culled'''
        ...
    
    @classmethod
    @property
    def FRONT(cls) -> CullFaceMode:
        '''Only front faces are culled'''
        ...
    
    @classmethod
    @property
    def BOTH(cls) -> CullFaceMode:
        '''Both back/front faces are culled, doesn't affect line/point rendering.'''
        ...
    
    ...

class DrawOperation:
    '''The primitive types to render'''
    
    @classmethod
    @property
    def POINTS(cls) -> DrawOperation:
        '''Points'''
        ...
    
    @classmethod
    @property
    def LINES(cls) -> DrawOperation:
        '''Lines'''
        ...
    
    @classmethod
    @property
    def LINE_STRIP(cls) -> DrawOperation:
        '''Line strips'''
        ...
    
    @classmethod
    @property
    def TRIANGLES(cls) -> DrawOperation:
        '''Triangles'''
        ...
    
    @classmethod
    @property
    def TRIANGLE_STRIP(cls) -> DrawOperation:
        '''Triangle strips'''
        ...
    
    @classmethod
    @property
    def TRIANGLE_FAN(cls) -> DrawOperation:
        '''Triangle fan'''
        ...
    
    ...

class EntityRendererFeatures:
    '''The extra features that the entity renderer will provide'''
    
    @classmethod
    @property
    def DEFAULT(cls) -> EntityRendererFeatures:
        '''No extra features'''
        ...
    
    @classmethod
    @property
    def FRAME_BEGIN(cls) -> EntityRendererFeatures:
        '''The :py:class:`aspose.threed.render.EntityRenderer` will watch for FrameBegin callback before rendering each scene frame'''
        ...
    
    @classmethod
    @property
    def FRAME_END(cls) -> EntityRendererFeatures:
        '''The :py:class:`aspose.threed.render.EntityRenderer` will watch for FrameBegin callback after rendering each scene frame'''
        ...
    
    @classmethod
    @property
    def SHADOWMAP(cls) -> EntityRendererFeatures:
        '''This renderer can work in shadowmap mode'''
        ...
    
    ...

class FrontFace:
    '''Define front- and back-facing polygons'''
    
    @classmethod
    @property
    def CLOCKWISE(cls) -> FrontFace:
        '''Clockwise order is front face'''
        ...
    
    @classmethod
    @property
    def COUNTER_CLOCKWISE(cls) -> FrontFace:
        '''Counter-clockwise order is front face'''
        ...
    
    ...

class IndexDataType:
    '''The data type of the elements in :py:class:`aspose.threed.render.IIndexBuffer`'''
    
    @classmethod
    @property
    def INT32(cls) -> IndexDataType:
        '''The index buffer's elements are 32bit int'''
        ...
    
    @classmethod
    @property
    def INT16(cls) -> IndexDataType:
        '''The index buffer's elements are 16bit int'''
        ...
    
    ...

class PixelFormat:
    '''The pixel's format used in texture unit.'''
    
    @classmethod
    @property
    def UNKNOWN(cls) -> PixelFormat:
        '''Unknown pixel format.'''
        ...
    
    @classmethod
    @property
    def L8(cls) -> PixelFormat:
        '''8-bit pixel format, all bits luminance.'''
        ...
    
    @classmethod
    @property
    def L16(cls) -> PixelFormat:
        '''16-bit pixel format, all bits luminance.'''
        ...
    
    @classmethod
    @property
    def A8(cls) -> PixelFormat:
        '''8-bit pixel format, all bits alpha.'''
        ...
    
    @classmethod
    @property
    def A4L4(cls) -> PixelFormat:
        '''8-bit pixel format, 4 bits alpha, 4 bits luminance.'''
        ...
    
    @classmethod
    @property
    def BYTE_LA(cls) -> PixelFormat:
        '''2 byte pixel format, 1 byte luminance, 1 byte alpha'''
        ...
    
    @classmethod
    @property
    def R5G6B5(cls) -> PixelFormat:
        '''16-bit pixel format, 5 bits red, 6 bits green, 5 bits blue.'''
        ...
    
    @classmethod
    @property
    def B5G6R5(cls) -> PixelFormat:
        '''16-bit pixel format, 5 bits red, 6 bits green, 5 bits blue.'''
        ...
    
    @classmethod
    @property
    def R3G3B2(cls) -> PixelFormat:
        '''8-bit pixel format, 2 bits blue, 3 bits green, 3 bits red.'''
        ...
    
    @classmethod
    @property
    def A4R4G4B4(cls) -> PixelFormat:
        '''16-bit pixel format, 4 bits for alpha, red, green and blue.'''
        ...
    
    @classmethod
    @property
    def A1R5G5B5(cls) -> PixelFormat:
        '''16-bit pixel format, 5 bits for blue, green, red and 1 for alpha.'''
        ...
    
    @classmethod
    @property
    def R8G8B8(cls) -> PixelFormat:
        '''24-bit pixel format, 8 bits for red, green and blue.'''
        ...
    
    @classmethod
    @property
    def B8G8R8(cls) -> PixelFormat:
        '''24-bit pixel format, 8 bits for blue, green and red.'''
        ...
    
    @classmethod
    @property
    def A8R8G8B8(cls) -> PixelFormat:
        '''32-bit pixel format, 8 bits for alpha, red, green and blue.'''
        ...
    
    @classmethod
    @property
    def A8B8G8R8(cls) -> PixelFormat:
        '''32-bit pixel format, 8 bits for blue, green, red and alpha.'''
        ...
    
    @classmethod
    @property
    def B8G8R8A8(cls) -> PixelFormat:
        '''32-bit pixel format, 8 bits for blue, green, red and alpha.'''
        ...
    
    @classmethod
    @property
    def R8G8B8A8(cls) -> PixelFormat:
        '''32-bit pixel format, 8 bits for red, green, blue and alpha.'''
        ...
    
    @classmethod
    @property
    def X8R8G8B8(cls) -> PixelFormat:
        '''32-bit pixel format, 8 bits for red, 8 bits for green, 8 bits for blue like A8R8G8B8, but alpha will get discarded'''
        ...
    
    @classmethod
    @property
    def X8B8G8R8(cls) -> PixelFormat:
        '''32-bit pixel format, 8 bits for blue, 8 bits for green, 8 bits for red like A8B8G8R8, but alpha will get discarded'''
        ...
    
    @classmethod
    @property
    def A2R10G10B10(cls) -> PixelFormat:
        '''32-bit pixel format, 2 bits for alpha, 10 bits for red, green and blue.'''
        ...
    
    @classmethod
    @property
    def A2B10G10R10(cls) -> PixelFormat:
        '''32-bit pixel format, 10 bits for blue, green and red, 2 bits for alpha.'''
        ...
    
    @classmethod
    @property
    def DXT1(cls) -> PixelFormat:
        '''DDS (DirectDraw Surface) DXT1 format.'''
        ...
    
    @classmethod
    @property
    def DXT2(cls) -> PixelFormat:
        '''DDS (DirectDraw Surface) DXT2 format.'''
        ...
    
    @classmethod
    @property
    def DXT3(cls) -> PixelFormat:
        '''DDS (DirectDraw Surface) DXT3 format.'''
        ...
    
    @classmethod
    @property
    def DXT4(cls) -> PixelFormat:
        '''DDS (DirectDraw Surface) DXT4 format.'''
        ...
    
    @classmethod
    @property
    def DXT5(cls) -> PixelFormat:
        '''DDS (DirectDraw Surface) DXT5 format.'''
        ...
    
    @classmethod
    @property
    def FLOAT16_R(cls) -> PixelFormat:
        '''16-bit pixel format, 16 bits (float) for red'''
        ...
    
    @classmethod
    @property
    def FLOAT16_RGB(cls) -> PixelFormat:
        '''48-bit pixel format, 16 bits (float) for red, 16 bits (float) for green, 16 bits (float) for blue'''
        ...
    
    @classmethod
    @property
    def FLOAT16_RGBA(cls) -> PixelFormat:
        '''64-bit pixel format, 16 bits (float) for red, 16 bits (float) for green, 16 bits (float) for blue, 16 bits (float) for alpha'''
        ...
    
    @classmethod
    @property
    def FLOAT32_R(cls) -> PixelFormat:
        '''32-bit pixel format, 32 bits (float) for red'''
        ...
    
    @classmethod
    @property
    def FLOAT32_RGB(cls) -> PixelFormat:
        '''96-bit pixel format, 32 bits (float) for red, 32 bits (float) for green, 32 bits (float) for blue'''
        ...
    
    @classmethod
    @property
    def FLOAT32_RGBA(cls) -> PixelFormat:
        '''128-bit pixel format, 32 bits (float) for red, 32 bits (float) for green, 32 bits (float) for blue, 32 bits (float) for alpha'''
        ...
    
    @classmethod
    @property
    def FLOAT16_GR(cls) -> PixelFormat:
        '''32-bit, 2-channel s10e5 floating point pixel format, 16-bit green, 16-bit red'''
        ...
    
    @classmethod
    @property
    def FLOAT32_GR(cls) -> PixelFormat:
        '''64-bit, 2-channel floating point pixel format, 32-bit green, 32-bit red'''
        ...
    
    @classmethod
    @property
    def DEPTH(cls) -> PixelFormat:
        '''Depth texture format.'''
        ...
    
    @classmethod
    @property
    def SHORT_RGBA(cls) -> PixelFormat:
        '''64-bit pixel format, 16 bits for red, green, blue and alpha'''
        ...
    
    @classmethod
    @property
    def SHORT_GR(cls) -> PixelFormat:
        '''32-bit pixel format, 16-bit green, 16-bit red'''
        ...
    
    @classmethod
    @property
    def SHORT_RGB(cls) -> PixelFormat:
        '''48-bit pixel format, 16 bits for red, green and blue'''
        ...
    
    @classmethod
    @property
    def R32_UINT(cls) -> PixelFormat:
        '''32-bit pixel format, 32 bits red (unsigned int).'''
        ...
    
    @classmethod
    @property
    def R32G32_UINT(cls) -> PixelFormat:
        '''64-bit pixel format, 32 bits red (unsigned int), 32 bits blue (unsigned int).'''
        ...
    
    @classmethod
    @property
    def R32G32B32A32_UINT(cls) -> PixelFormat:
        '''128-bit pixel format, 32 bits red (unsigned int), 32 bits blue (unsigned int), 32 bits green (unsigned int), 32 bits alpha (unsigned int).'''
        ...
    
    @classmethod
    @property
    def R8(cls) -> PixelFormat:
        '''8-bit pixel format, all bits red.'''
        ...
    
    @classmethod
    @property
    def G8(cls) -> PixelFormat:
        '''8-bit pixel format, all bits green.'''
        ...
    
    @classmethod
    @property
    def B8(cls) -> PixelFormat:
        '''8-bit pixel format, all bits blue.'''
        ...
    
    ...

class PixelMapMode:
    
    @classmethod
    @property
    def READ_ONLY(cls) -> PixelMapMode:
        '''The pixels are mapped only for reading.'''
        ...
    
    @classmethod
    @property
    def READ_WRITE(cls) -> PixelMapMode:
        '''The pixels are mapped for both reading and writing.'''
        ...
    
    @classmethod
    @property
    def WRITE_ONLY(cls) -> PixelMapMode:
        '''The pixels are mapped only for writing.'''
        ...
    
    ...

class PolygonMode:
    '''The polygon rasterization mode'''
    
    @classmethod
    @property
    def POINT(cls) -> PolygonMode:
        '''Polygon control points are drawn as points.'''
        ...
    
    @classmethod
    @property
    def LINE(cls) -> PolygonMode:
        '''Boundary edges of the polygon are drawn as line segments.'''
        ...
    
    @classmethod
    @property
    def FILL(cls) -> PolygonMode:
        '''The interior of the polygon is filled.'''
        ...
    
    ...

class PresetShaders:
    '''This defines the preset internal shaders used by the renderer.'''
    
    @classmethod
    @property
    def DEFAULT(cls) -> PresetShaders:
        '''Use the default shaders for phong/lambert/pbr materials'''
        ...
    
    @classmethod
    @property
    def CUSTOMIZED(cls) -> PresetShaders:
        '''User's customized shader set'''
        ...
    
    ...

class RenderQueueGroupId:
    '''The group id of render queue'''
    
    @classmethod
    @property
    def BACKGROUND(cls) -> RenderQueueGroupId:
        '''Render queue for background'''
        ...
    
    @classmethod
    @property
    def SKIES(cls) -> RenderQueueGroupId:
        '''Render queue for skies'''
        ...
    
    @classmethod
    @property
    def GEOMETRIES(cls) -> RenderQueueGroupId:
        '''Render queue for geometries'''
        ...
    
    @classmethod
    @property
    def MAIN(cls) -> RenderQueueGroupId:
        '''Render queue for main'''
        ...
    
    @classmethod
    @property
    def OPAQUE(cls) -> RenderQueueGroupId:
        '''Render queue for opaque objects'''
        ...
    
    @classmethod
    @property
    def OVERLAY(cls) -> RenderQueueGroupId:
        '''Render queue for overlays'''
        ...
    
    ...

class RenderStage:
    '''The render stage'''
    
    @classmethod
    @property
    def IDLE(cls) -> RenderStage:
        '''Renderer is idle'''
        ...
    
    @classmethod
    @property
    def SHADOW_MAP(cls) -> RenderStage:
        '''Renderer is rendering a shadow map'''
        ...
    
    @classmethod
    @property
    def SCENE(cls) -> RenderStage:
        '''Renderer is rendering the scene'''
        ...
    
    @classmethod
    @property
    def POST_PROCESSING(cls) -> RenderStage:
        '''Renderer is rendering post processing effects.'''
        ...
    
    ...

class ShaderStage:
    '''Shader stage'''
    
    @classmethod
    @property
    def VERTEX_SHADER(cls) -> ShaderStage:
        '''Vertex shader'''
        ...
    
    @classmethod
    @property
    def FRAGMENT_SHADER(cls) -> ShaderStage:
        '''Fragment shader'''
        ...
    
    @classmethod
    @property
    def GEOMETRY_SHADER(cls) -> ShaderStage:
        '''Geometry shader'''
        ...
    
    @classmethod
    @property
    def COMPUTE_SHADER(cls) -> ShaderStage:
        '''Compute shader'''
        ...
    
    ...

class StencilAction:
    '''The stencil test actions'''
    
    @classmethod
    @property
    def KEEP(cls) -> StencilAction:
        '''Keep the current value'''
        ...
    
    @classmethod
    @property
    def ZERO(cls) -> StencilAction:
        '''Sets the stencil buffer value to 0'''
        ...
    
    @classmethod
    @property
    def REPLACE(cls) -> StencilAction:
        '''Sets the stencil buffer to ref where defined in :py:attr:`aspose.threed.render.RenderState.stencil_reference`'''
        ...
    
    @classmethod
    @property
    def INCREMENT(cls) -> StencilAction:
        '''Increments the current stencil buffer value, clamps to maximum value.'''
        ...
    
    @classmethod
    @property
    def INCREMENT_WRAP(cls) -> StencilAction:
        '''Increments the current stencil buffer value and wrap it to zero when it reaches maximum value.'''
        ...
    
    @classmethod
    @property
    def DECREMENT(cls) -> StencilAction:
        '''Increments the current stencil buffer value, clamps to 0.'''
        ...
    
    @classmethod
    @property
    def DECREMENT_WRAP(cls) -> StencilAction:
        '''Decrements the current stencil buffer value and wrap it to maximum value when it reaches zero.'''
        ...
    
    @classmethod
    @property
    def INVERT(cls) -> StencilAction:
        '''Bit-wise inverts the current stencil buffer value.'''
        ...
    
    ...

class TextureType:
    '''The type of the :py:class:`aspose.threed.render.ITextureUnit`'''
    
    @classmethod
    @property
    def TEXTURE_1D(cls) -> TextureType:
        '''1-dimensional texture'''
        ...
    
    @classmethod
    @property
    def TEXTURE_2D(cls) -> TextureType:
        '''2-dimensional texture'''
        ...
    
    @classmethod
    @property
    def TEXTURE_3D(cls) -> TextureType:
        '''3-dimensional texture'''
        ...
    
    @classmethod
    @property
    def CUBE_MAP(cls) -> TextureType:
        '''Cube map texture contains 6 2d textures'''
        ...
    
    @classmethod
    @property
    def ARRAY_2D(cls) -> TextureType:
        '''Multiple set of 2d textures'''
        ...
    
    ...

