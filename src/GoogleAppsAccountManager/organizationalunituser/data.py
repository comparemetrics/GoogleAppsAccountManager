# -*- coding: utf-8 -*-
#
# GoogleAppsAccountManager: organizationalunituser/data
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

from GoogleAppsAccountManager import XMLNS_ATOM, XMLNS_APPS
from GoogleAppsAccountManager import data,errors
from GoogleAppsAccountManager.organizationalunit.data import OuEntry

class CustomerIdEntry(data.Entry):
    def getCustomerId(self):
        return self.getValueFromPropertyElement("customerId")

class OuUserFeed(data.Feed):
    def __init__(self, status, xml_string):
        data.Feed.__init__(self, status, xml_string, OuUserEntry)

class OuUserEntry(OuEntry):
    def getUserEmail(self):
        user_email = self.getValueFromPropertyElement("orgUserEmail")
        return user_email.encode("utf-8")

