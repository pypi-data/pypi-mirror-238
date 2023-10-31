# -*- coding: utf-8 -*-

# Copyright (c) 2008 - 2023 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Editor Search configuration page.
"""

from eric7 import Preferences

from .ConfigurationPageBase import ConfigurationPageBase
from .Ui_EditorSearchPage import Ui_EditorSearchPage


class EditorSearchPage(ConfigurationPageBase, Ui_EditorSearchPage):
    """
    Class implementing the Editor Search configuration page.
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.setupUi(self)
        self.setObjectName("EditorSearchPage")

        self.editorColours = {}

        # set initial values
        self.quicksearchCheckBox.setChecked(Preferences.getEditor("QuickSearchEnabled"))
        self.searchMarkersEnabledCheckBox.setChecked(
            Preferences.getEditor("SearchMarkersEnabled")
        )
        self.quicksearchMarkersEnabledCheckBox.setChecked(
            Preferences.getEditor("QuickSearchMarkersEnabled")
        )
        self.occurrencesMarkersEnabledCheckBox.setChecked(
            Preferences.getEditor("MarkOccurrencesEnabled")
        )

        self.markOccurrencesTimeoutSpinBox.setValue(
            Preferences.getEditor("MarkOccurrencesTimeout")
        )

        if Preferences.getEditor("SearchRegexpMode") == 0:
            self.regexpPosixButton.setChecked(True)
        else:
            self.regexpCxx11Button.setChecked(True)

        self.initColour(
            "SearchMarkers",
            self.searchMarkerButton,
            Preferences.getEditorColour,
            hasAlpha=True,
        )
        self.initColour(
            "SearchSelectionMarker",
            self.highlightingBackgroundButton,
            Preferences.getEditorColour,
            hasAlpha=True,
        )

    def setMode(self, displayMode):
        """
        Public method to perform mode dependent setups.

        @param displayMode mode of the configuration dialog
        @type ConfigurationMode
        """
        from ..ConfigurationDialog import ConfigurationMode

        if displayMode in (ConfigurationMode.SHELLMODE,):
            self.quicksearchCheckBox.hide()
            self.searckMarkersBox.hide()
            self.highlightingBackgroundLabel.hide()
            self.highlightingBackgroundButton.hide()

    def save(self):
        """
        Public slot to save the Editor Search configuration.
        """
        Preferences.setEditor(
            "QuickSearchEnabled", self.quicksearchCheckBox.isChecked()
        )
        Preferences.setEditor(
            "SearchMarkersEnabled", self.searchMarkersEnabledCheckBox.isChecked()
        )
        Preferences.setEditor(
            "QuickSearchMarkersEnabled",
            self.quicksearchMarkersEnabledCheckBox.isChecked(),
        )
        Preferences.setEditor(
            "MarkOccurrencesEnabled", self.occurrencesMarkersEnabledCheckBox.isChecked()
        )

        Preferences.setEditor(
            "MarkOccurrencesTimeout", self.markOccurrencesTimeoutSpinBox.value()
        )

        mode = 0 if self.regexpPosixButton.isChecked() else 1
        Preferences.setEditor("SearchRegexpMode", mode)

        self.saveColours(Preferences.setEditorColour)


def create(dlg):  # noqa: U100
    """
    Module function to create the configuration page.

    @param dlg reference to the configuration dialog
    @return reference to the instantiated page (ConfigurationPageBase)
    """
    page = EditorSearchPage()
    return page
