#
# GoogleAppsAccountManager: http
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2013-01-08, since 2012-12-28
#

import socket
import httplib
from GoogleAppsAccountManager import errors

def httpsRequest(method, server, path, header, body):
    for count in range(10):
        try:
            conn = httplib.HTTPSConnection(server)
            conn.request(method, path, body, header)
            res  = conn.getresponse()
        except socket.gaierror, e:
            raise errors.NotFoundServer()
        except Exception, e:
            continue
        else:
            return (res.read(), res.status)

    raise errors.UnknownError()

def httpsGETRequest(server, path, header, body=""):
    return httpsRequest("GET", server, path, header, body)

def httpsPOSTRequest(server, path, header, body):
    return httpsRequest("POST", server, path, header, body)

def httpsPUTRequest(server, path, header, body):
    return httpsRequest("PUT", server, path, header, body)

def httpsDELETERequest(server, path, header, body=""):
    return httpsRequest("DELETE", server, path, header, body)
