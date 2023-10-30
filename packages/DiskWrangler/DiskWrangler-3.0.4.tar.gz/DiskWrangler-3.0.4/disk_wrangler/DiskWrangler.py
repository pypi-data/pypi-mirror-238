#======================================================================
# DiskWrangler.py
#======================================================================
from enum import Enum
from d64gfx import D64Gfx
from jproperties import Properties
import logging
import os
from pathlib import Path
import platform
import sys
import time
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QObject, QThread
from PyQt6.QtWidgets import (
    QApplication, QStyleFactory, QHeaderView, QFileDialog,
    QMessageBox, QLabel, QMenu, QStatusBar, QVBoxLayout, QHBoxLayout,
    QAbstractItemView, QWidget, QGridLayout, QGroupBox
)
from PyQt6.QtCore import Qt, QSize, QPoint
from PyQt6.QtGui import QAction, QImage, QPixmap, QFont, QFontDatabase
from importlib.metadata import version
from d64py.base.Constants import FileType, GeosFileType, SectorErrors, CharSet
from disk_wrangler.DirTableModel import DirTableModel, ModelFields
from disk_wrangler.HexDialog import HexDialog
from disk_wrangler.SectorErrorDialog import SectorErrorDialog
from disk_wrangler.BamDialog import BamDialog
from disk_wrangler.PlaintextDialog import PlaintextDialog
from disk_wrangler.FontDialog import FontDialog
from disk_wrangler.Analyzer import Analyzer
from d64py.base.DirEntry import DirEntry
from d64py.base.DiskImage import DiskImage
from d64py.exception.PartialDataException import PartialDataException
from d64py.base import Geometry
from d64py.base.Constants import ImageType
from d64py.base.TrackSector import TrackSector
from d64py.utility import D64Utility

#======================================================================

class DiskWrangler(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        logging.debug(f"available Qt styles: {QStyleFactory.keys()}")
        logging.debug(f"current style: {app.style().name()}")

        self.title = f"Cenbe's Disk Wrangler {version('DiskWrangler')}"
        self.setWindowTitle(self.title)
        namesLayout = QVBoxLayout()
        lblPermName = QLabel("Permanent name string:")
        namesLayout.addWidget(lblPermName)
        self.lblPermNameData = QLabel("")
        namesLayout.addWidget(self.lblPermNameData)
        lblParentApp = QLabel("Parent application name:")
        namesLayout.addWidget(lblParentApp)
        self.lblParentAppData = QLabel("")
        namesLayout.addWidget(self.lblParentAppData)
        namesLayout.setContentsMargins(12, 12, 12, 12)

        iconLayout = QHBoxLayout()
        self.lblIcon = QLabel("")
        self.lblIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        iconLayout.addWidget(self.lblIcon)
        iconLayout.addLayout(namesLayout)

        # FIXME lose this hideous mockery of a language
        titleStyle = """
            QGroupBox:title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                margin-left: 3px;
                margin-right: 3px;
            }
             QGroupBox {
                border: 1px ridge grey;
                border-radius: 0px;
                padding-top: 10px;
                margin-top: 5px;
            }
            """

        infoBox = QGroupBox("GEOS info:")
        if app.style().name().lower() == "fusion":
            infoBox.setStyleSheet(titleStyle)
        infoLayout = QVBoxLayout()
        infoLayout.addLayout(iconLayout)

        self.lblInfo = QLabel(" ")
        self.lblInfo.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.lblInfo.setWordWrap(True)
        self.lblInfo.setContentsMargins(6, 6, 6, 6)
        scrInfo = QtWidgets.QScrollArea()
        scrInfo.setWidgetResizable(True)
        scrInfo.setWidget(self.lblInfo)
        infoLayout.addWidget(scrInfo)
        infoBox.setLayout(infoLayout)

        diskDataLayout = QGridLayout()
        diskDataLayout.setSpacing(9)
        lblDiskName = QLabel("Disk name:")
        self.lblDiskNameData = QLabel("")
        lblImageType = QLabel("Image type:")
        self.lblImageTypeData = QLabel("")
        lblIsGeos = QLabel("GEOS disk?")
        self.lblIsGeosData = QLabel("")
        lblFiles = QLabel("Files:")
        self.lblFilesData = QLabel("")
        lblBlocksFree = QLabel("Blocks free:")
        self.lblBlocksFreeData = QLabel("")

        diskDataLayout.addWidget(lblDiskName, 0, 0)
        diskDataLayout.addWidget(self.lblDiskNameData, 0, 1)
        diskDataLayout.addWidget(lblImageType, 1, 0)
        diskDataLayout.addWidget(self.lblImageTypeData, 1, 1)
        diskDataLayout.addWidget(lblIsGeos, 2, 0)
        diskDataLayout.addWidget(self.lblIsGeosData, 2, 1)
        diskDataLayout.addWidget(lblFiles, 3, 0)
        diskDataLayout.addWidget(self.lblFilesData, 3, 1)
        diskDataLayout.addWidget(lblBlocksFree, 4, 0)
        diskDataLayout.addWidget(self.lblBlocksFreeData, 4, 1)

        diskLayout = QVBoxLayout()
        diskLayout.addStretch(1)
        diskLayout.addLayout(diskDataLayout)
        diskLayout.addStretch(1)

        topLayout = QHBoxLayout()
        topLayout.setContentsMargins(12 ,12 ,12 ,12)
        topLayout.addLayout(diskLayout)
        topLayout.addStretch(1)
        topLayout.addWidget(infoBox)

        self.tblDirEntries = QtWidgets.QTableView()
        self.tblDirEntries.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tblDirEntries.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tblDirEntries.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tblDirEntries.customContextMenuRequested.connect(self.showDirContextMenu)
        self.tblDirEntries.doubleClicked.connect(self.doDefaultDirAction)

        self.header = self.tblDirEntries.horizontalHeader()
        self.header.setHighlightSections(False)
        font = self.header.font()
        font.setBold(False)
        self.header.setFont(font)
        self.tblDirEntries.verticalHeader().hide()
        self.model = DirTableModel([])
        self.tblDirEntries.setModel(self.model)
        for i in range(len(ModelFields)):
            self.model.setHeaderData(i, Qt.Orientation.Horizontal, ModelFields.getDescriptionByCode(i))
            if i == ModelFields.FILE_NAME.code:
                self.header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
            else:
                self.header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

        self.sizeTable()
        self.centerWindow()
        self.currentImage = None

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.tblDirEntries, 1) # stretch factor

        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        self.rememberAction = QAction("&Remember directory", self)
        self.rememberAction.setCheckable(True)
        self.rememberAction.triggered.connect(self.rememberDirectory)

        self.confirmAction = QAction("&Confirm exit", self)
        self.confirmAction.setCheckable(True)
        self.confirmAction.triggered.connect(self.confirmExit)

        self.tblDirEntries.installEventFilter(self)
        self.readProps()
        self.doMenu()
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.tblDirEntries.setFocus() # so cursor up/down works at start

# ======================================================================

    def doMenu(self):
        openFileAction = QAction("&Open", self)
        openFileAction.setShortcut("Ctrl+O")
        openFileAction.setStatusTip("Open Disk Image")
        openFileAction.triggered.connect(self.showOpenDialog)

        self.startAnalysisAction = QAction("&Analyze", self)
        self.startAnalysisAction.setShortcut("Ctrl-A")
        self.startAnalysisAction.setStatusTip("Analyze disk image")
        self.startAnalysisAction.triggered.connect(self.startAnalysis)
        self.startAnalysisAction.setDisabled(True)

        self.errorsAction = QAction("Show &errors", self)
        self.errorsAction.setShortcut("Ctrl-E")
        self.errorsAction.setStatusTip("Show error sectors")
        self.errorsAction.triggered.connect(self.showErrors)
        self.errorsAction.setDisabled(True)

        self.viewDirHeaderAction = QAction("View directory &header", self)
        self.viewDirHeaderAction.setShortcut("Ctrl-H")
        self.viewDirHeaderAction.setStatusTip("View directory header (read-only)")
        self.viewDirHeaderAction.triggered.connect(self.viewDirHeader)
        self.viewDirHeaderAction.setDisabled(True)

        self.viewDirSectorsAction = QAction("View directory &sectors", self)
        self.viewDirSectorsAction.triggered.connect(self.viewDirSectors)
        self.viewDirSectorsAction.setDisabled(True)

        self.viewBamAction = QAction("View &BAM", self)
        self.viewBamAction.setShortcut("Ctrl-B")
        self.viewBamAction.setStatusTip("View Block Availability Map")
        self.viewBamAction.triggered.connect(self.viewBam)
        self.viewBamAction.setDisabled(True)

        self.exportGeoWriteAction = QAction("Export geo&Write files")
        self.exportGeoWriteAction.setShortcut("Ctrl-W")
        self.exportGeoWriteAction.setStatusTip("Save geoWrite files as text")
        self.exportGeoWriteAction.triggered.connect(self.exportGeoWrite)
        self.exportGeoWriteAction.setDisabled(True)

        exitProgramAction = QAction("E&xit", self)
        exitProgramAction.setShortcut("Ctrl-X")
        exitProgramAction.setStatusTip("Exit Program")
        exitProgramAction.triggered.connect(self.exitProgram)
        app.aboutToQuit.connect(self.windowClosing)

        helpAboutAction = QAction("&About", self)
        helpAboutAction.setStatusTip("About This Program")
        helpAboutAction.triggered.connect(self.helpAbout)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(openFileAction)
        fileMenu.addAction(self.startAnalysisAction)
        fileMenu.addAction(self.errorsAction)
        fileMenu.addAction(self.viewDirHeaderAction)
        fileMenu.addAction(self.viewDirSectorsAction)
        fileMenu.addAction(self.viewBamAction)
        fileMenu.addAction(self.exportGeoWriteAction)
        fileMenu.addAction(exitProgramAction)

        optionsMenu = menubar.addMenu("O&ptions")
        optionsMenu.addAction(self.rememberAction)
        optionsMenu.addAction(self.confirmAction)

        helpMenu = menubar.addMenu("&Help")
        helpMenu.addAction(helpAboutAction)

# ======================================================================

    def showDirContextMenu(self, pos):
        contextMenu = QMenu(self)
        viewGeosHeaderAction = QAction("View GEOS Header", self)
        viewGeosHeaderAction.triggered.connect(self.viewGeosHeader)
        contextMenu.addAction(viewGeosHeaderAction)

        viewRawDataAction = QAction("View raw data", self)
        viewRawDataAction.triggered.connect(self.viewRawData)
        contextMenu.addAction(viewRawDataAction)

        exploreFontAction = QAction("Explore font", self)
        exploreFontAction.triggered.connect(self.exploreFont)
        contextMenu.addAction(exploreFontAction)

        viewGeoWriteAction = QAction("View geoWrite file as text", self)
        viewGeoWriteAction.triggered.connect(self.viewGeoWriteFile)
        contextMenu.addAction(viewGeoWriteAction)

        saveGeoWriteAction = QAction("Save geoWrite file as text", self)
        saveGeoWriteAction.triggered.connect(self.saveGeoWriteFile)
        contextMenu.addAction(saveGeoWriteAction)

        viewAsTextAction = QAction("View as text", self)
        viewAsTextAction.triggered.connect(self.viewAsText)
        contextMenu.addAction(viewAsTextAction)

        saveAsTextAction = QAction("Save as text")
        saveAsTextAction.triggered.connect(self.saveAsText)
        contextMenu.addAction(saveAsTextAction)

        dirEntry = self.model.dirEntries[self.tblDirEntries.selectedIndexes()[0].row()]
        if dirEntry.isGeosFile():
            viewGeosHeaderAction.setDisabled(False)
            viewAsTextAction.setDisabled(True)
            saveAsTextAction.setDisabled(True)
            if not "geoWrite" in dirEntry.geosFileHeader.getParentApplicationName():
                viewGeoWriteAction.setDisabled(True)
                saveGeoWriteAction.setDisabled(True)
            else:
                viewGeoWriteAction.setDisabled(False)
                saveGeoWriteAction.setDisabled(False)
            if dirEntry.getGeosFileType() == GeosFileType.FONT:
                exploreFontAction.setDisabled(False)
            else:
                exploreFontAction.setDisabled(True)
        else:
            viewGeosHeaderAction.setDisabled(True)
            exploreFontAction.setDisabled(True)
            viewGeoWriteAction.setDisabled(True)
            saveGeoWriteAction.setDisabled(True)
            if not dirEntry.getFileType() == FileType.FILETYPE_SEQUENTIAL.code:
                viewAsTextAction.setDisabled(True)
                saveAsTextAction.setDisabled(True)
            else:
                viewAsTextAction.setDisabled(False)
                saveAsTextAction.setDisabled(False)
        contextMenu.exec(self.tblDirEntries.mapToGlobal(pos))

    def viewGeosHeader(self):
        dirEntry = self.model.dirEntries[self.tblDirEntries.selectedIndexes()[0].row()]
        ts = dirEntry. getGeosFileHeaderTrackSector()
        sector = dirEntry.getGeosFileHeader().getRaw()
        try:
            self.hexDialog = HexDialog(self, Qt.WindowType.Dialog, sector, ts, True, True)
        except Exception as exc:
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            return
        self.hexDialog.show()

    def viewRawData(self):
        dirEntry = self.model.dirEntries[self.tblDirEntries.selectedIndexes()[0].row()]
        ts = dirEntry.getFileTrackSector()
        sector = self.currentImage.readSector(ts)
        try:
            self.hexDialog = HexDialog(self, Qt.WindowType.Dialog, sector, ts, True, True)
        except Exception as exc:
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            return
        self.hexDialog.show()

    def exploreFont(self):
        dirEntry = self.model.dirEntries[self.tblDirEntries.selectedIndexes()[0].row()]
        self.fontDialog = FontDialog(self, Qt.WindowType.Dialog, dirEntry, self.currentImage)
        self.fontDialog.show()

    def viewAsText(self):
        dirEntry = self.model.dirEntries[self.tblDirEntries.selectedIndexes()[0].row()]
        try :
            # PlaintextDialog starts out unshifted:
            textLines = self.currentImage.getFileAsText(dirEntry, CharSet.PETSCII, False)
        except Exception as exc:
            logging.error(exc)
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            if isinstance(exc, PartialDataException):
                textLines = exc.getPartialData()
            else:
                raise exc

        try:
            self.plaintextDialog = PlaintextDialog(self, textLines, CharSet.PETSCII, dirEntry)
        except Exception as exc:
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            return
        self.plaintextDialog.setWindowTitle(f"{self.currentImage.getDirHeader().getDiskName().strip()}  |  {dirEntry.getDisplayFileName()}")
        self.plaintextDialog.show()
        self.plaintextDialog.txtPlaintext.setFocus()

    def saveAsText(self):
        dirEntry = self.model.dirEntries[self.tblDirEntries.selectedIndexes()[0].row()]
        fileDialog = QFileDialog(self)
        saveFileName = fileDialog.getSaveFileName(self, "Export Filename",
                        str(Path.home()) + os.sep + dirEntry.getDisplayFileName() + ".txt",
                        "*", str(Path.home()))
        if not saveFileName[0]: # user cancelled
            return

        try :
            # Using unshifted by default at this time. Make sure to request translation.
            lines = self.currentImage.getFileAsText(dirEntry, CharSet.PETSCII, False, True)
        except Exception as exc:
            logging.error(exc)
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            if isinstance(exc, PartialDataException):
                lines = exc.getPartialData()
            else:
                raise exc

        with open(saveFileName[0], "w") as f:
            for line in lines:
                f.write(line.text + "\n")
        f.close()
        QMessageBox.information(self, "Information", f"{dirEntry.getDisplayFileName()} exported to\n{saveFileName[0]}",
                                    QMessageBox.StandardButton.Ok)

    def viewGeoWriteFile(self):
        dirEntry = self.model.dirEntries[self.tblDirEntries.selectedIndexes()[0].row()]
        try:
            pages = self.currentImage.getGeoWriteFileAsLines(dirEntry)
        except Exception as exc:
            logging.error(exc)
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            if isinstance(exc, PartialDataException):
                pages = exc.getPartialData()
            else:
                raise exc
        # Just smoosh all pages into a single list of lines.
        # This is meant to be expanded upon in the future, e.g.
        # showing page breaks or pagination w/page selector.
        lines = []
        for page in pages:
            for line in page:
                lines.append(line)

        try:
            self.plaintextDialog = PlaintextDialog(self, lines, CharSet.ASCII, dirEntry)
        except Exception as exc:
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            return
        self.plaintextDialog.setWindowTitle(f"{self.currentImage.getDirHeader().getDiskName().strip()}  |  {dirEntry.getDisplayFileName()}")
        self.plaintextDialog.show()
        self.plaintextDialog.txtPlaintext.setFocus()

    def saveGeoWriteFile(self):
        dirEntry = self.model.dirEntries[self.tblDirEntries.selectedIndexes()[0].row()]
        fileDialog = QFileDialog(self)
        saveFileName = fileDialog.getSaveFileName(self, "Export Filename",
                        str(Path.home()) + os.sep + dirEntry.getDisplayFileName() + ".txt",
                        "*.txt", str(Path.home()))
        if not saveFileName[0]: # user cancelled
            return
        try:
            pages = self.currentImage.getGeoWriteFileAsLines(dirEntry)
        except Exception as exc:
            logging.error(exc)
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            if isinstance(exc, PartialDataException):
                pages = exc.getPartialData()
            else:
                raise exc
        with open(saveFileName[0], "w") as f:
            for page in pages:
                for line in page:
                    f.write(line.text + "\n")
        f.close()
        QMessageBox.information(self, "Information", f"{dirEntry.getDisplayFileName()} exported.", QMessageBox.StandardButton.Ok)

    # ======================================================================

    def eventFilter(self, obj, event): # overridden
        if obj is self.tblDirEntries and event.type() == QtCore.QEvent.Type.KeyPress:
            if event.key() in (QtCore.Qt.Key.Key_Return, QtCore.Qt.Key.Key_Enter):
                indexes = self.tblDirEntries.selectedIndexes()
                if indexes:
                    row = indexes[0].row() # table is set for single selection
                    dirEntry = self.model.dirEntries[row]
                    self.defaultDirAction(dirEntry)
        return super().eventFilter(obj, event)

    def doDefaultDirAction(self): # user hit Enter: get dir entry
        dirEntry = self.model.dirEntries[self.tblDirEntries.selectedIndexes()[0].row()]
        self.defaultDirAction(dirEntry)

    def defaultDirAction(self, dirEntry: DirEntry):
        if dirEntry.isGeosFile():
            if dirEntry.getGeosFileType() == GeosFileType.APPL_DATA \
            and dirEntry.getGeosFileHeader().getParentApplicationName().startswith("geoWrite"):
                self.viewGeoWriteFile()
                return
            elif dirEntry.getGeosFileType() == GeosFileType.FONT:
                self.exploreFont()
                return
        if not dirEntry.isGeosFile() or dirEntry.getGeosFileType() == GeosFileType.NOT_GEOS:
            if dirEntry.getFileType() == FileType.FILETYPE_SEQUENTIAL.code:
                self.viewAsText()
                return

        # fall through: view as hex
        self.viewRawData()

    # ======================================================================

    def showOpenDialog(self):
        if self.props["rememberDirectory"].data == "True":
            self.startingDir = self.props["startingDirectory"].data
            fileName = QFileDialog.getOpenFileName(self, 'Open file', self.startingDir)
        else:
            fileName = QFileDialog.getOpenFileName(self, 'Open file', str(Path.home()))
        if fileName[0]: # tuple of filename, selection criteria
            self.props["startingDirectory"] = os.path.dirname(fileName[0])
            self.writeProps()
            self.openImageFile(fileName[0])

    def startAnalysis(self):
        self.thread = QThread(self)
        self.analyzer = Analyzer(self.currentImage)
        self.analyzer.moveToThread(self.thread)
        self.thread.started.connect(self.analyzer.run)
        self.analyzer.progress.connect(self.analysisProgress)
        self.analyzer.finished.connect(self.analysisComplete)
        self.startAnalysisAction.setDisabled(True)
        self.statusBar.showMessage("starting analysis...")
        self.thread.start()

    def analysisProgress(self, message: str):
        logging.info(message)

    def analysisComplete(self, output: list):
        self.thread.quit()
        self.thread.wait()
        self.statusBar.clearMessage()
        message = output[len(output) - 1].text # last message is anomaly count
        QMessageBox.information(self, "Information", message, QMessageBox.StandardButton.Ok)
        try:
            self.plaintextDialog = PlaintextDialog(self, output, CharSet.ASCII)
        except Exception as exc:
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            return
        self.plaintextDialog.setWindowTitle(f"Analysis of {self.currentImage.getDirHeader().getDiskName().strip()}")
        self.plaintextDialog.show()
        self.plaintextDialog.txtPlaintext.setFocus()
        self.startAnalysisAction.setDisabled(False)

    def viewDirHeader(self):
        ts = Geometry.getDirHeaderTrackSector(self.currentImage.imageType)
        sector = self.currentImage.readSector(ts)
        try:
            self.hexDialog = HexDialog(self, Qt.WindowType.Dialog, sector, ts, True, True)
        except Exception as exc:
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            return
        self.hexDialog.show()

    def viewBam(self):
        try:
            self.bamDialog = BamDialog(self, Qt.WindowType.Dialog, self.currentImage)
        except Exception as exc:
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            return
        self.bamDialog.show()

    def showErrors(self):
        errorMap = self.currentImage.getSectorErrorMap()
        errors = 0
        for key in errorMap:
            if errorMap[key] in [SectorErrors.NOT_REPORTED.code, SectorErrors.NO_ERROR.code]:
                continue
            errors += 1
        if not errors:
            QMessageBox.information(self, "Information", "All errors on this disk are either\n\"no error\" or \"not reported\".", QMessageBox.StandardButton.Ok)
            return
        self.sectorErrorDialog = SectorErrorDialog(self, Qt.WindowType.Dialog, errorMap)
        self.sectorErrorDialog.show()

    def viewDirSectors(self):
        if self.currentImage is None:
            QMessageBox.warning(self, "Error", "No image loaded!", QMessageBox.StandardButton.Ok)
            return
        ts = Geometry.getFirstDirTrackSector(self.currentImage.imageType)
        sector = self.currentImage.readSector(ts)
        try:
            self.hexDialog = HexDialog(self, Qt.WindowType.Dialog, sector, ts,True, True)
        except Exception as exc:
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            return
        self.hexDialog.show()

    def exportGeoWrite(self):
        fileDialog = QFileDialog(self)
        outputDir = fileDialog.getExistingDirectory(self, "Directory for Export", str(Path.home()), QFileDialog.Option.ShowDirsOnly)
        if not outputDir: # user cancelled
            return
        logging.info(f"geoWrite export directory: {outputDir}")
        filesConverted = 0
        for dirEntry in self.model.dirEntries:
            if dirEntry.isGeosFile() and dirEntry.geosFileHeader.getParentApplicationName().startswith("geoWrite"):
                logging.info(f"exporting {dirEntry.getDisplayFileName()}")
                try:
                    pages = self.currentImage.getGeoWriteFileAsLines(dirEntry)
                except Exception as exc:
                    logging.error(exc)
                    QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
                    if isinstance(exc, PartialDataException):
                        pages = exc.getPartialData()
                    else:
                        raise exc
                with open(outputDir + os.sep + dirEntry.getDisplayFileName() + ".txt", "w") as f:
                    for page in pages:
                        for line in page:
                            f.write(line.text + "\n")
                f.close()
                filesConverted += 1
        logging.info(f"{filesConverted} geoWrite file(s) exported to {outputDir}.")
        QMessageBox.information(self, "Information", f"{filesConverted} geoWrite file(s) exported to {outputDir}.", QMessageBox.StandardButton.Ok)

    # ======================================================================

    def sizeTable(self):
        i = 0; totalWidth = 0
        while (i < self.model.columnCount(-1)):
            if i == 0:
                # 16 chars in filename, but assuming proportional font
                # totalWidth += self.model.getLongestName(self.fontMetrics())
                totalWidth += self.fontMetrics().boundingRect("M" * 14).width() # fudge factor
            else:
                totalWidth += self.header.sectionSize(i)
            i += 1
        self.tblDirEntries.setMinimumWidth(totalWidth)

    def centerWindow(self):
        rect = self.frameGeometry()
        center = self.screen().availableGeometry().center()
        rect.moveCenter(center)
        self.move(rect.topLeft())

    def rememberDirectory(self, remember: bool):
        self.props["rememberDirectory"] = str(self.rememberAction.isChecked())
        self.writeProps()

    def confirmExit(self, confirm: bool):
        self.props["confirmExit"] = str(self.confirmAction.isChecked())
        self.writeProps()

    def helpAbout(self):
        sysVersion = sys.version_info
        msg = f"{self.title}" \
                + f"\n\nRunning under Python {sysVersion.major}.{sysVersion.minor}\n" \
                + f"on {platform.system()} {platform.release()}\n\n" \
                + "code: Cenbe (built with PyCharm)\n" \
                + "quality control: Wizard The Cat"
        QMessageBox.about(self, "About", msg)

    def exitProgram(self):
        if self.props["confirmExit"].data == "True":
            button = QMessageBox.question(self, "Exit Program?", "Please Confirm")
            if button == QMessageBox.StandardButton.Yes:
                QApplication.exit(0)
            else:
                return False
        else:
            QApplication.exit(0)

    def closeEvent(self, closeEvent): # close by button or ctrl-W
        if not self.exitProgram():
            closeEvent.ignore()

    def windowClosing(self):
        try:
            self.currentImage.close()
        except:
            pass

    def openImageFile(self, fileName: str):
        try:
            path = Path(fileName)
            imageName = path.name
            logging.info("opening " + str(path))
            image = DiskImage(path)
            image.readBam() # cache it
            logging.info("reading directory...")
            dirEntries = image.getDirectory()
            msg = f"{len(dirEntries)} directory entries read."
            logging.info(msg)
            self.statusBar.showMessage(msg)
            self.model = DirTableModel(dirEntries)
            self.tblDirEntries.setModel(self.model)
            self.tblDirEntries.clicked.connect(self.rowSelected)
            self.tblDirEntries.activated.connect(self.rowSelected) # Enter pressed
            self.selectionModel = self.tblDirEntries.selectionModel()
            self.selectionModel.currentRowChanged.connect(self.rowSelected)
            self.currentPath = path
            self.currentImage = image

            self.startAnalysisAction.setDisabled(False)
            if self.currentImage.imageType == ImageType.D64_ERROR:
                self.errorsAction.setDisabled(False)
            self.viewDirHeaderAction.setDisabled(False)
            self.viewBamAction.setDisabled(False)
            self.viewDirSectorsAction.setDisabled(False)
            self.exportGeoWriteAction.setDisabled(True)
            for dirEntry in dirEntries:
                if dirEntry.isGeosFile() and dirEntry.getGeosFileHeader().getParentApplicationName().startswith("geoWrite"):
                    self.exportGeoWriteAction.setDisabled(False)
                    break
            self.lblDiskNameData.setText(self.currentImage.getDirHeader().getDiskName())
            self.lblImageTypeData.setText(self.currentImage.imageType.description)
            self.lblIsGeosData.setText("yes" if self.currentImage.isGeosImage() else "no")
            self.lblFilesData.setText(str(len(self.model.dirEntries)))
            self.lblBlocksFreeData.setText(str(self.currentImage.getBlocksFree()))
            self.sizeTable()
            if dirEntries: # i.e. if not empty
                self.tblDirEntries.selectRow(0) # auto-select first row
            else:
                self.lblPermNameData.setText(" " * 20)
                self.lblParentAppData.setText(" " * 20)
                self.lblInfo.setText(" ")
                self.lblIcon.clear()
            self.setWindowTitle(f"{self.title}  |  {imageName}")
            if self.currentImage.imageType == ImageType.D64_ERROR:
                message = f"This image is a {self.currentImage.imageType.description}."
                response = QMessageBox.question(self, "View Errors?", message)
                if response == QMessageBox.StandardButton.Yes:
                    self.showErrors()
        except Exception as exc:
            logging.error(exc)
            QMessageBox.critical(self, "Error loading image", str(exc), QMessageBox.StandardButton.Ok)

    def rowSelected(self, index):
        dirHeader = self.currentImage.getDirHeader()
        dirEntry = self.model.dirEntries[index.row()]
        geosFileHeader = self.currentImage.getGeosFileHeader(dirEntry)

        if geosFileHeader:
            self.lblPermNameData.setText(geosFileHeader.getPermanentNameString())
            if dirEntry.getGeosFileType() == GeosFileType.FONT:
                self.lblParentAppData.setText(" " * 20) # this field used for font data
            else:
                self.lblParentAppData.setText(geosFileHeader.getParentApplicationName())
            self.lblInfo.setText(geosFileHeader.getInfo())
        else:
            self.lblPermNameData.setText(" " * 20)
            self.lblParentAppData.setText(" " * 20)
            self.lblInfo.setText(" ")

        if dirEntry.getGeosFileType() == GeosFileType.NOT_GEOS:
            self.lblIcon.clear()
        else:
            iconData = dirEntry.getGeosFileHeader().getIconData()
            rawImage = QImage(QSize(24, 21), QImage.Format.Format_Mono)
            rawImage.fill(0)  # clear it
            index =  0
            while index < len(iconData):
                y = index // 3
                card = index % 3 # icon is three bytes across
                bit = 0
                while bit < 8:
                    mask = (1 << bit)
                    data = 0 if iconData[index] & mask else 1
                    x = (7 - bit) + (card * 8)
                    rawImage.setPixel(QPoint(x, y), data)
                    bit += 1
                index += 1
            rawImage = rawImage.scaled(QSize(48, 42)) # double size
            iconImage = QPixmap.fromImage(rawImage)
            self.lblIcon.setPixmap(iconImage)

    def readProps(self):
        self.props = Properties()
        try:
            with open(str(Path.home()) + os.sep + "DiskWrangler.properties", "rb") as f:
                self.props.load(f, "utf-8")
        except Exception as exc:
            logging.info("Properties file not found, creating.")
            self.props["rememberDirectory"] = "False"
            self.props["confirmExit"] = "True"
            self.writeProps()

        if self.props["rememberDirectory"].data == "True":
            self.rememberAction.setChecked(True)
        else:
            self.rememberAction.setChecked(False)

        if self.props["confirmExit"].data == "True":
            self.confirmAction.setChecked(True)
        else:
            self.confirmAction.setChecked(False)

    def writeProps(self):
        try:
            with open(str(Path.home()) + os.sep + "DiskWrangler.properties", "wb") as f:
                self.props.store(f, encoding="utf-8")
        except Exception as exc:
            QMessageBox.critical(self, "Error writing properties file", str(exc), QMessageBox.StandardButton.Ok)

#======================================================================

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S',
                        filename=str(Path.home()) + os.sep + "DiskWrangler.log", encoding="utf-8", style="{",
                        format="{asctime} {levelname} {filename}:{lineno}: {message}")
    console = logging.StreamHandler()
    logging.getLogger().addHandler(console)
    logTitle = f"Cenbe's D64 Toolkit {version('DiskWrangler')} (Python version)"
    logging.info(logTitle)
    logging.info('-' * len(logTitle))
    print(f"sys.prefix: {sys.prefix}, sys.base_prefix: {sys.base_prefix}")
    if sys.prefix == sys.base_prefix:
        logging.debug("not running in a venv")
    else:
        logging.debug("running in a venv")

app = QtWidgets.QApplication(sys.argv)
window = DiskWrangler()
window.show()
app.exec()

