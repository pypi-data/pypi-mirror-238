#======================================================================
# HexDialog.py
#======================================================================
import logging
from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtCore import Qt, QRegularExpression, QItemSelectionModel
from PyQt6.QtGui import (QFont, QFontDatabase, QAction)
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QAbstractItemView, QPushButton, QRadioButton, QLabel, QLineEdit, QStatusBar,
    QMessageBox
)
from d64py.base import Geometry
from d64py.base.Chain import Chain
from d64py.base.Constants import ImageType, CharSet
from d64py.base.TrackSector import TrackSector
from disk_wrangler.HexTable import HexTable, DisplayType
from disk_wrangler.HexModel import HexModel

class HexDialog(QMainWindow):
    def __init__(self, parent, flags, data, ts: TrackSector, editable: bool, showSelector: bool):
        super().__init__()
        self.parent = parent
        self.data = data
        self.ts = ts
        self.editable = editable
        self.showSelector = showSelector

        self.setContentsMargins(12, 12, 12, 12)
        try:
            self.tblHex = HexTable(self, self.editable)
        except Exception as exc:
            raise exc
        self.hexModel = HexModel(data, self.editable, self.tblHex)
        self.tblHex.setModel(self.hexModel)
        self.tblHex.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.tblHex.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tblHex.resizeRowsToContents()
        self.tblHex.resizeColumnsToContents()
        width = self.tblHex.horizontalHeader().length() + 48 # fudge factor
        height = self.tblHex.verticalHeader().length()  + 2  # fudge factor
        self.tblHex.setMinimumSize(width, height)
        index = self.hexModel.createIndex(0, 0)
        self.tblHex.setCurrentIndex(index)

        self.chain = self.parent.currentImage.followChain(ts)
        self.chainIndex = 0

        jumpAction = QAction("&Jump link", self)
        jumpAction.setShortcut("Ctrl+J")
        jumpAction.setStatusTip("jump to track/sector under cursor")
        jumpAction.triggered.connect(self.jumpLink)

        self.nextAction = QAction("&Next in chain", self)
        self.nextAction.setShortcut("Ctrl+N")
        self.nextAction.setStatusTip("jump to next sector in chain")
        self.nextAction.triggered.connect(self.nextInChain)
        if not self.data[0]: # last sector in chain
            self.nextAction.setDisabled(True)

        self.prevAction = QAction("&Previous in chain", self)
        self.prevAction.setShortcut("Ctrl+P")
        self.prevAction.setStatusTip("jump to previous sector in chain")
        self.prevAction.triggered.connect(self.prevInChain)
        self.prevAction.setDisabled(True)

        shiftAction = QAction("use shifted &font", self)
        shiftAction.setShortcut("Ctrl+F")
        shiftAction.setStatusTip("shift font")
        shiftAction.triggered.connect(self.shiftFont)

        menubar = self.menuBar()
        viewMenu = menubar.addMenu("&View")
        viewMenu.addAction(jumpAction)
        viewMenu.addAction(self.nextAction)
        viewMenu.addAction(self.prevAction)
        optionsMenu = menubar.addMenu("O&ptions")
        optionsMenu.addAction(shiftAction)

        hexLayout = QHBoxLayout()
        hexLayout.addWidget(self.tblHex, 1) # stretch factor

        if showSelector:
            radioLayout = QVBoxLayout()
            rdoHex = QRadioButton("&Hex", self)
            rdoHex.setChecked(True)
            radioLayout.addWidget(rdoHex)
            self.rdoAscii = QRadioButton("&Ascii", self)
            # with two radio buttons, one will do for both:
            self.rdoAscii.toggled.connect(self.setInputType)
            radioLayout.addWidget(self.rdoAscii)

            tsLayout = QHBoxLayout()
            tsLayout.addStretch(2)
            self.lblTrack = QLabel("&Track:  ")
            tsLayout.addWidget(self.lblTrack)
            self.txtTrack = QLineEdit(self)
            self.txtTrack.setMaxLength(2)
            maxWidth = self.txtTrack.fontMetrics().boundingRect("WW").width()
            self.txtTrack.setMaximumWidth(maxWidth)
            self.lblTrack.setBuddy(self.txtTrack)
            tsLayout.addWidget(self.txtTrack)
            tsLayout.addStretch(1)

            self.lblSector = QLabel("&Sector:  ")
            tsLayout.addWidget(self.lblSector)
            self.txtSector= QLineEdit(self)
            self.txtSector.setMaxLength(2)
            self.txtSector.setMaximumWidth(maxWidth)
            self.lblSector.setBuddy(self.txtSector)
            tsLayout.addWidget(self.txtSector)
            tsLayout.addStretch(1)
            tsLayout.addLayout(radioLayout)
            tsLayout.addStretch(2)

            buttonLayout = QHBoxLayout()
            buttonLayout.setSpacing(24)
            buttonLayout.addStretch(3)
            btnRead = QPushButton(text="&Read", parent=self)
            btnRead.clicked.connect(self.readSector)
            buttonLayout.addWidget(btnRead)
            buttonLayout.addSpacing(2)
            btnWrite = QPushButton(text="&Write", parent=self)
            btnWrite.clicked.connect(self.writeSector)
            buttonLayout.addWidget(btnWrite)
            buttonLayout.addStretch(3)

            self.statusBar = QStatusBar()
            self.statusBar.setSizeGripEnabled(False)
            self.statusBar.setContentsMargins(0, 0, 0, 0)
            # self.statusBar.setStyleSheet("border: 1px solid;")
            self.setStatusBar(self.statusBar)

            self.setInputType()

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(hexLayout)
        if showSelector:
            mainLayout.addLayout(tsLayout)
            mainLayout.addSpacing(12)
            mainLayout.addLayout(buttonLayout)
            mainLayout.addStretch(1)

        self.setTitle()
        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)
        self.centerWindow()

    def setTitle(self):
        if self.rdoAscii.isChecked():
            tsString = str(self.ts)
            self.txtTrack.setText(f'{self.ts.track:02d}')
            self.txtSector.setText(f'{self.ts.sector:02d}')
        else:
            tsString = '$' + f'{self.ts.track:02x}' + '/' \
                     + '$' + f'{self.ts.sector:02x}'
            self.txtTrack.setText(f'{self.ts.track:02x}')
            self.txtSector.setText(f'{self.ts.sector:02x}')
        self.setWindowTitle(self.parent.currentImage.imagePath.name + "  ("
            + self.parent.currentImage.imageType.description + ", sector "
            + tsString + ")")

    def centerWindow(self):
        rect = self.frameGeometry()
        center = self.screen().availableGeometry().center()
        rect.moveCenter(center)
        self.move(rect.topLeft())

    def setInputType(self):
        if self.rdoAscii.isChecked():
            self.lblTrack.setText("&Track:  ")
            self.txtTrack.setInputMask("99") # just like COBOL!
            self.lblSector.setText("&Sector:  ")
            self.txtSector.setInputMask("99")
        else:
            self.lblTrack.setText("&Track: $")
            self.txtTrack.setInputMask("HH")
            self.lblSector.setText("&Sector: $")
            self.txtSector.setInputMask("HH")
        self.setTitle()

    def shiftFont(self):
        self.hexModel.shifted = not self.hexModel.shifted
        upperLeft = self.hexModel.createIndex(0, 0)
        lowerRight = self.hexModel.createIndex(31, 16)
        self.hexModel.dataChanged.emit(upperLeft, lowerRight)

    def jumpLink(self):
        index = self.tblHex.selectedIndexes()[0] # table is set for single selection
        if self.hexModel.displayType == DisplayType.CHAR:
            offset = ((index.row() * 8) - 9) + index.column() # convert to hex offset
        else:
            offset = index.row() * 8 + index.column()
        if offset == 255:
            QMessageBox.warning(self, "Error", "Link must be two bytes.", QMessageBox.StandardButton.Ok)
            return
        self.ts = TrackSector(self.data[offset], self.data[offset + 1])
        if not Geometry.isValidTrackSector(self.ts, self.parent.currentImage.imageType):
            QMessageBox.warning(self, "Error", "Invalid track and sector.", QMessageBox.StandardButton.Ok)
            return
        self.data = self.parent.currentImage.readSector(self.ts)
        # User may have jumped outside of or into the middle of a chain,
        # but there's no easy way to detect that, so check for one:
        self.chain = self.parent.currentImage.followChain(self.ts)
        self.chainIndex = 0
        self.prevAction.setDisabled(True)
        if len(self.chain.sectors) == 1:
            self.nextAction.setDisabled(True)
        else:
            self.nextAction.setDisabled(False)
        self.hexModel.setSectorData(self.data)
        self.setTsFields()
        index = self.hexModel.createIndex(0, 0)
        self.tblHex.selectionModel().setCurrentIndex(index, \
                    QItemSelectionModel.SelectionFlag.ClearAndSelect) # QModelIndex
        self.setTitle()

    def nextInChain(self):
        self.chainIndex += 1
        self.prevAction.setDisabled(False)
        if (self.chainIndex == len(self.chain.sectors) - 1):
            self.nextAction.setDisabled(True)
        self.ts = self.chain.sectors[self.chainIndex]
        self.data = self.parent.currentImage.readSector(self.chain.sectors[self.chainIndex])
        self.hexModel.setSectorData(self.data)
        self.setTsFields()
        index = self.hexModel.createIndex(0, 0)
        self.tblHex.selectionModel().setCurrentIndex(index, \
                    QItemSelectionModel.SelectionFlag.ClearAndSelect) # QModelIndex
        self.setTitle()

    def prevInChain(self):
        self.chainIndex -= 1
        self.nextAction.setDisabled(False)
        if self.chainIndex == 0:
            self.prevAction.setDisabled(True)
        self.ts = self.chain.sectors[self.chainIndex]
        self.data = self.parent.currentImage.readSector(self.chain.sectors[self.chainIndex])
        self.hexModel.setSectorData(self.data)
        self.setTsFields()
        index = self.hexModel.createIndex(0, 0)
        self.tblHex.selectionModel().setCurrentIndex(index, \
                    QItemSelectionModel.SelectionFlag.ClearAndSelect) # QModelIndex
        self.setTitle()

    def readSector(self):
        if not self.validateTrackSector(): # shows any error in a dialog
            return
        if self.rdoAscii.isChecked():
            logging.debug(f"readSector(): ts: {self.txtTrack.text()}/{self.txtSector.text()}")
            ts = TrackSector(self.txtTrack.text(), self.txtSector.text())
        else:
            logging.debug(f"readSector(): ts: {int(self.txtTrack.text(), 16)}/{int(self.txtSector.text(), 16)}")
            ts = TrackSector(int(self.txtTrack.text(), 16), int(self.txtSector.text(), 16))
        sector = self.parent.currentImage.readSector(ts)
        self.tblHex.model().setSectorData(sector)
        self.statusBar.showMessage(f"Sector {str(ts)} read.")
        self.tblHex.setFocus()

    def writeSector(self):
        if not self.validateTrackSector(): # shows any error in a dialog
            return
        if self.rdoAscii.isChecked():
            logging.debug(f"readSector(): ts: {self.txtTrack.text()}/{self.txtSector.text()}")
            ts = TrackSector(self.txtTrack.text(), self.txtSector.text())
        else:
            logging.debug(f"readSector(): ts: {int(self.txtTrack.text(), 16)}/{int(self.txtSector.text(), 16)}")
            ts = TrackSector(int(self.txtTrack.text(), 16), int(self.txtSector.text(), 16))
        self.parent.currentImage.writeSector(ts, self.hexModel.sector)
        self.statusBar.showMessage(f"Sector {str(ts)} written.")
        self.tblHex.setFocus()

    def setTsFields(self):
        if self.rdoAscii.isChecked():
            self.txtTrack.setText(self.ts.track)

    def validateTrackSector(self):
        invalidTrack = False; invalidSector = False; messages = []
        if not self.txtTrack.text():
            messages.append("You must enter a track number.")
        if not self.txtSector.text():
            messages.append("You must enter a sector number.")

        if not messages:
            if self.rdoAscii.isChecked():
                track = int(self.txtTrack.text())
                sector = int(self.txtSector.text())
            else:
                try:
                    track = int(self.txtTrack.text(), 16)
                except Exception as exc:
                    messages.append("Invalid track number.")
                try:
                    sector = int(self.txtSector.text(), 16)
                except Exception as exc:
                    messages.append("Invalid sector number.")

        if not messages:
            ts = TrackSector(track, sector)
            if not Geometry.isValidTrackSector(ts, self.parent.currentImage.imageType):
                messages.append("Invalid track and sector for image type.")

        if messages:
            QMessageBox.warning(self, "Error", '\n'.join(messages), QMessageBox.StandardButton.Ok)
            return False

        return True

