#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2023 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
eric Python IDE.

This is the main Python script that performs the necessary initialization
of the IDE and starts the Qt event loop.
"""

import contextlib
import io
import logging
import multiprocessing
import os
import sys
import time
import traceback

originalPathString = os.getenv("PATH")

# generate list of arguments to be remembered for a restart
restartArgsList = [
    "--config",
    "--debug",
    "--disable-crash",
    "--disable-plugin",
    "--no-multimedia",
    "--no-splash",
    "--plugin",
    "--settings",
]
restartArgs = [arg for arg in sys.argv[1:] if arg.split("=", 1)[0] in restartArgsList]

try:
    from PyQt6.QtCore import QCoreApplication, QLibraryInfo, QTimer, qWarning
    from PyQt6.QtGui import QGuiApplication
except ImportError:
    try:
        from tkinter import messagebox
    except ImportError:
        sys.exit(100)
    messagebox.showerror(
        "eric7 Error",
        "PyQt could not be imported. Please make sure"
        " it is installed and accessible.",
    )
    sys.exit(100)

try:
    from PyQt6 import QtWebEngineWidgets  # __IGNORE_WARNING__ __IGNORE_EXCEPTION__
    from PyQt6.QtWebEngineCore import QWebEngineUrlScheme

    WEBENGINE_AVAILABLE = True
except ImportError:
    WEBENGINE_AVAILABLE = False

# some global variables needed to start the application
args = None
mainWindow = None
splash = None
inMainLoop = False
app = None

if "--debug" in sys.argv:
    del sys.argv[sys.argv.index("--debug")]
    logging.basicConfig(level=logging.DEBUG)

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

from eric7.EricWidgets.EricApplication import EricApplication


def handleSingleApplication(ddindex):
    """
    Global function to handle the single application mode.

    @param ddindex index of a '--' option in the options list
    """
    from eric7.EricWidgets.EricSingleApplication import EricSingleApplicationClient

    client = EricSingleApplicationClient()
    res = client.connect()
    if res > 0:
        for switch in (
            "--debug",
            "--disable-crash",
            "--no-crash",
            "--no-multimedia",
            "--no-open",
            "--no-splash",
            "--small-screen",
        ):
            if switch in sys.argv and sys.argv.index(switch) < ddindex:
                sys.argv.remove(switch)
                ddindex -= 1
        for arg in sys.argv[:]:
            for switch in (
                "--config=",
                "--plugin=",
                "--disable-plugin=",
                "--settings=",
            ):
                if arg.startswith(switch) and sys.argv.index(arg) < ddindex:
                    sys.argv.remove(arg)
                    ddindex -= 1
                    break

        if len(sys.argv) > 1:
            client.processArgs(sys.argv[1:])
        sys.exit(0)

    elif res < 0:
        print("eric7: {0}".format(client.errstr()))
        # __IGNORE_WARNING_M801__
        sys.exit(res)


def excepthook(excType, excValue, tracebackobj):
    """
    Global function to catch unhandled exceptions.

    @param excType exception type
    @param excValue exception value
    @param tracebackobj traceback object
    """
    from eric7 import Globals, Utilities
    from eric7.UI.Info import BugAddress

    # Workaround for a strange issue with QScintilla
    if str(excValue) == "unable to convert a QVariant back to a Python object":
        return

    separator = "-" * 80
    logFile = os.path.join(Globals.getConfigDir(), "eric7_error.log")
    notice = (
        """An unhandled exception occurred. Please report the problem\n"""
        """using the error reporting dialog or via email to <{0}>.\n"""
        """A log has been written to "{1}".\n\nError information:\n""".format(
            BugAddress, logFile
        )
    )
    timeString = time.strftime("%Y-%m-%d, %H:%M:%S")

    versionInfo = "\n{0}\n{1}".format(separator, Utilities.generateVersionInfo())
    pluginVersionInfo = Utilities.generatePluginsVersionInfo()
    if pluginVersionInfo:
        versionInfo += "\n{0}\n{1}".format(separator, pluginVersionInfo)
    distroInfo = Utilities.generateDistroInfo()
    if distroInfo:
        versionInfo += "\n{0}\n{1}".format(separator, distroInfo)

    if isinstance(excType, str):
        tbinfo = tracebackobj
    else:
        tbinfofile = io.StringIO()
        traceback.print_tb(tracebackobj, None, tbinfofile)
        tbinfofile.seek(0)
        tbinfo = tbinfofile.read()
    errmsg = "{0}: \n{1}".format(str(excType), str(excValue))
    sections = ["", separator, timeString, separator, errmsg, separator, tbinfo]
    msg = "\n".join(sections)
    with contextlib.suppress(OSError), open(logFile, "w", encoding="utf-8") as f:
        f.write(msg)
        f.write(versionInfo)

    if inMainLoop:
        warning = notice + msg + versionInfo
        # Escape &<> otherwise it's not visible in the error dialog
        warning = (
            warning.replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;")
        )
        qWarning(warning)
    else:
        warning = notice + msg + versionInfo
        print(warning)  # __IGNORE_WARNING_M801__


def uiStartUp():
    """
    Global function to finalize the start up of the main UI.

    Note: It is activated by a zero timeout single-shot timer.
    """
    global args, mainWindow, splash

    if splash:
        splash.finish(mainWindow)
        del splash

    mainWindow.checkForErrorLog()
    mainWindow.processArgs(args)
    mainWindow.processInstallInfoFile()
    mainWindow.checkProjectsWorkspace()
    mainWindow.checkConfigurationStatus()
    mainWindow.performVersionCheck()
    mainWindow.checkPluginUpdatesAvailable()
    mainWindow.autoConnectIrc()


def main():
    """
    Main entry point into the application.
    """
    from eric7.Globals import AppInfo
    from eric7.SystemUtilities import OSUtilities, QtUtilities
    from eric7.Toolbox import Startup

    global app, args, mainWindow, splash, restartArgs, inMainLoop

    sys.excepthook = excepthook
    if OSUtilities.isLinuxPlatform():
        multiprocessing.set_start_method("spawn")

    QGuiApplication.setDesktopFileName("eric7")

    options = [
        (
            "--config=configDir",
            "use the given directory as the one containing the config files",
        ),
        ("--debug", "activate debugging output to the console"),
        ("--no-multimedia", "disable the support of multimedia functions"),
        ("--no-open", "don't open anything at startup except that given in command"),
        ("--no-splash", "don't show the splash screen"),
        ("--no-crash", "don't check for a crash session file on startup"),
        ("--disable-crash", "disable the support for crash sessions"),
        (
            "--disable-plugin=<plug-in name>",
            "disable the given plug-in (may be repeated)",
        ),
        ("--plugin=plugin-file", "load the given plugin file (plugin development)"),
        (
            "--settings=settingsDir",
            "use the given directory to store the settings files",
        ),
        ("--small-screen", "adjust the interface for screens smaller than FHD"),
        ("--start-file", "load the most recently opened file"),
        ("--start-multi", "load the most recently opened multi-project"),
        ("--start-project", "load the most recently opened project"),
        ("--start-session", "load the global session file"),
        ("--", "indicate that there are options for the program to be debugged"),
        ("", "(everything after that is considered arguments for this program)"),
    ]
    appinfo = AppInfo.makeAppInfo(
        sys.argv,
        "Eric7",
        "[project | files... [--] [debug-options]]",
        "A Python IDE",
        options,
    )

    if "__PYVENV_LAUNCHER__" in os.environ:
        del os.environ["__PYVENV_LAUNCHER__"]

    # make sure our executable directory (i.e. that of the used Python
    # interpreter) is included in the executable search path
    pathList = os.environ["PATH"].split(os.pathsep)
    exeDir = os.path.dirname(sys.executable)
    if exeDir not in pathList:
        pathList.insert(0, exeDir)
    os.environ["PATH"] = os.pathsep.join(pathList)

    # set the library paths for plugins
    Startup.setLibraryPaths()

    if WEBENGINE_AVAILABLE:
        scheme = QWebEngineUrlScheme(b"qthelp")
        scheme.setSyntax(QWebEngineUrlScheme.Syntax.Path)
        scheme.setFlags(QWebEngineUrlScheme.Flag.SecureScheme)
        QWebEngineUrlScheme.registerScheme(scheme)

    app = EricApplication(sys.argv)
    ddindex = Startup.handleArgs(sys.argv, appinfo)

    logging.debug("Importing Preferences")
    from eric7 import Preferences  # __IGNORE_WARNING_I101__

    if Preferences.getUI("SingleApplicationMode"):
        handleSingleApplication(ddindex)

    # set the application style sheet
    app.setStyleSheetFile(Preferences.getUI("StyleSheet"))

    # set the search path for icons
    Startup.initializeResourceSearchPath(app)

    # generate and show a splash window, if not suppressed
    from eric7.UI.SplashScreen import (  # __IGNORE_WARNING_I101__
        NoneSplashScreen,
        SplashScreen,
    )

    if "--no-splash" in sys.argv and sys.argv.index("--no-splash") < ddindex:
        sys.argv.remove("--no-splash")
        ddindex -= 1
        splash = NoneSplashScreen()
    elif not Preferences.getUI("ShowSplash"):
        splash = NoneSplashScreen()
    else:
        splash = SplashScreen()
    QCoreApplication.processEvents()

    # modify the executable search path for the PyQt5 installer
    if OSUtilities.isWindowsPlatform():
        pyqtDataDir = QtUtilities.getPyQt6ModulesDirectory()
        if os.path.exists(os.path.join(pyqtDataDir, "bin")):
            path = os.path.join(pyqtDataDir, "bin")
        else:
            path = pyqtDataDir
        os.environ["PATH"] = path + os.pathsep + os.environ["PATH"]

    pluginFile = None
    noopen = False
    nocrash = False
    disablecrash = False
    disabledPlugins = []
    if "--no-open" in sys.argv and sys.argv.index("--no-open") < ddindex:
        sys.argv.remove("--no-open")
        ddindex -= 1
        noopen = True
    if "--no-crash" in sys.argv and sys.argv.index("--no-crash") < ddindex:
        sys.argv.remove("--no-crash")
        ddindex -= 1
        nocrash = True
    if "--disable-crash" in sys.argv and sys.argv.index("--disable-crash") < ddindex:
        sys.argv.remove("--disable-crash")
        ddindex -= 1
        disablecrash = True
    for arg in sys.argv[:]:
        if arg.startswith("--disable-plugin=") and sys.argv.index(arg) < ddindex:
            # extract the plug-in name
            pluginName = arg.replace("--disable-plugin=", "")
            sys.argv.remove(arg)
            ddindex -= 1
            disabledPlugins.append(pluginName)
    for arg in sys.argv:
        if arg.startswith("--plugin=") and sys.argv.index(arg) < ddindex:
            # extract the plugin development option
            pluginFile = arg.replace("--plugin=", "").replace('"', "")
            sys.argv.remove(arg)
            ddindex -= 1
            pluginFile = os.path.expanduser(pluginFile)
            pluginFile = os.path.abspath(pluginFile)
            break

    # is there a set of filenames or options on the command line,
    # if so, pass them to the UI
    if len(sys.argv) > 1:
        args = sys.argv[1:]

    # get the Qt translations directory
    qtTransDir = Preferences.getQtTranslationsDir()
    if not qtTransDir:
        qtTransDir = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)

    # Load translation files and install them
    loc = Startup.loadTranslators(qtTransDir, app, ("qscintilla",))

    # Initialize SSL stuff
    from eric7.EricNetwork.EricSslUtilities import initSSL  # __IGNORE_WARNING_I101__

    initSSL()

    splash.showMessage(QCoreApplication.translate("eric7_ide", "Starting..."))
    # We can only import these after creating the EricApplication because they
    # make Qt calls that need the EricApplication to exist.
    from eric7.UI.UserInterface import UserInterface  # __IGNORE_WARNING_I101__

    splash.showMessage(
        QCoreApplication.translate("eric7_ide", "Generating Main Window...")
    )
    mainWindow = UserInterface(
        app,
        loc,
        splash,
        pluginFile,
        disabledPlugins,
        noopen,
        nocrash,
        disablecrash,
        restartArgs,
        originalPathString,
    )
    app.lastWindowClosed.connect(app.quit)
    mainWindow.show()

    QTimer.singleShot(0, uiStartUp)

    # generate a graphical error handler
    from eric7.EricWidgets import EricErrorMessage  # __IGNORE_WARNING_I101__

    eMsg = EricErrorMessage.qtHandler()
    eMsg.setMinimumSize(600, 400)

    # start the event loop
    inMainLoop = True
    res = app.exec()
    logging.debug("Shutting down, result %d", res)
    logging.shutdown()
    sys.exit(res)


if __name__ == "__main__":
    main()
