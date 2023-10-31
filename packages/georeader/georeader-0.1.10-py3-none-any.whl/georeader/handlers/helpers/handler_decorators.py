import functools
from georeader.logic.error_exceptions import LayerDoesNotExist


def pre_action_check(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'layer_name' in kwargs:
            layer_name = kwargs['layer_name']
        elif len(args) > 1:
            layer_name = args[1]
        else:
            layer_name = None
        if layer_name is not None and layer_name not in args[0].get_layers():
            raise LayerDoesNotExist(func, f'Layer {layer_name} does not exist')
        elif args[0].get_layer_count() > 1 and layer_name is None:
            raise ValueError('Layer name must be passed if more than one layer exists in file')
        value = func(*args, **kwargs)
        return value
    return wrapper
