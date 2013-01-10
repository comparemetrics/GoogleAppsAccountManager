# -*- coding: utf-8 -*-
#
# GoogleAppsAccountManager: nickname/data
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

from GoogleAppsAccountManager import XMLNS_ATOM, XMLNS_APPS
from GoogleAppsAccountManager import data, errors

class NicknameFeed(data.Feed):
    def __init__(self, status, xml_string):
        data.Feed.__init__(self, status, xml_string, NicknameEntry)

    def getNextLink(self):
        next_link = data.Feed.getNextLink(self)
        if next_link == "!!END!!":
            return ""
        else:
            return next_link

class NicknameEntry(data.Entry):
    def getNickname(self):
        login_space = self.xml_element.find("{0}nickname".format(XMLNS_APPS))
        return login_space.get("name").encode("utf-8")

    def getUserName(self):
        login_space = self.xml_element.find("{0}login".format(XMLNS_APPS))
        return login_space.get("userName").encode("utf-8")

