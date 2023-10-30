#======================================================================
# BamDialog.py
#======================================================================
import logging
from PyQt6 import QtGui
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QHeaderView, QWidget, QHBoxLayout,
)
from disk_wrangler.BamTable import BamTable
from disk_wrangler.BamModel import BamModel

class BamDialog(QMainWindow):
    """
    Dialog for showing a disk image's Block Availability Map.
    """
    def __init__(self, parent, flags, diskImage):
        super().__init__()
        self.parent = parent
        self.diskImage = diskImage
        self.setContentsMargins(12, 12, 12, 12)
        try:
            self.table = BamTable(self)
        except Exception as exc:
            raise exc
        self.model = BamModel(diskImage)
        self.table.setModel(self.model)
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()
        index = self.table.model().createIndex(0, 0)
        self.table.setCurrentIndex(index)

        self.button = QPushButton("&Close")
        self.button.clicked.connect(self.dismiss)
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.button)
        buttonLayout.addStretch(1)

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.addWidget(self.table,2)
        layout.addLayout(buttonLayout, 1)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
        self.setWindowTitle(f"Block Availability Map for {diskImage.getDirHeader().getDiskName().strip()}")
        self.sizeTable()
        self.centerWindow()

    def sizeTable(self):
        horizontalHeader = self.table.horizontalHeader()
        verticalHeader = self.table.verticalHeader()
        i = 0; width = 0; height = 0
        width += horizontalHeader.sectionSize(0) * self.model.columnCount(-1)
        width += verticalHeader.width()
        width += self.table.verticalScrollBar().width()
        self.table.setMinimumWidth(width)
        height = verticalHeader.sectionSize(0) * 35 # leave the same for D81
        height += horizontalHeader.height()
        self.table.setMinimumHeight(height)

    def centerWindow(self):
        rect = self.frameGeometry()
        center = self.screen().availableGeometry().center()
        rect.moveCenter(center)
        self.move(rect.topLeft())

    def dismiss(self):
        self.hide()
