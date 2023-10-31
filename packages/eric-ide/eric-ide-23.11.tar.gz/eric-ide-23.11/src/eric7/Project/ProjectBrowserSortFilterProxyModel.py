# -*- coding: utf-8 -*-

# Copyright (c) 2006 - 2023 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the browser sort filter proxy model.
"""

import contextlib

from eric7.UI.BrowserSortFilterProxyModel import BrowserSortFilterProxyModel


class ProjectBrowserSortFilterProxyModel(BrowserSortFilterProxyModel):
    """
    Class implementing the browser sort filter proxy model.
    """

    def __init__(self, filterType, parent=None):
        """
        Constructor

        @param filterType type of filter to apply
        @param parent reference to the parent object (QObject)
        """
        BrowserSortFilterProxyModel.__init__(self, parent)
        self.__filterType = filterType
        self.setDynamicSortFilter(True)

    def filterAcceptsRow(self, source_row, source_parent):
        """
        Public method to filter rows.

        It implements a filter to suppress the display of non public
        classes, methods and attributes.

        @param source_row row number (in the source model) of item (integer)
        @param source_parent index of parent item (in the source model)
            of item (QModelIndex)
        @return flag indicating, if the item should be shown (boolean)
        """
        sindex = self.sourceModel().index(source_row, 0, source_parent)
        if not sindex.isValid():
            return False
        sitem = self.sourceModel().item(sindex)
        with contextlib.suppress(AttributeError):
            if self.__filterType not in sitem.getProjectTypes():
                return False

        if self.hideNonPublic:
            return sitem.isPublic()
        else:
            return True
