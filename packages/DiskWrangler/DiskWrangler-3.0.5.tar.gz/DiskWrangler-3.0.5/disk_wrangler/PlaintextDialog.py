#======================================================================
# PlaintextDialog.py
#======================================================================
import logging
import os
from pathlib import Path
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import (QAction, QFont, QFontDatabase, QTextDocument,
                         QTextCursor)
from PyQt6.QtWidgets import (QMainWindow, QTextEdit, QLineEdit,
    QHBoxLayout, QVBoxLayout, QWidget, QLabel, QCheckBox, QPushButton,
    QMessageBox)
from PyQt6.QtGui import QColor
from d64py.base.DirEntry import DirEntry
from d64py.base.Constants import CharSet
from d64py.exception import PartialDataException
from d64py.utility import D64Utility, TextLine

class PlaintextDialog(QMainWindow):
    def __init__(self, parent, lines:list[TextLine], charSet:CharSet, dirEntry:DirEntry=None):
        super().__init__()
        self.parent = parent
        self.lines = lines
        self.charSet = charSet # PETSCII or ASCII
        self.shifted = False
        self.dirEntry = dirEntry
        self.setContentsMargins(12, 12, 12, 12)
        self.txtPlaintext = QTextEdit(self) # parent
        self.txtPlaintext.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
          | Qt.TextInteractionFlag.TextSelectableByKeyboard)
        self.plainFont = QFont("Monospace")
        self.plainFont.setStyleHint(QFont.StyleHint.TypeWriter)
        fontPath = str(Path(__file__).parents[0]) + os.sep + "C64_Pro_Mono-STYLE.ttf"
        fontId = QFontDatabase.addApplicationFont(fontPath)
        if fontId == -1:
            raise Exception("Can't load Style's Commodore font!")
        families = QFontDatabase.applicationFontFamilies(fontId)
        self.commodoreFont = QFont(families[0], 10)
        if charSet == CharSet.PETSCII:
            self.txtPlaintext.setFont(self.commodoreFont)
        else:
            self.txtPlaintext.setFont(self.plainFont)

        shiftAction = QAction("use shifted &font", self)
        shiftAction.setShortcut("Ctrl+F")
        shiftAction.setStatusTip("shift font")
        shiftAction.triggered.connect(self.shiftFont)
        self.txtPlaintext.addAction(shiftAction)

        metrics = self.txtPlaintext.fontMetrics()
        width = metrics.boundingRect('n' * 78).width()
        height = (metrics.boundingRect('N').height() + 1) * 40 + 1
        self.txtPlaintext.setMinimumSize(width, height)
        self.plainColor = self.txtPlaintext.textColor()

        self.showTextLines()

        hLayout = QHBoxLayout()
        lblSearch = QLabel("&Search: ")
        self.txtSearch = QLineEdit()
        self.txtSearch.returnPressed.connect(self.doSearch)
        lblSearch.setBuddy(self.txtSearch)
        self.chkCaseSensitive = QCheckBox("&Case-sensitive", self)
        self.lblShift = QLabel("(ctrl-F shifts)")
        hLayout.addWidget(lblSearch)
        hLayout.addWidget(self.txtSearch)
        hLayout.addWidget(self.chkCaseSensitive)
        hLayout.addWidget(self.lblShift)
        # only put the button for C= text files
        if charSet == CharSet.PETSCII:
            self.btnCharSet = QPushButton("&ASCII", self)
            self.btnCharSet.clicked.connect(self.switchCharSet)
            hLayout.addWidget(self.btnCharSet)
            self.lblShift.setDisabled(False)
        else:
            self.lblShift.setDisabled(True)
        vLayout = QVBoxLayout()
        vLayout.addLayout(hLayout)
        vLayout.addWidget(self.txtPlaintext)
        widget = QWidget()
        widget.setLayout(vLayout)
        self.setCentralWidget(widget)
        self.centerWindow()

    def centerWindow(self):
        rect = self.frameGeometry()
        center = self.screen().availableGeometry().center()
        rect.moveCenter(center)
        self.move(rect.topLeft())

    def showTextLines(self):
        try:
            for line in self.lines:
                if line.isErrorLine():
                    self.txtPlaintext.setTextColor(QColor(255, 48, 0))
                    self.txtPlaintext.insertPlainText(line.text + '\r')
                    self.txtPlaintext.setTextColor(self.plainColor)
                else:
                    self.txtPlaintext.insertPlainText(line.text + '\r')
        except Exception as exc:
            logging.exception(exc)
            return
        self.txtPlaintext.moveCursor(QTextCursor.MoveOperation.Start, QTextCursor.MoveMode.MoveAnchor)

    def shiftFont(self):
        if self.charSet == CharSet.ASCII:
            return
        self.shifted = not self.shifted
        self.lines = self.parent.currentImage.getFileAsText(self.dirEntry, self.charSet, self.shifted)
        self.txtPlaintext.clear()
        self.showTextLines()

    def switchCharSet(self):
        match self.charSet:
            case CharSet.ASCII:
                self.txtPlaintext.setFont(self.commodoreFont)
                self.charSet = CharSet.PETSCII
                self.lines = self.parent.currentImage.getFileAsText(self.dirEntry, self.charSet, self.shifted)
                self.lblShift.setDisabled(False)
                self.btnCharSet.setText("&ASCII")
            case CharSet.PETSCII:
                self.txtPlaintext.setFont(self.plainFont)
                self.charSet = CharSet.ASCII
                self.lines = self.parent.currentImage.getFileAsText(self.dirEntry, self.charSet)
                self.lblShift.setDisabled(True)
                self.btnCharSet.setText("&PETSCII")
        self.txtPlaintext.clear()
        self.showTextLines()

    def doSearch(self):
        match self.charSet:
            case CharSet.ASCII:
                if self.chkCaseSensitive.isChecked():
                    result = self.txtPlaintext.find(self.txtSearch.text(), QTextDocument.FindFlag.FindCaseSensitively)
                else:
                    result = self.txtPlaintext.find(self.txtSearch.text())
            case CharSet.PETSCII:
                temp = D64Utility.asciiToPetsciiString(self.txtSearch.text())
                searchTerm = ""
                for char in temp:
                    searchTerm += chr(ord(char) | 0xe100 if self.shifted else ord(char) | 0xe000)
                result = self.txtPlaintext.find(D64Utility.asciiToPetsciiString(searchTerm))
        if not result:
            QMessageBox.warning(self, "Warning", f"{self.txtSearch.text()} not found!", QMessageBox.StandardButton.Ok)
