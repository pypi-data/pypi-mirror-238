# -*- coding: utf-8 -*-

# Copyright (c) 2020 - 2023 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a check for use of insecure md4, md5, or sha1 hash
functions in hashlib.new().
"""

import sys

from Security.SecurityDefaults import SecurityDefaults

#
# This is a modified version of the one found in the bandit package.
#
# Original Copyright 2014 Hewlett-Packard Development Company, L.P.
#
# SPDX-License-Identifier: Apache-2.0
#


def getChecks():
    """
    Public method to get a dictionary with checks handled by this module.

    @return dictionary containing checker lists containing checker function and
        list of codes
    @rtype dict
    """
    return {
        "Call": [
            (checkHashlib, ("S331",)),
        ],
    }


def _hashlibFunc(reportError, context, config):
    """
    Function to check for use of insecure md4, md5, sha or sha1 hash functions
    in hashlib.new() if 'usedforsecurity' is not set to 'False'.

    @param reportError function to be used to report errors
    @type func
    @param context security context object
    @type SecurityContext
    @param config dictionary with configuration data
    @type dict
    """
    insecureHashes = (
        [h.lower() for h in config["insecure_hashes"]]
        if config and "insecure_hashes" in config
        else SecurityDefaults["insecure_hashes"]
    )

    if isinstance(context.callFunctionNameQual, str):
        qualnameList = context.callFunctionNameQual.split(".")

        if "hashlib" in qualnameList:
            func = qualnameList[-1]
            keywords = context.callKeywords

            if func in insecureHashes:
                if keywords.get("usedforsecurity", "True") == "True":
                    reportError(
                        context.node.lineno - 1,
                        context.node.col_offset,
                        "S332",
                        "H",
                        "H",
                        func.upper(),
                    )
            elif func == "new":
                args = context.callArgs
                name = args[0] if args else keywords.get("name")
                if (
                    isinstance(name, str)
                    and name.lower() in insecureHashes
                    and keywords.get("usedforsecurity", "True") == "True"
                ):
                    reportError(
                        context.node.lineno - 1,
                        context.node.col_offset,
                        "S332",
                        "H",
                        "H",
                        name.upper(),
                    )


def _hashlibNew(reportError, context, config):
    """
    Function to check for use of insecure md4, md5, sha or sha1 hash functions
    in hashlib.new().

    @param reportError function to be used to report errors
    @type func
    @param context security context object
    @type SecurityContext
    @param config dictionary with configuration data
    @type dict
    """
    insecureHashes = (
        [h.lower() for h in config["insecure_hashes"]]
        if config and "insecure_hashes" in config
        else SecurityDefaults["insecure_hashes"]
    )

    if isinstance(context.callFunctionNameQual, str):
        qualnameList = context.callFunctionNameQual.split(".")
        func = qualnameList[-1]
        if "hashlib" in qualnameList and func == "new":
            args = context.callArgs
            keywords = context.callKeywords
            name = args[0] if args else keywords.get("name")
            if isinstance(name, str) and name.lower() in insecureHashes:
                reportError(
                    context.node.lineno - 1,
                    context.node.col_offset,
                    "S331",
                    "M",
                    "H",
                    name.upper(),
                )


def checkHashlib(reportError, context, config):
    """
    Function to check for use of insecure md4, md5, sha or sha1 hash functions
    in hashlib.new().

    @param reportError function to be used to report errors
    @type func
    @param context security context object
    @type SecurityContext
    @param config dictionary with configuration data
    @type dict
    """
    if sys.version_info >= (3, 9):
        _hashlibFunc(reportError, context, config)
    else:
        _hashlibNew(reportError, context, config)
