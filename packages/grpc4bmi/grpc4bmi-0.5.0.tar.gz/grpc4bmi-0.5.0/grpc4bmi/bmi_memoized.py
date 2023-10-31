from bmipy import Bmi


class MemoizedBmi(Bmi):
    """Wrapper around Bmi object that caches the return values of almost all methods.

    Most BMI methods return same value each time it is called, so the results can be cached.
    gRPC communication is expensive and can be sped up by caching.

    The following methods are not cached:

    * initialize
    * update_*
    * finalize
    * get_current_time
    * get_value_*
    * set_value_*

    The cache is cleared when initialize() is called.

    Example:

        A gRPC BMI server is running on localhost:1234, to cache it use the following.

        >>> import grpc
        >>> from grpc4bmi.bmi_grpc_client import BmiClient
        >>> from grpc4bmi.bmi_memoized import MemoizedBmi
        >>> slow_model = BmiClient(grpc.insecure_channel("localhost:1234"))
        >>> model = MemoizedBmi(slow_model)
        >>> print(model.get_component_name())
        Hello world
        >>> # Calling second time will return cached value
        >>> # and not talk to server on "localhost:1234"
        >>> print(model.get_component_name())
        Hello world

    """
    def __init__(self, origin: Bmi):
        self.origin = origin
        self.cache = dict()

    def _cache(self, fn, arg=None, output=None):
        if fn not in self.cache:
            self.cache[fn] = dict()
        if arg not in self.cache[fn]:
            if arg is None:
                self.cache[fn][arg] = getattr(self.origin, fn)()
            else:
                if output is None:
                    self.cache[fn][arg] = getattr(self.origin, fn)(arg)
                else:
                    self.cache[fn][arg] = getattr(self.origin, fn)(arg, output)
        return self.cache[fn][arg]

    def initialize(self, filename):
        self.cache = dict()
        return self.origin.initialize(filename)

    def update(self):
        self.origin.update()

    def update_until(self, time):
        self.origin.update_until(time)

    def finalize(self):
        self.origin.finalize()

    def get_component_name(self):
        return self._cache('get_component_name')

    def get_input_item_count(self):
        return self._cache('get_input_item_count')

    def get_output_item_count(self):
        return self._cache('get_output_item_count')

    def get_input_var_names(self):
        return self._cache('get_input_var_names')

    def get_output_var_names(self):
        return self._cache('get_output_var_names')

    def get_start_time(self):
        return self._cache('get_start_time')

    def get_current_time(self):
        return self.origin.get_current_time()

    def get_end_time(self):
        return self._cache('get_end_time')

    def get_time_step(self):
        return self._cache('get_time_step')

    def get_time_units(self):
        return self._cache('get_time_units')

    def get_var_type(self, var_name):
        return self._cache('get_var_type', var_name)

    def get_var_units(self, var_name):
        return self._cache('get_var_units', var_name)

    def get_var_itemsize(self, var_name):
        return self._cache('get_var_itemsize', var_name)

    def get_var_nbytes(self, var_name):
        return self._cache('get_var_nbytes', var_name)

    def get_var_location(self, var_name):
        return self._cache('get_var_location', var_name)

    def get_var_grid(self, var_name):
        return self._cache('get_var_grid', var_name)

    def get_value(self, var_name, dest):
        return self.origin.get_value(var_name, dest)

    def get_value_ptr(self, var_name):
        return self.origin.get_value_ptr(var_name)  

    def get_value_at_indices(self, var_name, dest, inds):
        return self.origin.get_value_at_indices(var_name, dest, inds)

    def set_value(self, var_name, src):
        return self.origin.set_value(var_name, src)

    def set_value_at_indices(self, var_name, indices, src):
        return self.origin.set_value_at_indices(var_name, indices, src)

    def get_grid_shape(self, grid, shape):
        shape[:] = self._cache('get_grid_shape', grid, shape)
        return shape

    def get_grid_x(self, grid, x):
        x[:] = self._cache('get_grid_x', grid, x)
        return x

    def get_grid_y(self, grid, y):
        y[:] = self._cache('get_grid_y', grid, y)
        return y

    def get_grid_z(self, grid, z):
        z[:] = self._cache('get_grid_z', grid, z)
        return z

    def get_grid_spacing(self, grid, spacing):
        spacing[:] = self._cache('get_grid_spacing', grid, spacing)
        return spacing

    def get_grid_origin(self, grid, origin):
        origin[:] = self._cache('get_grid_origin', grid, origin)
        return origin

    def get_grid_rank(self, grid):
        return self._cache('get_grid_rank', grid)

    def get_grid_size(self, grid):
        return self._cache('get_grid_size', grid)

    def get_grid_type(self, grid):
        return self._cache('get_grid_type', grid)

    def get_grid_node_count(self, grid):
        return self._cache('get_grid_node_count', grid)

    def get_grid_edge_count(self, grid):
        return self._cache('get_grid_edge_count', grid)

    def get_grid_face_count(self, grid):
        return self._cache('get_grid_face_count', grid)

    def get_grid_edge_nodes(self, grid, edge_nodes):
        edge_nodes[:] = self._cache('get_grid_edge_nodes', grid, edge_nodes)
        return edge_nodes

    def get_grid_face_edges(self, grid, face_edges):
        face_edges[:] = self._cache('get_grid_face_edges', grid, face_edges)
        return face_edges

    def get_grid_face_nodes(self, grid, face_nodes):
        face_nodes[:] = self._cache('get_grid_face_nodes', grid, face_nodes)
        return face_nodes
    
    def get_grid_nodes_per_face(self, grid, nodes_per_face):
        nodes_per_face[:] = self._cache('get_grid_nodes_per_face', grid, nodes_per_face)
        return nodes_per_face
