"""
Load SMLM data
"""
from pathlib import Path

import locan as lc
import napari
import numpy as np

bin_size = (10, 20)
camera_pixel_size = 133

viewer = napari.current_viewer()

file_path = (
    Path(lc.__file__).resolve().parent
    / "tests/test_data"
    / "rapidSTORM_dstorm_data.txt"
)
file_type = lc.FileType.RAPIDSTORM

locdata = lc.load_locdata(path=file_path, file_type=file_type)

print(locdata.meta)

# optional kwargs for the corresponding viewer.add_* method
add_kwargs = {
    "name": Path(file_path).stem,
}

# render data
viewer, bins = lc.render_2d_napari(
    locdata=locdata,
    viewer=viewer,
    n_bins=None,
    bin_size=bin_size,
    bin_range="zero",
    bin_edges=None,
    rescale=lc.Trafo.EQUALIZE,
    cmap=lc.COLORMAP_CONTINUOUS,
    **add_kwargs,
)

if True:
    scale_factor = np.divide(bins.bin_size, camera_pixel_size)
    offset = np.multiply(scale_factor[::-1], [bins.n_bins[1] - 1, 0])

    viewer.layers[-1].scale = scale_factor
    viewer.layers[-1].rotate = ((0, -1), (1, 0))
    viewer.layers[-1].translate = offset
