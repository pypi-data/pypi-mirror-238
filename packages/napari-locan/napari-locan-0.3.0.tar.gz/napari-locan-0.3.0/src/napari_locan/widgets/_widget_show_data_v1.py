"""
QWidget plugin for showing locdata properties
"""
from __future__ import annotations

import logging
import pprint
from typing import Any

from napari.viewer import Viewer
from qtpy.QtCore import QAbstractTableModel, Qt
from qtpy.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QPlainTextEdit,
    QStackedLayout,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from napari_locan import smlm_data
from napari_locan.data_model.smlm_data import SmlmData

logger = logging.getLogger(__name__)


class TableModel(QAbstractTableModel):

    def __init__(self, data: Any) -> None:
        super().__init__()
        self._data = data

    def data(self, index, role) -> str:  # type: ignore
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, parent = None) -> int:  # type: ignore
        return self._data.shape[0]

    def columnCount(self, parent= None) -> int:  # type: ignore
        return self._data.shape[1]

    def headerData(self, section, orientation: Qt.Horizontal | Qt.Vertical, role) -> str:  # type: ignore
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class ShowDataQWidget(QWidget):  # type: ignore
    def __init__(self, napari_viewer: Viewer, smlm_data: SmlmData = smlm_data):
        super().__init__()
        self.viewer = napari_viewer
        self.smlm_data = smlm_data

        self._stackedLayout = QStackedLayout()
        self._add_display_combobox()
        self._add_summary_text()
        self._add_data_text()
        self._add_table_view()

        self._display_combobox.setCurrentIndex(0)
        self.smlm_data.index_changed_signal.emit(self.smlm_data.index)

        self._set_layout()

    def _add_display_combobox(self) -> None:
        self._display_combobox = QComboBox()
        self._display_combobox.setToolTip("Choose display layout for localization data.")
        self._display_combobox.addItems(["Summary", "Text", "Table"])
        self._display_combobox.currentIndexChanged.connect(self._stackedLayout.setCurrentIndex)

        self._display_layout = QHBoxLayout()
        self._display_layout.addWidget(self._display_combobox)

    def _add_summary_text(self) -> None:
        # QTableView
        self._summary_text_edit = QPlainTextEdit()
        self.smlm_data.index_changed_signal.connect(self._update_summary_text)

        self._stackedLayout.addWidget(self._summary_text_edit)

    def _update_summary_text(self) -> None:
        if self.smlm_data.index != -1:
            text = pprint.pformat(self.smlm_data.locdata.data.describe())  # type: ignore
            self._summary_text_edit.setPlainText(text)
        else:
            self._summary_text_edit.setPlainText("")

    def _add_data_text(self) -> None:
        self._data_text_edit = QPlainTextEdit()
        self.smlm_data.index_changed_signal.connect(self._update_data_text)

        self._stackedLayout.addWidget(self._data_text_edit)

    def _update_data_text(self) -> None:
        if self.smlm_data.index != -1:
            text = pprint.pformat(self.smlm_data.locdata.data)  # type: ignore
            self._data_text_edit.setPlainText(text)
        else:
            self._data_text_edit.setPlainText("")

    def _add_table_view(self) -> None:
        self._table_view = QTableView()
        self.smlm_data.index_changed_signal.connect(self._update_table_view)

        self._stackedLayout.addWidget(self._table_view)

    def _update_table_view(self) -> None:
        if self.smlm_data.index != -1:
            self.model = TableModel(data=self.smlm_data.locdata.data)
        else:
            self.model = None
        self._table_view.setModel(self.model)

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._display_layout)
        layout.addLayout(self._stackedLayout)
        self.setLayout(layout)
