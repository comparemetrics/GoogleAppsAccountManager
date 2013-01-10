# -*- coding: utf-8 -*-
#
# GoogleAppsAccountManager: multipledomainnickname/data
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

from GoogleAppsAccountManager import XMLNS_ATOM, XMLNS_APPS
from GoogleAppsAccountManager import data, errors

class AliasFeed_M(data.Feed):
    def __init__(self, status, xml_string):
        data.Feed.__init__(self, status, xml_string, AliasEntry_M)

    def getNextLink(self):
        next_link = data.Feed.getNextLink(self)
        if next_link == "!!END!!":
            return ""
        else:
            return next_link

class AliasEntry_M(data.Entry):
    def getAliasEmail(self):
        user_email = self.getValueFromPropertyElement("aliasEmail")
        return user_email.encode("utf-8")

    def getUserEmail(self):
        user_email = self.getValueFromPropertyElement("userEmail")
        return user_email.encode("utf-8")

