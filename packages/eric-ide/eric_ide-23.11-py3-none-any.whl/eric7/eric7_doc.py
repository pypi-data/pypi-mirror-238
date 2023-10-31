#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2003 - 2023 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
eric Documentation Generator.

This is the main Python script of the documentation generator. It is
this script that gets called via the source documentation interface.
This script can be used via the commandline as well.
"""

import fnmatch
import getopt
import glob
import os
import shutil
import sys

from eric7.DocumentationTools import TemplatesListsStyleCSS
from eric7.DocumentationTools.Config import eric7docDefaultColors
from eric7.DocumentationTools.IndexGenerator import IndexGenerator
from eric7.DocumentationTools.ModuleDocumentor import ModuleDocument
from eric7.DocumentationTools.QtHelpGenerator import QtHelpGenerator
from eric7.SystemUtilities import FileSystemUtilities, OSUtilities
from eric7.UI.Info import Version
from eric7.Utilities import ModuleParser

# list of supported filename extensions
supportedExtensions = [".py", ".pyw", ".ptl", ".rb"]


def usage():
    """
    Function to print some usage information.

    It prints a reference of all commandline parameters that may
    be used and ends the application.
    """
    print("eric7_doc")
    print()
    print("Copyright (c) 2003 - 2023 Detlev Offenbach <detlev@die-offenbachs.de>.")
    print()
    print("Usage:")
    print()
    print("  eric7_doc [options] files...")
    print()
    print("where files can be either python modules, package")
    print("directories or ordinary directories.")
    print()
    print("Options:")
    print()
    print("  -c filename or --style-sheet=filename")
    print("        Specify a CSS style sheet file to be used.")
    print("  -e or --noempty")
    print("        Don't include empty modules.")
    print("  --eol=eol-type")
    print("        Use the given eol type to terminate lines.")
    print("        Valid values are 'cr', 'lf' and 'crlf'.")
    print("  --exclude-file=pattern")
    print("        Specify a filename pattern of files to be excluded.")
    print("        This option may be repeated multiple times.")
    print("  -h or --help")
    print("        Show this help and exit.")
    print("  -i or --noindex")
    print("        Don't generate index files.")
    print("  -o directory or --outdir=directory")
    print("        Generate files in the named directory.")
    print("  -R, -r or --recursive")
    print("        Perform a recursive search for Python files.")
    print("  -s directory or --startdir=directory")
    print("        Start the documentation generation in the given directory.")
    print("  -t ext or --extension=ext")
    print("        Add the given extension to the list of file extensions.")
    print("        This option may be given multiple times.")
    print("  -V or --version")
    print("        Show version information and exit.")
    print("  -x directory or --exclude=directory")
    print("        Specify a directory basename to be excluded.")
    print("        This option may be repeated multiple times.")
    print()
    print("  --body-color=color")
    print("        Specify the text color.")
    print("  --body-background-color=color")
    print("        Specify the text background color.")
    print("  --l1header-color=color")
    print("        Specify the text color of level 1 headers.")
    print("  --l1header-background-color=color")
    print("        Specify the text background color of level 1 headers.")
    print("  --l2header-color=color")
    print("        Specify the text color of level 2 headers.")
    print("  --l2header-background-color=color")
    print("        Specify the text background color of level 2 headers.")
    print("  --cfheader-color=color")
    print("        Specify the text color of class and function headers.")
    print("  --cfheader-background-color=color")
    print("        Specify the text background color of class and function headers.")
    print("  --link-color=color")
    print("        Specify the text color of hyperlinks.")
    print()
    print("  --create-qhp")
    print("        Enable generation of QtHelp files.")
    print("  --qhp-outdir=directory")
    print("        Generate QtHelp files in the named directory.")
    print("  --qhp-namespace=namespace")
    print("        Use the given namespace (mandatory).")
    print("  --qhp-virtualfolder=folder")
    print("        Use the given virtual folder (mandatory).")
    print("        The virtual folder must not contain '/'.")
    print("  --qhp-filtername=name")
    print("        Use the given name for the custom filter.")
    print("  --qhp-filterattribs=attributes")
    print("        Add the given attributes to the filter list.")
    print("        Attributes must be separated by ':'.")
    print("  --qhp-title=title")
    print("        Use this as the title for the generated help (mandatory).")
    print("  --create-qhc")
    print("        Enable generation of QtHelp Collection files.")
    sys.exit(1)


def version():
    """
    Function to show the version information.
    """
    print(
        """eric7_doc  {0}\n"""
        """\n"""
        """eric API documentation generator.\n"""
        """\n"""
        """Copyright (c) 2003-2023 Detlev Offenbach"""
        """ <detlev@die-offenbachs.de>\n"""
        """This is free software; see LICENSE.txt for copying"""
        """ conditions.\n"""
        """There is NO warranty; not even for MERCHANTABILITY or FITNESS"""
        """ FOR A\n"""
        """PARTICULAR PURPOSE.""".format(Version)
    )
    sys.exit(1)


def main():
    """
    Main entry point into the application.
    """
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "c:ehio:Rrs:t:Vx:",
            [
                "exclude=",
                "extension=",
                "help",
                "noindex",
                "noempty",
                "outdir=",
                "recursive",
                "startdir=",
                "style-sheet=",
                "version",
                "exclude-file=",
                "eol=",
                "body-color=",
                "body-background-color=",
                "l1header-color=",
                "l1header-background-color=",
                "l2header-color=",
                "l2header-background-color=",
                "cfheader-color=",
                "cfheader-background-color=",
                "link-color=",
                "create-qhp",
                "qhp-outdir=",
                "qhp-namespace=",
                "qhp-virtualfolder=",
                "qhp-filtername=",
                "qhp-filterattribs=",
                "qhp-title=",
                "create-qhc",
            ],
        )
    except getopt.error:
        usage()

    excludeDirs = [
        ".svn",
        ".hg",
        ".git",
        ".ropeproject",
        ".eric7project",
        ".jedi",
        "dist",
        "build",
        "doc",
        "docs",
        "__pycache__",
    ]
    excludePatterns = []
    startDir = ""
    outputDir = "doc"
    recursive = False
    doIndex = True
    noempty = False
    newline = None

    stylesheetFile = ""
    colors = eric7docDefaultColors.copy()

    qtHelpCreation = False
    qtHelpOutputDir = "help"
    qtHelpNamespace = ""
    qtHelpFolder = "source"
    qtHelpFilterName = "unknown"
    qtHelpFilterAttribs = ""
    qtHelpTitle = ""
    qtHelpCreateCollection = False

    for k, v in opts:
        if k in ["-s", "--startdir"]:
            startDir = v
        elif k in ["-o", "--outdir"]:
            outputDir = v
        elif k in ["-R", "-r", "--recursive"]:
            recursive = True
        elif k in ["-x", "--exclude"]:
            excludeDirs.append(v)
        elif k == "--exclude-file":
            excludePatterns.append(v)
        elif k in ["-i", "--noindex"]:
            doIndex = False
        elif k in ["-e", "--noempty"]:
            noempty = True
        elif k in ["-h", "--help"]:
            usage()
        elif k in ["-V", "--version"]:
            version()
        elif k in ["-c", "--style-sheet"]:
            stylesheetFile = v
        elif k in ["-t", "--extension"]:
            if v.strip() and not v.startswith("."):
                v = ".{0}".format(v)
            supportedExtensions.append(v)
        elif k == "--eol":
            if v.lower() == "cr":
                newline = "\r"
            elif v.lower() == "lf":
                newline = "\n"
            elif v.lower() == "crlf":
                newline = "\r\n"

        elif k == "--body-color":
            colors["BodyColor"] = v
        elif k == "--body-background-color":
            colors["BodyBgColor"] = v
        elif k == "--l1header-color":
            colors["Level1HeaderColor"] = v
        elif k == "--l1header-background-color":
            colors["Level1HeaderBgColor"] = v
        elif k == "--l2header-color":
            colors["Level2HeaderColor"] = v
        elif k == "--l2header-background-color":
            colors["Level2HeaderBgColor"] = v
        elif k == "--cfheader-color":
            colors["CFColor"] = v
        elif k == "--cfheader-background-color":
            colors["CFBgColor"] = v
        elif k == "--link-color":
            colors["LinkColor"] = v

        elif k == "--create-qhp":
            qtHelpCreation = True
        elif k == "--qhp-outdir":
            qtHelpOutputDir = v
        elif k == "--qhp-namespace":
            qtHelpNamespace = v
        elif k == "--qhp-virtualfolder":
            qtHelpFolder = v
        elif k == "--qhp-filtername":
            qtHelpFilterName = v
        elif k == "--qhp-filterattribs":
            qtHelpFilterAttribs = v
        elif k == "--qhp-title":
            qtHelpTitle = v
        elif k == "--create-qhc":
            qtHelpCreateCollection = True

    if not args:
        usage()

    if qtHelpCreation and (
        qtHelpNamespace == ""
        or qtHelpFolder == ""
        or "/" in qtHelpFolder
        or qtHelpTitle == ""
    ):
        usage()

    basename = ""

    if outputDir:
        if not os.path.isdir(outputDir):
            try:
                os.makedirs(outputDir)
            except OSError:
                sys.stderr.write(
                    "Could not create output directory {0}.".format(outputDir)
                )
                sys.exit(2)
    else:
        outputDir = os.getcwd()
    outputDir = os.path.abspath(outputDir)

    if stylesheetFile:
        try:
            shutil.copy(stylesheetFile, os.path.join(outputDir, "styles.css"))
        except OSError:
            sys.stderr.write(
                "The CSS stylesheet '{0}' does not exist\n".format(stylesheetFile)
            )
            sys.exit(2)
    else:
        try:
            with open(os.path.join(outputDir, "styles.css"), "w") as sf:
                sf.write(TemplatesListsStyleCSS.cssTemplate.format(**colors))
        except OSError:
            sys.stderr.write(
                "The CSS stylesheet '{0}' could not be created\n".format(stylesheetFile)
            )
            sys.exit(2)

    indexGenerator = IndexGenerator(outputDir)

    if qtHelpCreation:
        if qtHelpOutputDir:
            if not os.path.isdir(qtHelpOutputDir):
                try:
                    os.makedirs(qtHelpOutputDir)
                except OSError:
                    sys.stderr.write(
                        "Could not create QtHelp output directory {0}.".format(
                            qtHelpOutputDir
                        )
                    )
                    sys.exit(2)
        else:
            qtHelpOutputDir = os.getcwd()
        qtHelpOutputDir = os.path.abspath(qtHelpOutputDir)

        qtHelpGenerator = QtHelpGenerator(
            outputDir,
            qtHelpOutputDir,
            qtHelpNamespace,
            qtHelpFolder,
            qtHelpFilterName,
            qtHelpFilterAttribs,
            qtHelpTitle,
            qtHelpCreateCollection,
        )

    if startDir:
        os.chdir(os.path.abspath(startDir))

    for arg in args:
        if os.path.isdir(arg):
            if os.path.exists(
                os.path.join(arg, FileSystemUtilities.joinext("__init__", ".py"))
            ):
                basename = os.path.dirname(arg)
                if arg == ".":
                    sys.stderr.write("The directory '.' is a package.\n")
                    sys.stderr.write("Please repeat the call giving its real name.\n")
                    sys.stderr.write("Ignoring the directory.\n")
                    continue
            else:
                basename = arg
            if basename:
                basename = "{0}{1}".format(basename, os.sep)

            if recursive and not os.path.islink(arg):
                names = [arg] + FileSystemUtilities.getDirs(arg, excludeDirs)
            else:
                names = [arg]
        else:
            basename = ""
            names = [arg]

        for filename in names:
            inpackage = False
            if os.path.isdir(filename):
                files = []
                for ext in supportedExtensions:
                    files.extend(
                        glob.glob(
                            os.path.join(
                                filename, FileSystemUtilities.joinext("*", ext)
                            )
                        )
                    )
                    initFile = os.path.join(
                        filename, FileSystemUtilities.joinext("__init__", ext)
                    )
                    if initFile in files:
                        inpackage = True
                        files.remove(initFile)
                        files.insert(0, initFile)
            else:
                if OSUtilities.isWindowsPlatform() and glob.has_magic(filename):
                    files = glob.glob(filename)
                else:
                    files = [filename]

            for file in files:
                skipIt = False
                for pattern in excludePatterns:
                    if fnmatch.fnmatch(os.path.basename(file), pattern):
                        skipIt = True
                        break
                if skipIt:
                    continue

                try:
                    print("Processing", file)
                    module = ModuleParser.readModule(
                        file,
                        basename=basename,
                        inpackage=inpackage,
                        extensions=supportedExtensions,
                    )
                    moduleDocument = ModuleDocument(module)
                    doc = moduleDocument.genDocument()
                except OSError as v:
                    sys.stderr.write("{0} error: {1}\n".format(file, v[1]))
                    continue
                except ImportError as v:
                    sys.stderr.write("{0} error: {1}\n".format(file, v))
                    continue
                except Exception as ex:
                    sys.stderr.write(
                        "{0} error while parsing: {1}\n".format(file, str(ex))
                    )
                    raise

                f = FileSystemUtilities.joinext(
                    os.path.join(outputDir, moduleDocument.name()), ".html"
                )

                # remember for index file generation
                indexGenerator.remember(file, moduleDocument, basename)

                # remember for QtHelp generation
                if qtHelpCreation:
                    qtHelpGenerator.remember(file, moduleDocument, basename)

                if (
                    noempty or file.endswith("__init__.py")
                ) and moduleDocument.isEmpty():
                    continue

                # generate output
                try:
                    with open(f, "w", encoding="utf-8", newline=newline) as out:
                        out.write(doc)
                except OSError as v:
                    sys.stderr.write("{0} error: {1}\n".format(file, v[1]))
                except Exception as ex:
                    sys.stderr.write(
                        "{0} error while writing: {1}\n".format(file, str(ex))
                    )
                    raise
                else:
                    sys.stdout.write("{0} ok\n".format(f))

                sys.stdout.flush()
                sys.stderr.flush()

    sys.stdout.write("code documentation generated")

    sys.stdout.flush()
    sys.stderr.flush()

    # write index files
    if doIndex:
        indexGenerator.writeIndices(basename, newline=newline)

    # generate the QtHelp files
    if qtHelpCreation:
        qtHelpGenerator.generateFiles(newline=newline)

    sys.exit(0)


if __name__ == "__main__":
    main()

#
# eflag: noqa = M801
