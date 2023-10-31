#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
eric PDF Viewer.

This is the main Python script that performs the necessary initialization
of the PDF viewer and starts the Qt event loop. This is a standalone version
of the integrated PDF viewer.
"""

import os
import sys

from PyQt6.QtGui import QGuiApplication

for arg in sys.argv[:]:
    if arg.startswith("--config="):
        from eric7 import Globals

        configDir = arg.replace("--config=", "")
        Globals.setConfigDir(configDir)
        sys.argv.remove(arg)
    elif arg.startswith("--settings="):
        from PyQt6.QtCore import QSettings

        settingsDir = os.path.expanduser(arg.replace("--settings=", ""))
        if not os.path.isdir(settingsDir):
            os.makedirs(settingsDir)
        QSettings.setPath(
            QSettings.Format.IniFormat, QSettings.Scope.UserScope, settingsDir
        )
        sys.argv.remove(arg)

from eric7.Globals import AppInfo
from eric7.Toolbox import Startup


def createMainWidget(argv):
    """
    Function to create the main widget.

    @param argv list of commandline parameters (list of strings)
    @return reference to the main widget (QWidget)
    """
    from eric7.PdfViewer.PdfViewerWindow import PdfViewerWindow

    try:
        fileName = argv[1]
    except IndexError:
        fileName = ""

    editor = PdfViewerWindow(fileName, None)
    return editor


def main():
    """
    Main entry point into the application.
    """
    QGuiApplication.setDesktopFileName("eric7_pdf")

    options = [
        (
            "--config=configDir",
            "use the given directory as the one containing the config files",
        ),
        (
            "--settings=settingsDir",
            "use the given directory to store the settings files",
        ),
        ("", "name of file to edit"),
    ]
    appinfo = AppInfo.makeAppInfo(
        sys.argv, "eric PDF Viewer", "", "Little tool to view PDF files.", options
    )
    res = Startup.simpleAppStartup(sys.argv, appinfo, createMainWidget)
    sys.exit(res)


if __name__ == "__main__":
    main()
