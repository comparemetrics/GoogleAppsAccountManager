#
# GoogleAppsAccountManager: organizationalunituser/client
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

import urllib
from GoogleAppsAccountManager import http, errors
from GoogleAppsAccountManager.organizationalunituser import data

def getCustomerId(auth_token):
    from GoogleAppsAccountManager.organizationalunit import client
    return client.getCustomerId(auth_token)

def getOuOfUser(auth_token, customer_id, user_email):
    user_email_quoted = urllib.quote(user_email)

    server = "apps-apis.google.com"
    path   = "/a/feeds/orguser/2.0/{0}/{1}".format(customer_id, user_email_quoted)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsGETRequest(server, path, header)

    # Get organizational unit entry
    ou_user_entry = data.OuUserEntry(status, xml_string=response)

    return {user_email: ou_user_entry}

def getAllUsersWithOu(auth_token, customer_id, display_obj=None):
    ou_user_info         = {}

    body      = ""
    header = { "Content-type" : "application/atom+xml"
              , "Authorization": "GoogleLogin auth={0}".format(auth_token)
              }

    next_link = None
    while next_link != "!!END!!":
        (tmp_ou_user_info, next_link) = get100UsersWithOu(auth_token, customer_id, next_link, display_obj)
        ou_user_info.update(tmp_ou_user_info)

    return ou_user_info

def get100UsersWithOu(auth_token, customer_id, next_link=None, display_obj=None):
    ou_user_info         = {}
    organizational_units = []

    server = "apps-apis.google.com"
    path   = "/a/feeds/orguser/2.0/{0}?get=all".format(customer_id)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    if next_link is None:
        (response, status) = http.httpsGETRequest(server, path, header)
    else:
        path     = "/" + "/".join(next_link.split("/")[3:])
        (response, status) = http.httpsGETRequest(server, path, header)

    # Get organizational unit feed
    ou_user_feed = data.OuUserFeed(status, response)

    # Retrieve organizational unit information from xml string
    for ou_user_entry in ou_user_feed.entries:
        user_email = ou_user_entry.getUserEmail()
        ou_user_info[user_email] = ou_user_entry

        if display_obj:
            username = user_email.split("@")[0]
            ou_path = ou_user_entry.getOuPath()
            header = ["username", "ou"]
            value  = {"username" : username, "ou": ou_path}
            display_obj.display(*header, **value)

    # Check 100 over?
    next_link = ou_user_feed.getNextLink()

    return (ou_user_info, next_link)

def outputAllUsersWithOu(auth_token, customer_id):
    from GoogleAppsAccountManager import display
    getAllUsersWithOu(auth_token, customer_id, display.Display())

def moveUserToOu(auth_token, customer_id, user_email, new_ou_path):
    from GoogleAppsAccountManager import template

    user_email_quoted = urllib.quote(user_email)

    server = "apps-apis.google.com"
    path   = ( "/a/feeds/orguser/2.0/{0}/{1}"
               .format(customer_id, user_email_quoted)
             )
    header = { "Content-type"   : "application/atom+xml"
             , "Authorization"  : "GoogleLogin auth={0}".format(auth_token)
             }

    ou_user_info    = getOuOfUser(auth_token, customer_id, user_email)
    old_ou_path_rel = ou_user_info[user_email].getOuPath(unquoted=False)
    new_ou_path_rel = urllib.quote(new_ou_path[1:])
    if new_ou_path_rel == "":
        new_ou_path_rel = "/"

    body   = template.OU_USER_ENTRY.format(
                  customer_id       = customer_id
                , user_email_quoted = user_email_quoted
                , old_ou_path_rel   = old_ou_path_rel
                , new_ou_path_rel   = new_ou_path_rel
                )

    # HTTP Request
    (response, status) = http.httpsPUTRequest(server, path, header, body)

    # Get organizational unit entry
    ou_user_entry = data.OuUserEntry(status, xml_string=response)
    try:
        return ou_user_entry.getUserEmail()
    except:
        raise errors.ResponseError_xml(ou_user_entry.getRawXML())

