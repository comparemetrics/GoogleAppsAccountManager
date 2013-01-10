# -*- coding: utf-8 -*-
#
# GoogleAppsAccountManager: groupowner/data
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

from GoogleAppsAccountManager import XMLNS_ATOM, XMLNS_APPS
from GoogleAppsAccountManager import data, errors

class GroupOwnerFeed(data.Feed):
    def __init__(self, status, xml_string):
        data.Feed.__init__(self, status, xml_string, GroupOwnerEntry)

class GroupOwnerEntry(data.Entry):
    def getOwnerEmail(self):
        membername = self.getValueFromPropertyElement("email")
        return membername.encode("utf-8")

