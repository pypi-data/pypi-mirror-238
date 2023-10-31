# -*- coding: utf-8 -*-

# Copyright (c) 2008 - 2023 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the add project dialog.
"""

import os

from PyQt6.QtCore import QUuid, pyqtSlot
from PyQt6.QtWidgets import QDialog, QDialogButtonBox

from eric7 import Preferences
from eric7.EricWidgets.EricPathPicker import EricPathPickerModes
from eric7.SystemUtilities import FileSystemUtilities

from .Ui_AddProjectDialog import Ui_AddProjectDialog


class AddProjectDialog(QDialog, Ui_AddProjectDialog):
    """
    Class implementing the add project dialog.
    """

    def __init__(
        self, parent=None, startdir="", project=None, categories=None, category=""
    ):
        """
        Constructor

        @param parent parent widget of this dialog
        @type QWidget
        @param startdir start directory for the selection dialog
        @type str
        @param project dictionary containing project data
        @type dict
        @param categories list of already used categories
        @type list of str
        @param category category to be preset
        @type str
        """
        super().__init__(parent)
        self.setupUi(self)

        self.filenamePicker.setMode(EricPathPickerModes.OPEN_FILE_MODE)
        self.filenamePicker.setFilters(
            self.tr("Project Files (*.epj);;XML Project Files (*.e4p)")
        )
        self.filenamePicker.setDefaultDirectory(
            Preferences.getMultiProject("Workspace")
        )

        if categories:
            self.categoryComboBox.addItem("")
            self.categoryComboBox.addItems(sorted(categories))
        self.categoryComboBox.setEditText(category)

        self.startdir = startdir
        self.uid = ""

        self.__okButton = self.buttonBox.button(QDialogButtonBox.StandardButton.Ok)
        self.__okButton.setEnabled(False)

        if project is not None:
            self.setWindowTitle(self.tr("Project Properties"))

            self.nameEdit.setText(project["name"])
            self.filenamePicker.setText(project["file"])
            self.descriptionEdit.setPlainText(project["description"])
            self.mainCheckBox.setChecked(project["master"])
            index = self.categoryComboBox.findText(project["category"])
            if index == -1:
                index = 0
            self.categoryComboBox.setCurrentIndex(index)
            self.uid = project["uid"]

    def getData(self):
        """
        Public slot to retrieve the dialogs data.

        @return tuple of five values giving the project name, the name of the project
            file, a flag telling whether the project shall be the main project, a short
            description for the project and the project category
        @rtype tuple of (str, str, bool, str, str)
        """
        if not self.uid:
            # new project entry
            self.uid = QUuid.createUuid().toString()

        filename = self.filenamePicker.text()
        if not os.path.isabs(filename):
            filename = FileSystemUtilities.toNativeSeparators(
                os.path.join(self.startdir, filename)
            )
        return (
            self.nameEdit.text(),
            filename,
            self.mainCheckBox.isChecked(),
            self.descriptionEdit.toPlainText(),
            self.categoryComboBox.currentText(),
            self.uid,
        )

    @pyqtSlot(str)
    def on_nameEdit_textChanged(self, txt):
        """
        Private slot called when the project name has changed.

        @param txt text of the edit
        @type str
        """
        self.__updateUi()

    @pyqtSlot(str)
    def on_filenamePicker_textChanged(self, txt):
        """
        Private slot called when the project filename has changed.

        @param txt text of the edit
        @type str
        """
        self.__updateUi()

    def __updateUi(self):
        """
        Private method to update the dialog.
        """
        self.__okButton.setEnabled(
            self.nameEdit.text() != "" and self.filenamePicker.text() != ""
        )
