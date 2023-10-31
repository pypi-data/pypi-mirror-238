# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2023 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a file manager for MicroPython devices.
"""

import os
import shutil

from PyQt6.QtCore import QPoint, Qt, pyqtSlot
from PyQt6.QtWidgets import (
    QDialog,
    QHeaderView,
    QInputDialog,
    QLineEdit,
    QMenu,
    QTreeWidgetItem,
    QWidget,
)

from eric7 import Globals, Preferences, Utilities
from eric7.EricGui import EricPixmapCache
from eric7.EricWidgets import EricMessageBox, EricPathPickerDialog
from eric7.EricWidgets.EricApplication import ericApp
from eric7.EricWidgets.EricFileSaveConfirmDialog import confirmOverwrite
from eric7.EricWidgets.EricPathPicker import EricPathPickerModes
from eric7.UI.DeleteFilesConfirmationDialog import DeleteFilesConfirmationDialog

from .MicroPythonFileSystemUtilities import (
    decoratedName,
    listdirStat,
    mode2string,
    mtime2string,
)
from .Ui_MicroPythonFileManagerWidget import Ui_MicroPythonFileManagerWidget


class MicroPythonFileManagerWidget(QWidget, Ui_MicroPythonFileManagerWidget):
    """
    Class implementing a file manager for MicroPython devices.
    """

    def __init__(self, fileManager, parent=None):
        """
        Constructor

        @param fileManager reference to the device file manager interface
        @type MicroPythonFileManager
        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent)
        self.setupUi(self)

        self.__repl = parent

        self.syncButton.setIcon(EricPixmapCache.getIcon("2rightarrow"))
        self.putButton.setIcon(EricPixmapCache.getIcon("1rightarrow"))
        self.putAsButton.setIcon(EricPixmapCache.getIcon("putAs"))
        self.getButton.setIcon(EricPixmapCache.getIcon("1leftarrow"))
        self.getAsButton.setIcon(EricPixmapCache.getIcon("getAs"))
        self.localUpButton.setIcon(EricPixmapCache.getIcon("1uparrow"))
        self.localHomeButton.setIcon(EricPixmapCache.getIcon("home"))
        self.localReloadButton.setIcon(EricPixmapCache.getIcon("reload"))
        self.deviceUpButton.setIcon(EricPixmapCache.getIcon("1uparrow"))
        self.deviceHomeButton.setIcon(EricPixmapCache.getIcon("home"))
        self.deviceReloadButton.setIcon(EricPixmapCache.getIcon("reload"))
        self.openButton.setIcon(EricPixmapCache.getIcon("open"))
        self.saveButton.setIcon(EricPixmapCache.getIcon("fileSave"))
        self.saveAsButton.setIcon(EricPixmapCache.getIcon("fileSaveAs"))

        isMicrobitDeviceWithMPy = self.__repl.isMicrobit()

        self.deviceUpButton.setEnabled(not isMicrobitDeviceWithMPy)
        self.deviceHomeButton.setEnabled(not isMicrobitDeviceWithMPy)

        self.putButton.setEnabled(False)
        self.putAsButton.setEnabled(False)
        self.getButton.setEnabled(False)
        self.getAsButton.setEnabled(False)

        self.openButton.setEnabled(False)
        self.saveButton.setEnabled(False)

        self.localFileTreeWidget.header().setSortIndicator(
            0, Qt.SortOrder.AscendingOrder
        )
        self.deviceFileTreeWidget.header().setSortIndicator(
            0, Qt.SortOrder.AscendingOrder
        )

        self.__progressInfoDialog = None
        self.__fileManager = fileManager

        self.__fileManager.longListFiles.connect(self.__handleLongListFiles)
        self.__fileManager.currentDir.connect(self.__handleCurrentDir)
        self.__fileManager.currentDirChanged.connect(self.__handleCurrentDir)
        self.__fileManager.putFileDone.connect(self.__newDeviceList)
        self.__fileManager.getFileDone.connect(self.__handleGetDone)
        self.__fileManager.rsyncDone.connect(self.__handleRsyncDone)
        self.__fileManager.rsyncProgressMessage.connect(
            self.__handleRsyncProgressMessage
        )
        self.__fileManager.removeDirectoryDone.connect(self.__newDeviceList)
        self.__fileManager.createDirectoryDone.connect(self.__newDeviceList)
        self.__fileManager.deleteFileDone.connect(self.__newDeviceList)
        self.__fileManager.fsinfoDone.connect(self.__fsInfoResultReceived)
        self.__fileManager.putDataDone.connect(self.__newDeviceList)

        self.__fileManager.error.connect(self.__handleError)

        self.localFileTreeWidget.customContextMenuRequested.connect(
            self.__showLocalContextMenu
        )
        self.deviceFileTreeWidget.customContextMenuRequested.connect(
            self.__showDeviceContextMenu
        )

        self.__localMenu = QMenu(self)
        self.__localMenu.addAction(
            self.tr("Change Directory"), self.__changeLocalDirectory
        )
        self.__localMenu.addAction(
            self.tr("Create Directory"), self.__createLocalDirectory
        )
        self.__localDelDirTreeAct = self.__localMenu.addAction(
            self.tr("Delete Directory Tree"), self.__deleteLocalDirectoryTree
        )
        self.__localMenu.addSeparator()
        self.__localDelFileAct = self.__localMenu.addAction(
            self.tr("Delete File"), self.__deleteLocalFile
        )
        self.__localMenu.addSeparator()
        act = self.__localMenu.addAction(self.tr("Show Hidden Files"))
        act.setCheckable(True)
        act.setChecked(Preferences.getMicroPython("ShowHiddenLocal"))
        act.triggered[bool].connect(self.__localHiddenChanged)

        self.__deviceMenu = QMenu(self)
        if not isMicrobitDeviceWithMPy:
            self.__deviceMenu.addAction(
                self.tr("Change Directory"), self.__changeDeviceDirectory
            )
            self.__deviceMenu.addAction(
                self.tr("Create Directory"), self.__createDeviceDirectory
            )
            self.__devDelDirAct = self.__deviceMenu.addAction(
                self.tr("Delete Directory"), self.__deleteDeviceDirectory
            )
            self.__devDelDirTreeAct = self.__deviceMenu.addAction(
                self.tr("Delete Directory Tree"), self.__deleteDeviceDirectoryTree
            )
            self.__deviceMenu.addSeparator()
        self.__devDelFileAct = self.__deviceMenu.addAction(
            self.tr("Delete File"), self.__deleteDeviceFile
        )
        self.__deviceMenu.addSeparator()
        act = self.__deviceMenu.addAction(self.tr("Show Hidden Files"))
        act.setCheckable(True)
        act.setChecked(Preferences.getMicroPython("ShowHiddenDevice"))
        act.triggered[bool].connect(self.__deviceHiddenChanged)
        if not isMicrobitDeviceWithMPy:
            self.__deviceMenu.addSeparator()
            self.__deviceMenu.addAction(
                self.tr("Show Filesystem Info"), self.__showFileSystemInfo
            )

    def start(self):
        """
        Public method to start the widget.
        """
        dirname = ""
        vm = ericApp().getObject("ViewManager")
        aw = vm.activeWindow()
        if aw and aw.isLocalFile():
            dirname = os.path.dirname(aw.getFileName())
        if not dirname:
            dirname = (
                Preferences.getMicroPython("MpyWorkspace")
                or Preferences.getMultiProject("Workspace")
                or os.path.expanduser("~")
            )
        self.__listLocalFiles(dirname)

        if self.__repl.deviceSupportsLocalFileAccess():
            dirname = self.__repl.getDeviceWorkspace()
            if dirname:
                self.__listLocalFiles(dirname, True)
                return

        # list files via device script
        self.__fileManager.pwd()

    def stop(self):
        """
        Public method to stop the widget.
        """
        pass

    @pyqtSlot(str, str)
    def __handleError(self, method, error):
        """
        Private slot to handle errors.

        @param method name of the method the error occured in
        @type str
        @param error error message
        @type str
        """
        EricMessageBox.warning(
            self,
            self.tr("Error handling device"),
            self.tr(
                "<p>There was an error communicating with the connected"
                " device.</p><p>Method: {0}</p><p>Message: {1}</p>"
            ).format(method, error),
        )

    @pyqtSlot(str)
    def __handleCurrentDir(self, dirname):
        """
        Private slot to handle a change of the current directory of the device.

        @param dirname name of the current directory
        @type str
        """
        self.deviceCwd.setText(dirname)
        self.__newDeviceList()

    @pyqtSlot(tuple)
    def __handleLongListFiles(self, filesList):
        """
        Private slot to receive a long directory listing.

        @param filesList tuple containing tuples with name, mode, size and time
            for each directory entry
        @type tuple of (str, str, str, str)
        """
        self.deviceFileTreeWidget.clear()
        for name, mode, size, dateTime in filesList:
            itm = QTreeWidgetItem(
                self.deviceFileTreeWidget, [name, mode, size, dateTime]
            )
            itm.setTextAlignment(1, Qt.AlignmentFlag.AlignHCenter)
            itm.setTextAlignment(2, Qt.AlignmentFlag.AlignRight)
        self.deviceFileTreeWidget.header().resizeSections(
            QHeaderView.ResizeMode.ResizeToContents
        )

    def __listLocalFiles(self, dirname="", localDevice=False):
        """
        Private method to populate the local files list.

        @param dirname name of the local directory to be listed
        @type str
        @param localDevice flag indicating device access via local file system
        @type bool
        """
        if not dirname:
            dirname = os.getcwd()
        if dirname != os.sep and dirname.endswith(os.sep):
            dirname = dirname[:-1]
        if localDevice:
            self.deviceCwd.setText(dirname)
            showHidden = Preferences.getMicroPython("ShowHiddenDevice")
        else:
            self.localCwd.setText(dirname)
            showHidden = Preferences.getMicroPython("ShowHiddenLocal")

        filesStatList = listdirStat(dirname, showHidden=showHidden)
        filesList = [
            (
                decoratedName(f, s[0], os.path.isdir(os.path.join(dirname, f))),
                mode2string(s[0]),
                str(s[6]),
                mtime2string(s[8]),
            )
            for f, s in filesStatList
        ]
        fileTreeWidget = (
            self.deviceFileTreeWidget if localDevice else self.localFileTreeWidget
        )
        fileTreeWidget.clear()
        for item in filesList:
            itm = QTreeWidgetItem(fileTreeWidget, item)
            itm.setTextAlignment(1, Qt.AlignmentFlag.AlignHCenter)
            itm.setTextAlignment(2, Qt.AlignmentFlag.AlignRight)
        fileTreeWidget.header().resizeSections(QHeaderView.ResizeMode.ResizeToContents)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_localFileTreeWidget_itemActivated(self, item, column):
        """
        Private slot to handle the activation of a local item.

        If the item is a directory, the list will be re-populated for this
        directory.

        @param item reference to the activated item
        @type QTreeWidgetItem
        @param column column of the activation
        @type int
        """
        name = os.path.join(self.localCwd.text(), item.text(0))
        if name.endswith("/"):
            # directory names end with a '/'
            self.__listLocalFiles(name[:-1])
        elif Utilities.MimeTypes.isTextFile(name):
            ericApp().getObject("ViewManager").getEditor(name)

    @pyqtSlot()
    def on_localFileTreeWidget_itemSelectionChanged(self):
        """
        Private slot handling a change of selection in the local pane.
        """
        enable = bool(len(self.localFileTreeWidget.selectedItems()))
        if enable:
            enable &= not (
                self.localFileTreeWidget.selectedItems()[0].text(0).endswith("/")
            )
        self.putButton.setEnabled(enable)
        self.putAsButton.setEnabled(enable)

    @pyqtSlot(str)
    def on_localCwd_textChanged(self, cwd):
        """
        Private slot handling a change of the current local working directory.

        @param cwd current local working directory
        @type str
        """
        self.localUpButton.setEnabled(cwd != os.sep)

    @pyqtSlot()
    def on_localUpButton_clicked(self):
        """
        Private slot to go up one directory level.
        """
        cwd = self.localCwd.text()
        dirname = os.path.dirname(cwd)
        self.__listLocalFiles(dirname)

    @pyqtSlot()
    def on_localHomeButton_clicked(self):
        """
        Private slot to change directory to the configured workspace.
        """
        dirname = (
            Preferences.getMicroPython("MpyWorkspace")
            or Preferences.getMultiProject("Workspace")
            or os.path.expanduser("~")
        )
        self.__listLocalFiles(dirname)

    @pyqtSlot()
    def on_localReloadButton_clicked(self):
        """
        Private slot to reload the local list.
        """
        dirname = self.localCwd.text()
        self.__listLocalFiles(dirname)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_deviceFileTreeWidget_itemActivated(self, item, column):
        """
        Private slot to handle the activation of a device item.

        If the item is a directory, the current working directory is changed
        and the list will be re-populated for this directory.

        @param item reference to the activated item
        @type QTreeWidgetItem
        @param column column of the activation
        @type int
        """
        if self.__repl.deviceSupportsLocalFileAccess():
            name = os.path.join(self.deviceCwd.text(), item.text(0))
            if name.endswith("/"):
                # directory names end with a '/'
                self.__listLocalFiles(name[:-1], True)
            else:
                if not os.path.exists(name):
                    EricMessageBox.warning(
                        self,
                        self.tr("Open Device File"),
                        self.tr(
                            """<p>The file <b>{0}</b> does not exist.</p>"""
                        ).format(name),
                    )
                    return
                if Utilities.MimeTypes.isTextFile(name):
                    ericApp().getObject("ViewManager").getEditor(name)
        else:
            cwd = self.deviceCwd.text()
            if cwd:
                name = (
                    cwd + item.text(0)
                    if cwd.endswith("/")
                    else "{0}/{1}".format(cwd, item.text(0))
                )
            else:
                name = item.text(0)
            if name.endswith("/"):
                # directory names end with a '/'
                self.__fileManager.cd(name[:-1])
            else:
                data = self.__fileManager.getData(name)
                try:
                    text = data.decode(encoding="utf-8")
                    ericApp().getObject("ViewManager").newEditorWithText(
                        text, fileName="device:{0}".format(name)
                    )
                except UnicodeDecodeError:
                    EricMessageBox.warning(
                        self,
                        self.tr("Open Device File"),
                        self.tr(
                            "<p>The file <b>{0}</b> does not contain Unicode text.</p>"
                        ).format(name),
                    )
                    return

    @pyqtSlot()
    def on_deviceFileTreeWidget_itemSelectionChanged(self):
        """
        Private slot handling a change of selection in the local pane.
        """
        enable = bool(len(self.deviceFileTreeWidget.selectedItems()))
        if enable:
            enable &= not (
                self.deviceFileTreeWidget.selectedItems()[0].text(0).endswith("/")
            )
        self.getButton.setEnabled(enable)
        self.getAsButton.setEnabled(enable)

        self.openButton.setEnabled(enable)
        self.saveButton.setEnabled(enable)

    @pyqtSlot(str)
    def on_deviceCwd_textChanged(self, cwd):
        """
        Private slot handling a change of the current device working directory.

        @param cwd current device working directory
        @type str
        """
        self.deviceUpButton.setEnabled(cwd != "/")

    @pyqtSlot()
    def on_deviceUpButton_clicked(self):
        """
        Private slot to go up one directory level on the device.
        """
        cwd = self.deviceCwd.text()
        dirname = os.path.dirname(cwd)
        if self.__repl.deviceSupportsLocalFileAccess():
            self.__listLocalFiles(dirname, True)
        else:
            self.__fileManager.cd(dirname)

    @pyqtSlot()
    def on_deviceHomeButton_clicked(self):
        """
        Private slot to move to the device home directory.
        """
        if self.__repl.deviceSupportsLocalFileAccess():
            dirname = self.__repl.getDeviceWorkspace()
            if dirname:
                self.__listLocalFiles(dirname, True)
                return

        # list files via device script
        self.__fileManager.cd("/")

    @pyqtSlot()
    def on_deviceReloadButton_clicked(self):
        """
        Private slot to reload the device list.
        """
        dirname = self.deviceCwd.text()
        if self.__repl.deviceSupportsLocalFileAccess():
            self.__listLocalFiles(dirname, True)
        else:
            if dirname:
                self.__newDeviceList()
            else:
                self.__fileManager.pwd()

    def __isFileInList(self, filename, treeWidget):
        """
        Private method to check, if a file name is contained in a tree widget.

        @param filename name of the file to check
        @type str
        @param treeWidget reference to the tree widget to be checked against
        @return flag indicating that the file name is present
        @rtype bool
        """
        itemCount = treeWidget.topLevelItemCount()
        return itemCount > 0 and any(
            treeWidget.topLevelItem(row).text(0) == filename for row in range(itemCount)
        )

    @pyqtSlot()
    def on_putButton_clicked(self, putAs=False):
        """
        Private slot to copy the selected file to the connected device.

        @param putAs flag indicating to give it a new name
        @type bool
        """
        selectedItems = self.localFileTreeWidget.selectedItems()
        if selectedItems:
            filename = selectedItems[0].text(0).strip()
            if not filename.endswith("/"):
                # it is really a file
                if putAs:
                    deviceFilename, ok = QInputDialog.getText(
                        self,
                        self.tr("Put File As"),
                        self.tr("Enter a new name for the file"),
                        QLineEdit.EchoMode.Normal,
                        filename,
                    )
                    if not ok or not filename:
                        return
                else:
                    deviceFilename = filename

                if self.__isFileInList(deviceFilename, self.deviceFileTreeWidget):
                    # ask for overwrite permission
                    action, resultFilename = confirmOverwrite(
                        deviceFilename,
                        self.tr("Copy File to Device"),
                        self.tr(
                            "The given file exists already (Enter file name only)."
                        ),
                        False,
                        self,
                    )
                    if action == "cancel":
                        return
                    elif action == "rename":
                        deviceFilename = os.path.basename(resultFilename)

                if self.__repl.deviceSupportsLocalFileAccess():
                    shutil.copy2(
                        os.path.join(self.localCwd.text(), filename),
                        os.path.join(self.deviceCwd.text(), deviceFilename),
                    )
                    self.__listLocalFiles(self.deviceCwd.text(), localDevice=True)
                else:
                    deviceCwd = self.deviceCwd.text()
                    if deviceCwd:
                        if deviceCwd != "/":
                            deviceFilename = deviceCwd + "/" + deviceFilename
                        else:
                            deviceFilename = "/" + deviceFilename
                    self.__fileManager.put(
                        os.path.join(self.localCwd.text(), filename), deviceFilename
                    )

    @pyqtSlot()
    def on_putAsButton_clicked(self):
        """
        Private slot to copy the selected file to the connected device
        with a different name.
        """
        self.on_putButton_clicked(putAs=True)

    @pyqtSlot()
    def on_getButton_clicked(self, getAs=False):
        """
        Private slot to copy the selected file from the connected device.

        @param getAs flag indicating to give it a new name
        @type bool
        """
        selectedItems = self.deviceFileTreeWidget.selectedItems()
        if selectedItems:
            filename = selectedItems[0].text(0).strip()
            if not filename.endswith("/"):
                # it is really a file
                if getAs:
                    localFilename, ok = QInputDialog.getText(
                        self,
                        self.tr("Get File As"),
                        self.tr("Enter a new name for the file"),
                        QLineEdit.EchoMode.Normal,
                        filename,
                    )
                    if not ok or not filename:
                        return
                else:
                    localFilename = filename

                if self.__isFileInList(localFilename, self.localFileTreeWidget):
                    # ask for overwrite permission
                    action, resultFilename = confirmOverwrite(
                        localFilename,
                        self.tr("Copy File from Device"),
                        self.tr("The given file exists already."),
                        True,
                        self,
                    )
                    if action == "cancel":
                        return
                    elif action == "rename":
                        localFilename = resultFilename

                if self.__repl.deviceSupportsLocalFileAccess():
                    shutil.copy2(
                        os.path.join(self.deviceCwd.text(), filename),
                        os.path.join(self.localCwd.text(), localFilename),
                    )
                    self.__listLocalFiles(self.localCwd.text())
                else:
                    deviceCwd = self.deviceCwd.text()
                    if deviceCwd:
                        filename = deviceCwd + "/" + filename
                    self.__fileManager.get(
                        filename, os.path.join(self.localCwd.text(), localFilename)
                    )

    @pyqtSlot()
    def on_getAsButton_clicked(self):
        """
        Private slot to copy the selected file from the connected device
        with a different name.
        """
        self.on_getButton_clicked(getAs=True)

    @pyqtSlot(str, str)
    def __handleGetDone(self, deviceFile, localFile):
        """
        Private slot handling a successful copy of a file from the device.

        @param deviceFile name of the file on the device
        @type str
        @param localFile name of the local file
        @type str
        """
        self.__listLocalFiles(self.localCwd.text())

    @pyqtSlot()
    def on_syncButton_clicked(self):
        """
        Private slot to synchronize the local directory to the device.
        """
        self.__fileManager.rsync(
            self.localCwd.text(),
            self.deviceCwd.text(),
            mirror=True,
            localDevice=self.__repl.deviceSupportsLocalFileAccess(),
        )

    @pyqtSlot(str, str)
    def __handleRsyncDone(self, localDir, deviceDir):
        """
        Private method to handle the completion of the rsync operation.

        @param localDir name of the local directory
        @type str
        @param deviceDir name of the device directory
        @type str
        """
        # simulate button presses to reload the two lists
        self.on_localReloadButton_clicked()
        self.on_deviceReloadButton_clicked()

    @pyqtSlot(str)
    def __handleRsyncProgressMessage(self, message):
        """
        Private slot handling progress messages sent by the file manager.

        @param message message to be shown
        @type str
        """
        from .MicroPythonProgressInfoDialog import MicroPythonProgressInfoDialog

        if self.__progressInfoDialog is None:
            self.__progressInfoDialog = MicroPythonProgressInfoDialog(self)
            self.__progressInfoDialog.finished.connect(
                self.__progressInfoDialogFinished
            )
        self.__progressInfoDialog.show()
        self.__progressInfoDialog.addMessage(message)

    @pyqtSlot()
    def __progressInfoDialogFinished(self):
        """
        Private slot handling the closing of the progress info dialog.
        """
        self.__progressInfoDialog.deleteLater()
        self.__progressInfoDialog = None

    @pyqtSlot()
    def __newDeviceList(self):
        """
        Private slot to initiate a new long list of the device directory.
        """
        self.__fileManager.lls(
            self.deviceCwd.text(),
            showHidden=Preferences.getMicroPython("ShowHiddenDevice"),
        )

    @pyqtSlot()
    def on_openButton_clicked(self):
        """
        Private slot to open the selected file in a new editor.
        """
        selectedItems = self.deviceFileTreeWidget.selectedItems()
        if selectedItems:
            filename = selectedItems[0].text(0).strip()
            if self.__repl.deviceSupportsLocalFileAccess():
                name = os.path.join(self.deviceCwd.text(), filename)
                if not name.endswith("/") and Utilities.MimeTypes.isTextFile(name):
                    ericApp().getObject("ViewManager").getEditor(name)
            else:
                cwd = self.deviceCwd.text()
                if cwd:
                    name = (
                        cwd + filename
                        if cwd.endswith("/")
                        else "{0}/{1}".format(cwd, filename)
                    )
                else:
                    name = filename
                if not name.endswith("/"):
                    data = self.__fileManager.getData(name)
                    text = data.decode(encoding="utf-8")
                    ericApp().getObject("ViewManager").newEditorWithText(
                        text, "Python3", "device:{0}".format(name)
                    )

    @pyqtSlot()
    def on_saveButton_clicked(self, saveAs=False):
        """
        Private slot to save the text of the current editor to a file on the device.

        @param saveAs flag indicating to save the file with a new name
        @type bool
        """
        aw = ericApp().getObject("ViewManager").activeWindow()
        if not aw:
            return

        selectedItems = self.deviceFileTreeWidget.selectedItems()
        if selectedItems:
            filename = selectedItems[0].text(0).strip()
            if filename.endswith("/"):
                saveAs = True
        else:
            saveAs = True
            filename = ""

        if saveAs:
            filename, ok = QInputDialog.getText(
                self,
                self.tr("Save File As"),
                self.tr("Enter a new name for the file:"),
                QLineEdit.EchoMode.Normal,
                filename,
            )
            if not ok or not filename:
                return

        if not saveAs:
            # check editor and selected file names for an implicit 'save as'
            editorFileName = os.path.basename(aw.getFileName().replace("device:", ""))
            if editorFileName != filename:
                saveAs = True

        if saveAs and self.__isFileInList(filename, self.deviceFileTreeWidget):
            # ask for overwrite permission
            action, resultFilename = confirmOverwrite(
                filename,
                self.tr("Save File As"),
                self.tr("The given file exists already (Enter file name only)."),
                False,
                self,
            )
            if action == "cancel":
                return
            elif action == "rename":
                filename = os.path.basename(resultFilename)

        text = aw.text()
        if self.__repl.deviceSupportsLocalFileAccess():
            filename = os.path.join(self.deviceCwd.text(), filename)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as f:
                f.write(text)
            self.__newDeviceList()
            aw.setFileName(filename)
        else:
            if not filename.startswith("/"):
                deviceCwd = self.deviceCwd.text()
                if deviceCwd:
                    filename = (
                        deviceCwd + "/" + filename
                        if deviceCwd != "/"
                        else "/" + filename
                    )
            dirname = filename.rsplit("/", 1)[0]
            self.__fileManager.makedirs(dirname)
            self.__fileManager.putData(filename, text.encode("utf-8"))
            aw.setFileName("device:" + filename)

        aw.setModified(False)
        aw.resetOnlineChangeTraceInfo()

    @pyqtSlot()
    def on_saveAsButton_clicked(self):
        """
        Private slot to save the current editor in a new file on the connected device.
        """
        self.on_saveButton_clicked(saveAs=True)

    ##################################################################
    ## Context menu methods for the local files below
    ##################################################################

    @pyqtSlot(QPoint)
    def __showLocalContextMenu(self, pos):
        """
        Private slot to show the REPL context menu.

        @param pos position to show the menu at
        @type QPoint
        """
        hasSelection = bool(len(self.localFileTreeWidget.selectedItems()))
        if hasSelection:
            name = self.localFileTreeWidget.selectedItems()[0].text(0)
            isDir = name.endswith("/")
            isFile = not isDir
        else:
            isDir = False
            isFile = False
        self.__localDelDirTreeAct.setEnabled(isDir)
        self.__localDelFileAct.setEnabled(isFile)

        self.__localMenu.exec(self.localFileTreeWidget.mapToGlobal(pos))

    @pyqtSlot()
    def __changeLocalDirectory(self, localDevice=False):
        """
        Private slot to change the local directory.

        @param localDevice flag indicating device access via local file system
        @type bool
        """
        cwdWidget = self.deviceCwd if localDevice else self.localCwd

        dirPath, ok = EricPathPickerDialog.getStrPath(
            self,
            self.tr("Change Directory"),
            self.tr("Select Directory"),
            EricPathPickerModes.DIRECTORY_SHOW_FILES_MODE,
            strPath=cwdWidget.text(),
            defaultDirectory=cwdWidget.text(),
        )
        if ok and dirPath:
            if not os.path.isabs(dirPath):
                dirPath = os.path.join(cwdWidget.text(), dirPath)
            cwdWidget.setText(dirPath)
            self.__listLocalFiles(dirPath, localDevice=localDevice)

    @pyqtSlot()
    def __createLocalDirectory(self, localDevice=False):
        """
        Private slot to create a local directory.

        @param localDevice flag indicating device access via local file system
        @type bool
        """
        cwdWidget = self.deviceCwd if localDevice else self.localCwd

        dirPath, ok = QInputDialog.getText(
            self,
            self.tr("Create Directory"),
            self.tr("Enter directory name:"),
            QLineEdit.EchoMode.Normal,
        )
        if ok and dirPath:
            dirPath = os.path.join(cwdWidget.text(), dirPath)
            try:
                os.mkdir(dirPath)
                self.__listLocalFiles(cwdWidget.text(), localDevice=localDevice)
            except OSError as exc:
                EricMessageBox.critical(
                    self,
                    self.tr("Create Directory"),
                    self.tr(
                        """<p>The directory <b>{0}</b> could not be"""
                        """ created.</p><p>Reason: {1}</p>"""
                    ).format(dirPath, str(exc)),
                )

    @pyqtSlot()
    def __deleteLocalDirectoryTree(self, localDevice=False):
        """
        Private slot to delete a local directory tree.

        @param localDevice flag indicating device access via local file system
        @type bool
        """
        if localDevice:
            cwdWidget = self.deviceCwd
            fileTreeWidget = self.deviceFileTreeWidget
        else:
            cwdWidget = self.localCwd
            fileTreeWidget = self.localFileTreeWidget

        if bool(len(fileTreeWidget.selectedItems())):
            name = fileTreeWidget.selectedItems()[0].text(0)
            dirname = os.path.join(cwdWidget.text(), name[:-1])
            dlg = DeleteFilesConfirmationDialog(
                self,
                self.tr("Delete Directory Tree"),
                self.tr("Do you really want to delete this directory tree?"),
                [dirname],
            )
            if dlg.exec() == QDialog.DialogCode.Accepted:
                try:
                    shutil.rmtree(dirname)
                    self.__listLocalFiles(cwdWidget.text(), localDevice=localDevice)
                except Exception as exc:
                    EricMessageBox.critical(
                        self,
                        self.tr("Delete Directory Tree"),
                        self.tr(
                            """<p>The directory <b>{0}</b> could not be"""
                            """ deleted.</p><p>Reason: {1}</p>"""
                        ).format(dirname, str(exc)),
                    )

    @pyqtSlot()
    def __deleteLocalFile(self, localDevice=False):
        """
        Private slot to delete a local file.

        @param localDevice flag indicating device access via local file system
        @type bool
        """
        if localDevice:
            cwdWidget = self.deviceCwd
            fileTreeWidget = self.deviceFileTreeWidget
        else:
            cwdWidget = self.localCwd
            fileTreeWidget = self.localFileTreeWidget

        if bool(len(fileTreeWidget.selectedItems())):
            name = fileTreeWidget.selectedItems()[0].text(0)
            filename = os.path.join(cwdWidget.text(), name)
            dlg = DeleteFilesConfirmationDialog(
                self,
                self.tr("Delete File"),
                self.tr("Do you really want to delete this file?"),
                [filename],
            )
            if dlg.exec() == QDialog.DialogCode.Accepted:
                try:
                    os.remove(filename)
                    self.__listLocalFiles(cwdWidget.text(), localDevice=localDevice)
                except OSError as exc:
                    EricMessageBox.critical(
                        self,
                        self.tr("Delete File"),
                        self.tr(
                            """<p>The file <b>{0}</b> could not be"""
                            """ deleted.</p><p>Reason: {1}</p>"""
                        ).format(filename, str(exc)),
                    )

    @pyqtSlot(bool)
    def __localHiddenChanged(self, checked):
        """
        Private slot handling a change of the local show hidden menu entry.

        @param checked new check state of the action
        @type bool
        """
        Preferences.setMicroPython("ShowHiddenLocal", checked)
        self.on_localReloadButton_clicked()

    ##################################################################
    ## Context menu methods for the device files below
    ##################################################################

    @pyqtSlot(QPoint)
    def __showDeviceContextMenu(self, pos):
        """
        Private slot to show the REPL context menu.

        @param pos position to show the menu at
        @type QPoint
        """
        hasSelection = bool(len(self.deviceFileTreeWidget.selectedItems()))
        if hasSelection:
            name = self.deviceFileTreeWidget.selectedItems()[0].text(0)
            isDir = name.endswith("/")
            isFile = not isDir
        else:
            isDir = False
            isFile = False
        if not self.__repl.isMicrobit():
            self.__devDelDirAct.setEnabled(isDir)
            self.__devDelDirTreeAct.setEnabled(isDir)
        self.__devDelFileAct.setEnabled(isFile)

        self.__deviceMenu.exec(self.deviceFileTreeWidget.mapToGlobal(pos))

    @pyqtSlot()
    def __changeDeviceDirectory(self):
        """
        Private slot to change the current directory of the device.

        Note: This triggers a re-population of the device list for the new
        current directory.
        """
        if self.__repl.deviceSupportsLocalFileAccess():
            self.__changeLocalDirectory(True)
        else:
            dirPath, ok = QInputDialog.getText(
                self,
                self.tr("Change Directory"),
                self.tr("Enter the directory path on the device:"),
                QLineEdit.EchoMode.Normal,
                self.deviceCwd.text(),
            )
            if ok and dirPath:
                if not dirPath.startswith("/"):
                    dirPath = self.deviceCwd.text() + "/" + dirPath
                self.__fileManager.cd(dirPath)

    @pyqtSlot()
    def __createDeviceDirectory(self):
        """
        Private slot to create a directory on the device.
        """
        if self.__repl.deviceSupportsLocalFileAccess():
            self.__createLocalDirectory(True)
        else:
            dirPath, ok = QInputDialog.getText(
                self,
                self.tr("Create Directory"),
                self.tr("Enter directory name:"),
                QLineEdit.EchoMode.Normal,
            )
            if ok and dirPath:
                self.__fileManager.mkdir(dirPath)

    @pyqtSlot()
    def __deleteDeviceDirectory(self):
        """
        Private slot to delete an empty directory on the device.
        """
        if self.__repl.deviceSupportsLocalFileAccess():
            self.__deleteLocalDirectoryTree(True)
        else:
            if bool(len(self.deviceFileTreeWidget.selectedItems())):
                name = self.deviceFileTreeWidget.selectedItems()[0].text(0)
                cwd = self.deviceCwd.text()
                if cwd:
                    if cwd != "/":
                        dirname = cwd + "/" + name[:-1]
                    else:
                        dirname = "/" + name[:-1]
                else:
                    dirname = name[:-1]
                dlg = DeleteFilesConfirmationDialog(
                    self,
                    self.tr("Delete Directory"),
                    self.tr("Do you really want to delete this directory?"),
                    [dirname],
                )
                if dlg.exec() == QDialog.DialogCode.Accepted:
                    self.__fileManager.rmdir(dirname)

    @pyqtSlot()
    def __deleteDeviceDirectoryTree(self):
        """
        Private slot to delete a directory and all its subdirectories
        recursively.
        """
        if self.__repl.deviceSupportsLocalFileAccess():
            self.__deleteLocalDirectoryTree(True)
        else:
            if bool(len(self.deviceFileTreeWidget.selectedItems())):
                name = self.deviceFileTreeWidget.selectedItems()[0].text(0)
                cwd = self.deviceCwd.text()
                if cwd:
                    if cwd != "/":
                        dirname = cwd + "/" + name[:-1]
                    else:
                        dirname = "/" + name[:-1]
                else:
                    dirname = name[:-1]
                dlg = DeleteFilesConfirmationDialog(
                    self,
                    self.tr("Delete Directory Tree"),
                    self.tr("Do you really want to delete this directory tree?"),
                    [dirname],
                )
                if dlg.exec() == QDialog.DialogCode.Accepted:
                    self.__fileManager.rmdir(dirname, recursive=True)

    @pyqtSlot()
    def __deleteDeviceFile(self):
        """
        Private slot to delete a file.
        """
        if self.__repl.deviceSupportsLocalFileAccess():
            self.__deleteLocalFile(True)
        else:
            if bool(len(self.deviceFileTreeWidget.selectedItems())):
                name = self.deviceFileTreeWidget.selectedItems()[0].text(0)
                dirname = self.deviceCwd.text()
                if dirname:
                    if dirname != "/":
                        filename = dirname + "/" + name
                    else:
                        filename = "/" + name
                else:
                    filename = name
                dlg = DeleteFilesConfirmationDialog(
                    self,
                    self.tr("Delete File"),
                    self.tr("Do you really want to delete this file?"),
                    [filename],
                )
                if dlg.exec() == QDialog.DialogCode.Accepted:
                    self.__fileManager.delete(filename)

    @pyqtSlot(bool)
    def __deviceHiddenChanged(self, checked):
        """
        Private slot handling a change of the device show hidden menu entry.

        @param checked new check state of the action
        @type bool
        """
        Preferences.setMicroPython("ShowHiddenDevice", checked)
        self.on_deviceReloadButton_clicked()

    @pyqtSlot()
    def __showFileSystemInfo(self):
        """
        Private slot to show some file system information.
        """
        self.__fileManager.fileSystemInfo()

    @pyqtSlot(tuple)
    def __fsInfoResultReceived(self, fsinfo):
        """
        Private slot to show the file system information of the device.

        @param fsinfo tuple of tuples containing the file system name, the
            total size, the used size and the free size
        @type tuple of tuples of (str, int, int, int)
        """
        msg = self.tr("<h3>Filesystem Information</h3>")
        if fsinfo:
            for name, totalSize, usedSize, freeSize in fsinfo:
                msg += self.tr(
                    "<h4>{0}</h4"
                    "<table>"
                    "<tr><td>Total Size: </td><td align='right'>{1}</td></tr>"
                    "<tr><td>Used Size: </td><td align='right'>{2}</td></tr>"
                    "<tr><td>Free Size: </td><td align='right'>{3}</td></tr>"
                    "</table>"
                ).format(
                    name,
                    Globals.dataString(totalSize),
                    Globals.dataString(usedSize),
                    Globals.dataString(freeSize),
                )
        else:
            msg += self.tr(
                "<p>No file systems or file system information available.</p>"
            )
        EricMessageBox.information(self, self.tr("Filesystem Information"), msg)
