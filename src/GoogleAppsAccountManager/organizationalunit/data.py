# -*- coding: utf-8 -*-
#
# GoogleAppsAccountManager: organizationalunit/data
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

import urllib
from GoogleAppsAccountManager import XMLNS_ATOM, XMLNS_APPS
from GoogleAppsAccountManager import data,errors

class CustomerIdEntry(data.Entry):
    def getCustomerId(self):
        return self.getValueFromPropertyElement("customerId")

class OuFeed(data.Feed):
    def __init__(self, status, xml_string):
        data.Feed.__init__(self, status, xml_string, OuEntry)

class OuEntry(data.Entry):
    def getOuPath(self, unquoted=True):
        ou_path = self.getValueFromPropertyElement("orgUnitPath")
        if unquoted:
            return "/" + urllib.unquote(ou_path)
        else:
            return ou_path

    def getOuBaseName(self):
        ou_basename = self.getValueFromPropertyElement("name")
        return ou_basename.encode("utf-8")

    def getOuParentPath(self, unquoted=True):
        ou_parent_path = self.getValueFromPropertyElement("parentOrgUnitPath")
        if unquoted:
            return "/" + urllib.unquote(ou_parent_path)
        else:
            return ou_parent_path

    def getOuDescription(self):
        ou_description = self.getValueFromPropertyElement("description")
        return ou_description.encode("utf-8")

    def setOuDescription(self, new_description_utf8):
        return self.setValueToPropertyElement(
                  "description"
                , new_description_utf8.decode("utf-8")
                )

    def setOuBlockInheritance(self, new_blockInheritance):
        return self.setValueToPropertyElement(
                  "blockInheritance"
                , new_blockInheritance.decode("utf-8")
                )

