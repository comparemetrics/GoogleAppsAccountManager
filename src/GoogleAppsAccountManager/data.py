# -*- coding: utf-8 -*-
#
# GoogleAppsAccountManager: data
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

import urllib
import xml.etree.ElementTree as ET
from GoogleAppsAccountManager import XMLNS_ATOM, XMLNS_APPS
from GoogleAppsAccountManager import errors

class Feed(object):
    def __init__(self, status, xml_string, entry_class):
        self.xml_tree = ET.fromstring(xml_string)
        self.entries = []

        for entry in self.xml_tree.findall("{0}entry".format(XMLNS_ATOM)):
            obj = entry_class(status, xml_element=entry)
            self.entries += [obj]

        # Check error
        if self.xml_tree.find("error") is not None:
            raise errors.ResponseError_xml(self.xml_tree)

    def getNextLink(self):
        for link in self.xml_tree.findall("{0}link".format(XMLNS_ATOM)):
            if link.get("rel") == "next":
                return link.get("href")

        return "!!END!!"

class Entry(object):
    def __init__(self, status, xml_element=None, xml_string=None):
        if (xml_element is None) and (xml_string is None):
            raise errors.ArgumentsError(
                    "Few arguments: XML object or XML string is needed\n"
                    )
        elif (xml_element is not None) and (xml_string is not None):
            raise errors.ArgumentsError("Too much arguments\n")

        if xml_element is not None:
            self.xml_element = xml_element
        elif xml_string is not None:
            try:
                self.xml_element = ET.fromstring(xml_string)
            except ET.ParseError:
                if (status / 100) == 2:
                    # When status is 20x, success. So make dummy xml object.
                    self.xml_element = ET.fromstring("<success />")
                else:
                    # Unknown error - maybe, url format is wrong
                    raise errors.ResponseError_string(xml_string)

        # Check error
        if self.xml_element.find("error") is not None:
            raise errors.ResponseError_xml(self.xml_element)

    def getRawXMLString(self):
        return ET.tostring(self.xml_element)

    def getRawXML(self):
        return self.xml_element

    def getValueFromPropertyElement(self, attribute_name):
        for e in self.xml_element.findall("{0}property".format(XMLNS_APPS)):
            if e.get("name") == attribute_name:
                return e.get("value")
        raise errors.XMLParseError()

    def setValueToPropertyElement(self, attribute_name, value):
        for e in self.xml_element.findall("{0}property".format(XMLNS_APPS)):
            if e.get("name") == attribute_name:
                e.set("value", value)
                return self.getRawXMLString()
        raise errors.XMLParseError()

    def setNewValueToPropertyElement(self, attribute_name, value):
        import copy
        e = copy.deepcopy(self.xml_element.findall("{0}property".format(XMLNS_APPS))[0])
        e.set("name", attribute_name)
        e.set("value", value)
        self.xml_element.append(e)
        return self.getRawXMLString()

