# -*- coding: utf-8 -*-

# Copyright (c) 2005 - 2023 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a Diff lexer with some additional methods.
"""

from PyQt6.Qsci import QsciLexerDiff

from .Lexer import Lexer


class LexerDiff(Lexer, QsciLexerDiff):
    """
    Subclass to implement some additional lexer dependant methods.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent parent widget of this lexer
        """
        QsciLexerDiff.__init__(self, parent)
        Lexer.__init__(self)

        self.keywordSetDescriptions = []

    def isCommentStyle(self, style):
        """
        Public method to check, if a style is a comment style.

        @param style style to check (integer)
        @return flag indicating a comment style (boolean)
        """
        return style in [LexerDiff.Comment]

    def isStringStyle(self, style):  # noqa: U100
        """
        Public method to check, if a style is a string style.

        @param style style to check (integer)
        @return flag indicating a string style (boolean)
        """
        return False

    def defaultKeywords(self, kwSet):
        """
        Public method to get the default keywords.

        @param kwSet number of the keyword set (integer)
        @return string giving the keywords (string) or None
        """
        return QsciLexerDiff.keywords(self, kwSet)


def createLexer(variant="", parent=None):  # noqa: U100
    """
    Function to instantiate a lexer object.

    @param variant name of the language variant
    @type str
    @param parent parent widget of this lexer
    @type QObject
    @return instantiated lexer object
    @rtype LexerDiff
    """
    return LexerDiff(parent=parent)
