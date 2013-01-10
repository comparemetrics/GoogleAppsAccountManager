# -*- coding: utf-8 -*-
#
# GoogleAppsAccountManager: multipledomainuser/data
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

from GoogleAppsAccountManager import XMLNS_ATOM, XMLNS_APPS
from GoogleAppsAccountManager import data, errors

class UserFeed_M(data.Feed):
    def __init__(self, status, xml_string):
        data.Feed.__init__(self, status, xml_string, UserEntry_M)

    def getNextLink(self):
        next_link = data.Feed.getNextLink(self)
        if next_link == "!!END!!":
            return ""
        else:
            return next_link

class UserEntry_M(data.Entry):
    def getUserEmail(self):
        user_email = self.getValueFromPropertyElement("userEmail")
        return user_email.encode("utf-8")

    def getSn(self):
        sn = self.getValueFromPropertyElement("lastName")
        return sn.encode("utf-8")

    def getGivenName(self):
        given_name = self.getValueFromPropertyElement("firstName")
        return given_name.encode("utf-8")

    def isActive(self):
        active = self.getValueFromPropertyElement("isSuspended")
        if active == "false":
            active = "True"
        else:
            active = "False"
        return active.encode("utf-8")

    def isAdmin(self):
        is_admin = self.getValueFromPropertyElement("isAdmin")
        if is_admin == "true":
            is_admin = "True"
        else:
            is_admin = "False"
        return is_admin.encode("utf-8")

    def isChangePasswordAtNextLogin(self):
        is_change = self.getValueFromPropertyElement("isChangePasswordAtNextLogin")
        if is_change == "true":
            is_change = "True"
        else:
            is_change = "False"
        return is_change.encode("utf-8")

    def isAgreedToTerms(self):
        is_agreed = self.getValueFromPropertyElement("agreedToTerms")
        if is_agreed == "true":
            is_agreed = "True"
        else:
            is_agreed = "False"
        return is_agreed.encode("utf-8")

    def setPassword(self, new_password, hash_function_name):
        self.setNewValueToPropertyElement(
                  "password"
                , new_password.decode("utf-8")
                )
        return self.setNewValueToPropertyElement(
                  "hashFunction"
                , hash_function_name.decode("utf-8")
                )

    def setSn(self, new_sn):
        return self.setValueToPropertyElement(
                  "lastName"
                , new_sn.decode("utf-8")
                )

    def setGivenName(self, new_given_name):
        return self.setValueToPropertyElement(
                  "firstName"
                , new_given_name.decode("utf-8")
                )

    def setSuspended(self, new_is_suspended):
        return self.setValueToPropertyElement(
                  "isSuspended"
                , new_is_suspended.decode("utf-8")
                )

    def setAdmin(self, new_is_admin):
        return self.setValueToPropertyElement(
                  "isAdmin"
                , new_is_admin.decode("utf-8")
                )

    def setChangePassword(self, new_is_change_password):
        return self.setValueToPropertyElement(
                  "isChangePasswordAtNextLogin"
                , new_is_change_password.decode("utf-8")
                )

    def setNewUserEmail(self, new_user_email):
        return self.setNewValueToPropertyElement(
                  "newEmail"
                , new_user_email.decode("utf-8")
                )

