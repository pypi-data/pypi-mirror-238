import numpy as np

from dummy_test_plugin import (
    napari_get_reader,
    napari_get_writer,
    my_function,
    threshold
)


def test_reader(tmp_path):
    np_path = tmp_path / "test_file.npy"
    data = np.ones(shape=(10, 10))
    np.save(np_path, data)

    reader = napari_get_reader(str(np_path))
    assert callable(reader)
    read_tuples = reader(np_path)
    assert len(read_tuples) == 1
    read_tuple = read_tuples[0]
    np.testing.assert_allclose(data, read_tuple[0])

    fake_path = tmp_path / "file.fake"
    reader = napari_get_reader(str(fake_path))
    assert reader is None

def test_get_writer(tmp_path):
    np_path = tmp_path / "test_file.npy"
    data = np.ones(shape=(10, 10))
    layer_tuple = (data, {}, 'image')
    writer = napari_get_writer(str(np_path), ['image'])
    assert callable(writer)
    saved_path = writer(np_path, [layer_tuple])
    assert saved_path == np_path
    loaded_data = np.load(saved_path)
    np.testing.assert_allclose(data, loaded_data)

    fake_path = tmp_path / "file.fake"
    writer = napari_get_writer(str(fake_path), ['image'])
    assert writer is None

def test_my_function():
    im_data = np.ones(shape=(10, 10), dtype=np.uint8)
    func_result = my_function(im_data)
    assert len(func_result) == 3
    data = func_result[0]
    assert np.all(data == 255)

def test_threshold():
    widget = threshold()
    im_data = np.ones(shape=(10, 10), dtype=np.uint8)
    thresholded_im = widget(im_data, 0)
    assert np.all(thresholded_im)
