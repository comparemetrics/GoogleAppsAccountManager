# -*- coding: utf-8 -*-
#
# GoogleAppsAccountManager: group/data
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

from GoogleAppsAccountManager import XMLNS_ATOM, XMLNS_APPS
from GoogleAppsAccountManager import data, errors

class GroupFeed(data.Feed):
    def __init__(self, status, xml_string):
        data.Feed.__init__(self, status, xml_string, GroupEntry)

class GroupEntry(data.Entry):
    def getGroupId(self):
        group_id = self.getValueFromPropertyElement("groupId")
        return group_id.encode("utf-8")

    def getGroupName(self):
        group_name = self.getValueFromPropertyElement("groupName")
        return group_name.encode("utf-8")

    def getGroupDescription(self):
        group_description = self.getValueFromPropertyElement("description")
        return group_description.encode("utf-8")

    def setGroupName(self, new_name_utf8):
        return self.setValueToPropertyElement(
                  "groupName"
                , new_name_utf8.decode("utf-8")
                )

    def setGroupDescription(self, new_description_utf8):
        return self.setValueToPropertyElement(
                  "description"
                , new_description_utf8.decode("utf-8")
                )

