#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2006 - 2023 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
eric Configure.

This is the main Python script to configure the eric IDE from the outside.
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


def createMainWidget(argv):  # noqa: U100
    """
    Function to create the main widget.

    @param argv list of commandline parameters (list of strings)
    @return reference to the main widget (QWidget)
    """
    from eric7.Preferences.ConfigurationDialog import ConfigurationWindow

    w = ConfigurationWindow()
    w.show()
    w.showConfigurationPageByName("empty")
    return w


def main():
    """
    Main entry point into the application.
    """
    QGuiApplication.setDesktopFileName("eric7_configure")

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
        sys.argv, "eric Configure", "", "Configuration editor for eric", options
    )
    res = Startup.simpleAppStartup(sys.argv, appinfo, createMainWidget)
    sys.exit(res)


if __name__ == "__main__":
    main()
