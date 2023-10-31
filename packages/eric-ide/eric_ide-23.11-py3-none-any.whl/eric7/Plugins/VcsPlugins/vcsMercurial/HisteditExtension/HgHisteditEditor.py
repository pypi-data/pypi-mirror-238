#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 - 2023 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the main script for histedit.

Depending on the file name given by the Mercurial histedit command one
of two possible dialogs will be shown.
"""

import os
import sys

sys.path.insert(
    1,
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."),
)
# five times up is our installation directory

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

    @param argv list of commandline parameters
    @type list of str
    @return reference to the main widget or None in case of an error
    @rtype QWidget or None
    """
    if len(argv) > 1:
        fileName = os.path.basename(argv[1])
        if fileName.startswith("hg-histedit-"):
            from HgHisteditPlanEditor import (  # __IGNORE_WARNING_I10__
                HgHisteditPlanEditor,
            )

            return HgHisteditPlanEditor(argv[1])
        elif fileName.startswith("hg-editor-"):
            from HgHisteditCommitEditor import (  # __IGNORE_WARNING_I10__
                HgHisteditCommitEditor,
            )

            return HgHisteditCommitEditor(argv[1])

    return None


def main():
    """
    Main entry point into the application.
    """
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
        sys.argv,
        "Mercurial Histedit Editor",
        "",
        "Editor for the Mercurial histedit command",
        options,
    )
    res = Startup.simpleAppStartup(sys.argv, appinfo, createMainWidget)
    sys.exit(res)


if __name__ == "__main__":
    main()
