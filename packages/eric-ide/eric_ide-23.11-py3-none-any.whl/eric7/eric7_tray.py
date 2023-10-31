#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2006 - 2023 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
eric Tray.

This is the main Python script that performs the necessary initialization
of the system-tray application. This acts as a quickstarter by providing a
context menu to start the eric IDE and the eric tools.
"""

import os
import sys

from PyQt6.QtGui import QGuiApplication

SettingsDir = None

for arg in sys.argv[:]:
    if arg.startswith("--config="):
        from eric7 import Globals

        configDir = arg.replace("--config=", "")
        Globals.setConfigDir(configDir)
        sys.argv.remove(arg)
    elif arg.startswith("--settings="):
        from PyQt6.QtCore import QSettings

        SettingsDir = os.path.expanduser(arg.replace("--settings=", ""))
        if not os.path.isdir(SettingsDir):
            os.makedirs(SettingsDir)
        QSettings.setPath(
            QSettings.Format.IniFormat, QSettings.Scope.UserScope, SettingsDir
        )
        sys.argv.remove(arg)

from eric7.Globals import AppInfo
from eric7.Toolbox import Startup


def createMainWidget(argv):  # noqa: U100
    """
    Function to create the main widget.

    @param argv list of commandline parameters (list of strings)
    @return reference to the main widget (QWidget)
    """
    from eric7.Tools.TrayStarter import TrayStarter

    return TrayStarter(SettingsDir)


def main():
    """
    Main entry point into the application.
    """
    QGuiApplication.setDesktopFileName("eric7_tray")

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
        sys.argv, "eric Tray", "", "Traystarter for eric", options
    )
    res = Startup.simpleAppStartup(
        sys.argv, appinfo, createMainWidget, quitOnLastWindowClosed=False, raiseIt=False
    )
    sys.exit(res)


if __name__ == "__main__":
    main()
