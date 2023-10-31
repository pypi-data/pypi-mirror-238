# -*- coding: utf-8 -*-

# Copyright (c) 2022 - 2023 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing Python related utility functions.
"""

import os
import sys
import sysconfig


def getPythonExecutable():
    """
    Function to determine the path of the (non-windowed) Python executable.

    @return path of the Python executable
    @rtype str
    """
    if sys.platform.startswith("linux"):
        return sys.executable
    elif sys.platform == "darwin":
        return sys.executable.replace("pythonw", "python")
    else:
        return sys.executable.replace("pythonw.exe", "python.exe")


def getPythonLibraryDirectory():
    """
    Function to determine the path to Python's library directory.

    @return path to the Python library directory
    @rtype str
    """
    return sysconfig.get_path("platlib")


def getPythonScriptsDirectory():
    """
    Function to determine the path to Python's scripts directory.

    @return path to the Python scripts directory
    @rtype str
    """
    return sysconfig.get_path("scripts")


def getPythonLibPath():
    """
    Function to determine the path to Python's library.

    @return path to the Python library (string)
    """
    return sysconfig.get_path("platstdlib")


def getPythonVersion():
    """
    Function to get the Python version (major, minor) as an integer value.

    @return An integer representing major and minor version number (integer)
    """
    return sys.hexversion >> 16


def determinePythonVersion(filename, source, editor=None):
    """
    Function to determine the python version of a given file.

    @param filename name of the file with extension (str)
    @param source of the file (str)
    @param editor reference to the editor, if the file is opened
        already (Editor object)
    @return Python version if file is Python3 (int)
    """
    from eric7 import Preferences, Utilities
    from eric7.EricWidgets.EricApplication import ericApp

    pyAssignment = {
        "Python3": 3,
        "MicroPython": 3,
        "Cython": 3,
    }

    if not editor:
        viewManager = ericApp().getObject("ViewManager")
        editor = viewManager.getOpenEditor(filename)

    # Maybe the user has changed the language
    if editor and editor.getFileType() in pyAssignment:
        return pyAssignment[editor.getFileType()]

    pyVer = 0
    if filename:
        if not source and os.path.exists(filename):
            source = Utilities.readEncodedFile(filename)[0]
        flags = Utilities.extractFlags(source)
        ext = os.path.splitext(filename)[1]
        py3Ext = Preferences.getPython("Python3Extensions")
        project = ericApp().getObject("Project")
        basename = os.path.basename(filename)

        if "FileType" in flags:
            pyVer = pyAssignment.get(flags["FileType"], 0)
        elif project.isOpen() and project.isProjectFile(filename):
            language = project.getEditorLexerAssoc(basename)
            if not language:
                language = Preferences.getEditorLexerAssoc(basename)
            if language == "Python3":
                pyVer = pyAssignment[language]

        if pyVer:
            # Skip the next tests
            pass
        elif (
            Preferences.getProject("DeterminePyFromProject")
            and project.isOpen()
            and project.isProjectFile(filename)
            and ext in py3Ext
        ):
            pyVer = pyAssignment.get(project.getProjectLanguage(), 0)
        elif ext in py3Ext:
            pyVer = 3
        elif source:
            if isinstance(source, str):
                line0 = source.splitlines()[0]
            else:
                line0 = source[0]
            if line0.startswith("#!") and (("python3" in line0) or ("python" in line0)):
                pyVer = 3

        if pyVer == 0 and ext in py3Ext:
            pyVer = 3

    return pyVer
