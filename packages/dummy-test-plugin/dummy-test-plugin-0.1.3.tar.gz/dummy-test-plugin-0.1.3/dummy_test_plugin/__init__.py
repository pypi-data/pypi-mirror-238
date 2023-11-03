from typing import Dict, List
import numpy as np
from napari_plugin_engine import napari_hook_implementation
from magicgui import magic_factory

#### READER ####
@napari_hook_implementation
def napari_get_reader(path: str):
    if not path.endswith(".npy"):
        return None
    return reader_function


#### SAMPLE ####
@napari_hook_implementation
def napari_provide_sample_data():
    return {
        'random data': generate_random_data,
        'random image': 'https://picsum.photos/1024',
    }


#### WRITERS ####
@napari_hook_implementation
def napari_get_writer(path: str, layer_types: List[str]):
    if not path.endswith('.npy'):
        return None

    return save_numpy


@napari_hook_implementation
def napari_write_image(path:str, data: np.ndarray, meta: Dict):
    if not path.endswith('.npy'):
        return None
    
    saved_path = save_numpy(path, [(data, meta, 'image')])
    return saved_path


### WIDGETS ###
@napari_hook_implementation
def napari_experimental_provide_function():
    return my_function


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return threshold


### HELPERS ###
def reader_function(path: str):
    data = np.load(path)
    return [(data, {}, 'image')]


def generate_random_data(shape=(512, 512)):
    data = np.random.rand(*shape)
    return [(data, {'name': 'random data'})]


def save_numpy(path, layer_tuples):
    data, _, _ = layer_tuples[0]
    np.save(path, data)
    return path


def my_function(image : 'napari.types.ImageData') -> 'napari.types.LayerDataTuple':
    result = -image
    return (result, {'colormap':'turbo'}, 'image')


@magic_factory(auto_call=True, threshold={'max': 2 ** 16})
def threshold(
    data: 'napari.types.ImageData', threshold: int
) -> 'napari.types.LabelsData':
    return (data > threshold).astype(int)

