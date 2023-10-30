# type: ignore
"""
napari-locan QWidget plugin for napari
"""
import sys
from pathlib import Path

import locan as lc
from magicgui import magic_factory
from napari.viewer import Viewer
from qtpy.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


@magic_factory(
    call_button="Load file",
    file_type={"label": "File type"},
    file_path={"label": "File path"},
    bin_size={"label": "Bin size"},
    rescale={"label": "Rescale intensity"},
)
def load_data_widget(
    napari_viewer: Viewer,
    file_type: lc.FileType = lc.FileType.RAPIDSTORM,
    file_path=None,
    bin_size=20,
    rescale=lc.Trafo.EQUALIZE,
):
    if file_path is None:
        file_path = Path.home()

    locdata = lc.load_locdata(path=file_path, file_type=file_type)

    # optional kwargs for the corresponding viewer.add_* method
    add_kwargs = {}

    # render data
    lc.render_2d_napari(
        locdata=locdata,
        viewer=napari_viewer,
        bin_size=bin_size,
        rescale=rescale,
        cmap="viridis",
        **add_kwargs,
    )

    return None
