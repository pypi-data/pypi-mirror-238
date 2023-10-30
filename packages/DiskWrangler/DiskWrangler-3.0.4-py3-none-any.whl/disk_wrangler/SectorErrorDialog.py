#======================================================================
# SectorErrorDialog.py
#======================================================================
import logging
from PyQt6 import QtGui
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QTableWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidgetItem
)
from d64py.base.Constants import SectorErrors
from disk_wrangler.SectorErrorTable import SectorErrorTable
from disk_wrangler.SectorErrorModel import SectorErrorModel

class SectorErrorDialog(QMainWindow):
    def __init__(self, parent, flags, errorMap):
        super().__init__()
        self.errorMap = errorMap
        self.realErrorMap = dict()
        row = 0
        for key in errorMap:
            if errorMap[key] in [SectorErrors.NOT_REPORTED.code, SectorErrors.NO_ERROR.code]:
                continue
            self.realErrorMap[key] = errorMap[key]

        table = SectorErrorTable(self)
        model = SectorErrorModel(self.realErrorMap)
        table.setModel(model)
        table.resizeRowsToContents()
        table.resizeColumnsToContents()
        table.verticalHeader().hide()
        table.resizeRowsToContents()
        table.resizeColumnsToContents()
        index = table.model().createIndex(0, 0)
        table.setCurrentIndex(index)

        button = QPushButton("&Close")
        button.clicked.connect(self.dismiss)
        hLayout = QHBoxLayout()
        hLayout.addStretch(1)
        hLayout.addWidget(button)
        hLayout.addStretch(1)
        vLayout = QVBoxLayout()
        vLayout.addWidget(table)
        vLayout.addLayout(hLayout)
        centralWidget = QWidget()
        centralWidget.setLayout(vLayout)
        self.setCentralWidget(centralWidget)
        self.setWindowTitle("sector errors")
        self.centerWindow()

    def centerWindow(self):
        rect = self.frameGeometry()
        center = self.screen().availableGeometry().center()
        rect.moveCenter(center)
        self.move(rect.topLeft())

    def dismiss(self):
        self.hide()
