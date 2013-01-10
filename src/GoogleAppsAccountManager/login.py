#
# GoogleAppsAccountManager: login
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

import socket
import httplib
import urllib
from GoogleAppsAccountManager import MY_APP_NAME
from GoogleAppsAccountManager import errors

def clientLogin(admin_email, admin_pass):
    body    = urllib.urlencode(
                { "accountType" : "HOSTED_OR_GOOGLE"
                , "Email"       : admin_email
                , "Passwd"      : admin_pass
                , "service"     : "apps"
                , "source"      : MY_APP_NAME
                }
              )
    headers = { "Content-type" : "application/x-www-form-urlencoded"
              }

    # Connect and get response
    try:
        conn = httplib.HTTPSConnection("www.google.com")
        conn.request("POST", "/accounts/ClientLogin", body, headers)
        res  = conn.getresponse()
    except socket.gaierror, e:
        raise errors.NotFoundServer()
    except:
        import traceback
        traceback.print_exc()
        raise errors.UnknownError()

    # Check if I get auth token
    auth_token = None
    for line in res.read().split("\n"):
        if "Auth=" in line:
            auth_token = line.replace("Auth=", "")
            break

    if not auth_token:
        raise errors.AdminLoginError()

    domain = admin_email.split("@")[1]

    # Return Handler object
    return auth_token

