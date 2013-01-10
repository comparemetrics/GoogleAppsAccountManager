# -*- coding: utf-8 -*-
#
# GoogleAppsAccountManager: groupmember/data
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

from GoogleAppsAccountManager import XMLNS_ATOM, XMLNS_APPS
from GoogleAppsAccountManager import data, errors

class GroupMemberFeed(data.Feed):
    def __init__(self, status, xml_string):
        data.Feed.__init__(self, status, xml_string, GroupMemberEntry)

class GroupMemberEntry(data.Entry):
    def getMemberId(self):
        membername = self.getValueFromPropertyElement("memberId")
        return membername.encode("utf-8")

