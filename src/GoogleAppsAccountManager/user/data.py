# -*- coding: utf-8 -*-
#
# GoogleAppsAccountManager: user/data
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

from GoogleAppsAccountManager import XMLNS_ATOM, XMLNS_APPS
from GoogleAppsAccountManager import data, errors

class UserFeed(data.Feed):
    def __init__(self, status, xml_string):
        data.Feed.__init__(self, status, xml_string, UserEntry)

    def getNextLink(self):
        next_link = data.Feed.getNextLink(self)
        if next_link == "!!END!!":
            return ""
        else:
            return next_link

class UserEntry(data.Entry):
    def getUserName(self):
        login_space = self.xml_element.find("{0}login".format(XMLNS_APPS))
        return login_space.get("userName").encode("utf-8")

    def getActive(self):
        login_space = self.xml_element.find("{0}login".format(XMLNS_APPS))
        if login_space.get("suspended") == "false":
            active = "True"
        else:
            active = "False"
        return active.encode("utf-8")

    def getSn(self):
        name_space = self.xml_element.find("{0}name".format(XMLNS_APPS))
        return name_space.get("familyName").encode("utf-8")

    def getGivenName(self):
        name_space = self.xml_element.find("{0}name".format(XMLNS_APPS))
        return name_space.get("givenName").encode("utf-8")

    def getQuota(self):
        quota_space = self.xml_element.find("{0}quota".format(XMLNS_APPS))
        return quota_space.get("limit").encode("utf-8")

    def setUserPassword(self, new_password, hashFunctionName):
        login_space = self.xml_element.find("{0}login".format(XMLNS_APPS))
        login_space.set("password", new_password)
        login_space.set("hashFunctionName", hashFunctionName)
        return self.getRawXMLString()

    def setUserSn(self, new_sn_utf8):
        name_space = self.xml_element.find("{0}name".format(XMLNS_APPS))
        name_space.set("familyName", new_sn_utf8.decode("utf-8"))
        return self.getRawXMLString()

    def setUserGivenName(self, new_givenName_utf8):
        name_space = self.xml_element.find("{0}name".format(XMLNS_APPS))
        name_space.set("givenName", new_givenName_utf8.decode("utf-8"))
        return self.getRawXMLString()

    def setUserSuspended(self, new_suspended):
        login_space = self.xml_element.find("{0}login".format(XMLNS_APPS))
        login_space.set("suspended", new_suspended.lower())
        return self.getRawXMLString()

    # Quota control is not available
    def setUserLimit(self, new_limit):
        quota_space = self.xml_element.find("{0}quota".format(XMLNS_APPS))
        quota_space.set("limit", new_limit)
        return self.getRawXMLString()
