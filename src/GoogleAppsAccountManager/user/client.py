#
# GoogleAppsAccountManager: user/client
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

from GoogleAppsAccountManager import http, errors
from GoogleAppsAccountManager.user import data

def createUser( domain
              , auth_token
              , user_name
              , password
              , sn
              , given_name
              , hash_function_name="SHA-1"
              , suspended="false"
              , limit="10240" # Not available
              ):
    from GoogleAppsAccountManager import template

    server = "apps-apis.google.com"
    path   = "/a/feeds/{0}/user/2.0".format(domain)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }
    # Quota is not available.
    # So nothing will be done whether limit has value or not.
    # With an eye toward a future, I leave this implemention
    limit  = "10240"
    body   = template.USER_ENTRY.format( user_name=user_name
                                       , password=password
                                       , sn=sn
                                       , given_name=given_name
                                       , hash_function_name=hash_function_name
                                       , suspended=suspended
                                       , limit=limit
                                       , domain=domain
                                       )

    # HTTP Request
    (response, status) = http.httpsPOSTRequest(server, path, header, body)

    user_entry = data.UserEntry(status, xml_string=response)
    return True

def updateUser( domain
              , auth_token
              , user_name
              , password=None
              , sn=None
              , given_name=None
              , hash_function_name="SHA-1"
              , suspended=None
              , limit=None # Not available
              ):
    server = "apps-apis.google.com"
    path   = "/a/feeds/{0}/user/2.0/{1}".format(domain, user_name)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    users_info = get1User(domain, auth_token, user_name)
    body   = ""
    if password is not None:
        body = users_info[user_name].setUserPassword(password, hash_function_name)

    if sn is not None:
        body = users_info[user_name].setUserSn(sn)

    if given_name is not None:
        body = users_info[user_name].setUserGivenName(given_name)

    if suspended is not None:
        if (suspended.lower() == "true") or (suspended.lower() == "false"):
            body = users_info[user_name].setUserSuspended(suspended)
        else:
            raise errors.ArgumentsError(
                    "suspended must be \"true\" or \"false\"\n"
                    )

    # Quota is not available.
    # So nothing will be done whether limit has value or not.
    # With an eye toward a future, I leave this implemention
    if (limit is not None) or (limit is None):
        pass
    else:
        try:
            int(limit)
        except ValueError:
            raise errors.ArgumentsError("limit must be Integer\n")
        else:
            body = users_info[user_name].setUserLimit(limit)

    if body == "":
        raise errors.NoParametersError()

    # HTTP Request
    (response, status) = http.httpsPUTRequest(server, path, header, body)

    user_entry = data.UserEntry(status, xml_string=response)
    return True

def deleteUser(domain, auth_token, user_name):
    server = "apps-apis.google.com"
    path   = "/a/feeds/{0}/user/2.0/{1}".format(domain, user_name)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsDELETERequest(server, path, header)

    user_entry = data.UserEntry(status, xml_string=response)
    return True

def getAllUsers(domain, auth_token, display_obj=None):
    users_info = {} # {user : user_entry object}

    next_user = "!"
    while next_user != "":
        ( tmp_users_info
        , next_user ) = get100Users(domain, auth_token, next_user, display_obj)
        users_info.update(tmp_users_info)

    return users_info

def get100Users(domain, auth_token, next_user="", display_obj=None):
    users_info      = {} # {user : user_entry object}
    disp_users_info = {}

    server = "apps-apis.google.com"
    path   = "/a/feeds/{0}/user/2.0?startUsername={1}".format(domain, next_user)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsGETRequest(server, path, header)

    # Get user feed
    user_feed = data.UserFeed(status, response)

    # Retrieve user information from xml string
    for user_entry in user_feed.entries:
        user_name   = user_entry.getUserName()
        users_info[user_name] = user_entry

        if display_obj:
            sn        = user_entry.getSn()
            given_name = user_entry.getGivenName()
            active    = user_entry.getActive()
            quota     = user_entry.getQuota()
            disp_users_info[user_name] = { "sn" : sn
                                        , "given_name" : given_name
                                        , "quota"      : quota
                                        , "active"     : active
                                        }
            header = ["user_name", "sn", "given_name", "quota", "active"]
            value  = {"user_name" : user_name}
            value.update(disp_users_info[user_name])
            display_obj.display(*header, **value)

    # Check 100 over?
    next_user = user_feed.getNextLink()
    if "?" in next_user:
        next_user = next_user.split("?")[1].split("=")[1]

    return (users_info, next_user)

def get1User(domain, auth_token, user_name):
    server = "apps-apis.google.com"
    path   = "/a/feeds/{0}/user/2.0/{1}".format(domain, user_name)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsGETRequest(server, path, header)

    # Get entry
    user_entry = data.UserEntry(status, xml_string=response)

    return {user_name : user_entry}

def outputAllUsers(domain, auth_token):
    from GoogleAppsAccountManager import display
    getAllUsers(domain, auth_token, display.Display())
    return True

