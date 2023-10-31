#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2023 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
eric testing.

This is the main Python script that performs the necessary initialization
of the testing module and starts the Qt event loop. This is a standalone
version of the integrated testing module.
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

# make Python debug client available as a package repository (needed for 'coverage')
sys.path.insert(2, os.path.join(os.path.dirname(__file__), "DebugClients", "Python"))


def createMainWidget(argv):
    """
    Function to create the main widget.

    @param argv list of commandline parameters
    @type list of str
    @return reference to the main widget
    @rtype QWidget
    """
    from eric7.Testing.TestingWidget import TestingWindow

    try:
        fn = argv[1]
    except IndexError:
        fn = None
    return TestingWindow(fn)


def main():
    """
    Main entry point into the application.
    """
    QGuiApplication.setDesktopFileName("eric7_testing")

    options = [
        (
            "--config=configDir",
            "use the given directory as the one containing the config files",
        ),
        (
            "--settings=settingsDir",
            "use the given directory to store the settings files",
        ),
    ]
    appinfo = AppInfo.makeAppInfo(
        sys.argv, "eric Testing", "file", "Graphical test application", options
    )
    res = Startup.simpleAppStartup(sys.argv, appinfo, createMainWidget)
    sys.exit(res)


if __name__ == "__main__":
    main()
