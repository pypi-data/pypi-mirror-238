# -*- coding: utf-8 -*-

# Copyright (c) 2011 - 2023 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Security configuration page.
"""

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QDialog

from eric7 import Preferences

from .ConfigurationPageBase import ConfigurationPageBase
from .Ui_SecurityPage import Ui_SecurityPage


class SecurityPage(ConfigurationPageBase, Ui_SecurityPage):
    """
    Class implementing the Security configuration page.
    """

    def __init__(self, configDialog):
        """
        Constructor

        @param configDialog reference to the configuration dialog
            (ConfigurationDialog)
        """
        super().__init__()
        self.setupUi(self)
        self.setObjectName("SecurityPage")

        self.__configDlg = configDialog
        self.__displayMode = None

        # set initial values
        self.savePasswordsCheckBox.setChecked(Preferences.getUser("SavePasswords"))
        self.mainPasswordCheckBox.setChecked(Preferences.getUser("UseMasterPassword"))
        self.mainPasswordButton.setEnabled(Preferences.getUser("UseMasterPassword"))

        self.__newPassword = ""
        self.__oldUseMainPassword = Preferences.getUser("UseMasterPassword")

        self.alwaysRejectCheckBox.setChecked(
            Preferences.getWebBrowser("AlwaysRejectFaultyCertificates")
        )

    def setMode(self, displayMode):
        """
        Public method to perform mode dependent setups.

        @param displayMode mode of the configuration dialog
        @type ConfigurationMode
        """
        from ..ConfigurationDialog import ConfigurationMode

        if displayMode in (
            ConfigurationMode.DEFAULTMODE,
            ConfigurationMode.WEBBROWSERMODE,
        ):
            self.__displayMode = displayMode

            self.certificateErrorsGroup.setVisible(
                displayMode == ConfigurationMode.WEBBROWSERMODE
            )

    def save(self):
        """
        Public slot to save the Help Viewers configuration.
        """
        Preferences.setUser("SavePasswords", self.savePasswordsCheckBox.isChecked())
        Preferences.setUser("UseMasterPassword", self.mainPasswordCheckBox.isChecked())

        if self.__oldUseMainPassword != self.mainPasswordCheckBox.isChecked():
            self.__configDlg.mainPasswordChanged.emit("", self.__newPassword)

        Preferences.setWebBrowser(
            "AlwaysRejectFaultyCertificates", self.alwaysRejectCheckBox.isChecked()
        )

    @pyqtSlot(bool)
    def on_mainPasswordCheckBox_clicked(self, checked):
        """
        Private slot to handle the use of a main password.

        @param checked flag indicating the state of the check box (boolean)
        """
        from .MainPasswordEntryDialog import MainPasswordEntryDialog

        if checked:
            dlg = MainPasswordEntryDialog("", self)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                Preferences.setUser("MasterPassword", dlg.getMainPassword())
                self.mainPasswordButton.setEnabled(True)
                self.__newPassword = dlg.getMainPassword()
            else:
                self.mainPasswordCheckBox.setChecked(False)
        else:
            self.mainPasswordButton.setEnabled(False)
            self.__newPassword = ""

    @pyqtSlot()
    def on_mainPasswordButton_clicked(self):
        """
        Private slot to change the main password.
        """
        from .MainPasswordEntryDialog import MainPasswordEntryDialog

        dlg = MainPasswordEntryDialog(Preferences.getUser("MasterPassword"), self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            Preferences.setUser("MasterPassword", dlg.getMainPassword())

            if self.__oldUseMainPassword != self.mainPasswordCheckBox.isChecked():
                # the user is about to change the use of a main password
                # just save the changed password
                self.__newPassword = dlg.getMainPassword()
            else:
                self.__configDlg.mainPasswordChanged.emit(
                    dlg.getCurrentPassword(), dlg.getMainPassword()
                )


def create(dlg):
    """
    Module function to create the configuration page.

    @param dlg reference to the configuration dialog
    @return reference to the instantiated page (ConfigurationPageBase)
    """
    page = SecurityPage(dlg)
    return page
