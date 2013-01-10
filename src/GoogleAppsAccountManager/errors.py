# -*- coding: utf-8 -*-
#
# GoogleAppsAccountManager: errors
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

# DNS resolution failed
class NotFoundServer(Exception):
    pass

# Administrator's login failed
class AdminLoginError(Exception):
    pass

# Unknown error
class UnknownError(Exception):
    import traceback
    errortrace = traceback.format_exc()

# Argument error
class ArgumentsError(Exception):
    def __init__(self, msg=""):
        self.errormessage = msg

# XML perse error
class XMLParseError(Exception):
    pass

######################## Error because of user's input ########################

# ResponseError - connection succeeded, but get error response (xml object)
class ResponseError_xml(Exception):
    def __init__(self, xml_object):
        def conv(s):
            if isinstance(s, unicode): return s.encode("utf-8")
            else:                      return s

        self.error_code    = xml_object.find("error").get("errorCode")
        self.invalid_input = conv(xml_object.find("error").get("invalidInput"))
        self.reason        = xml_object.find("error").get("reason")

# ResponseError - connection succeeded, but get error response (string)
class ResponseError_string(Exception):
    reason = ""
    def __init__(self, xml_string):
        self.reason = xml_string

# No parameters specified
class NoParametersError(Exception):
    pass

