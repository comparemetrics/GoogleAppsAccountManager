#
# GoogleAppsAccountManager: multipledomainuser/client
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

from GoogleAppsAccountManager import http, errors
from GoogleAppsAccountManager.multipledomainuser import data

def createUser( domain
              , auth_token
              , user_email
              , password
              , sn
              , given_name
              , hash_function_name="SHA-1"
              , is_suspended="false"
              , is_admin="false"
              , is_change_password="true"
              ):
    from GoogleAppsAccountManager import template

    # Get additional domain
    (user_name, mail_domain) = user_email.split("@")

    server = "apps-apis.google.com"
    path   = "/a/feeds/user/2.0/{0}".format(mail_domain)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    body   = template.USER_ENTRY_M.format( user_name=user_name
                                         , mail_domain=mail_domain
                                         , password=password
                                         , hash_function_name=hash_function_name
                                         , sn=sn
                                         , given_name=given_name
                                         , is_change_password=is_change_password
                                         , is_suspended=is_suspended
                                         , is_admin=is_admin
                                         )

    # HTTP Request
    (response, status) = http.httpsPOSTRequest(server, path, header, body)

    user_entry = data.UserEntry_M(status, xml_string=response)
    return True

def updateUser( domain
              , auth_token
              , user_email
              , password=None
              , sn=None
              , given_name=None
              , hash_function_name="SHA-1"
              , is_suspended=None
              , is_admin=None
              , is_change_password=None
              ):

    # Get additional domain
    (user_name, mail_domain) = user_email.split("@")

    server = "apps-apis.google.com"
    path   = "/a/feeds/user/2.0/{0}/{1}".format(mail_domain, user_email)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    users_info = get1User(domain, auth_token, user_email)

    body   = ""
    if password is not None:
        body = users_info[user_email].setPassword(password, hash_function_name)

    if sn is not None:
        body = users_info[user_email].setSn(sn)

    if given_name is not None:
        body = users_info[user_email].setGivenName(given_name)

    if is_suspended is not None:
        if (is_suspended.lower() == "true") or (is_suspended.lower() == "false"):
            body = users_info[user_email].setSuspended(is_suspended.lower())
        else:
            raise errors.ArgumentsError(
                    "is_suspended must be \"true\" or \"false\"\n"
                    )

    if is_admin is not None:
        if (is_admin.lower() == "true") or (is_admin.lower() == "false"):
            body = users_info[user_email].setAdmin(is_admin.lower())
        else:
            raise errors.ArgumentsError(
                    "is_admin must be \"true\" or \"false\"\n"
                    )

    if is_change_password is not None:
        if (is_change_password.lower() == "true") or (is_change_password.lower() == "false"):
            body = users_info[user_email].setChangePassword(is_change_password.lower())
        else:
            raise errors.ArgumentsError(
                    "is_change_password must be \"true\" or \"false\"\n"
                    )

    if body == "":
        raise errors.NoParametersError()

    # HTTP Request
    (response, status) = http.httpsPUTRequest(server, path, header, body)

    user_entry = data.UserEntry_M(status, xml_string=response)
    return True

def renameAccount(domain, auth_token, old_user_email, new_user_email):
    # Get additional domain
    (user_name, old_domain) = old_user_email.split("@")

    server = "apps-apis.google.com"
    path   = "/a/feeds/user/userEmail/2.0/{0}/{1}".format(old_domain, old_user_email)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    users_info = get1User(domain, auth_token, old_user_email)

    body = users_info[old_user_email].setNewUserEmail(new_user_email)

    # HTTP Request
    (response, status) = http.httpsPUTRequest(server, path, header, body)

    user_entry = data.UserEntry_M(status, xml_string=response)
    return True

def deleteUser(domain, auth_token, user_email):
    # Get additional domain
    (_, mail_domain) = user_email.split("@")

    server = "apps-apis.google.com"
    path   = "/a/feeds/user/2.0/{0}/{1}".format(mail_domain, user_email)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsDELETERequest(server, path, header)

    user_entry = data.UserEntry_M(status, xml_string=response)
    return True

def getAllUsers(domain, auth_token, display_obj=None):
    users_info = {} # {user : user_entry object}

    next_user_email = "!"
    while next_user_email != "":
        ( tmp_users_info
        , next_user_email ) = get100Users(domain, auth_token, next_user_email, display_obj)
        users_info.update(tmp_users_info)

    return users_info

def get100Users(domain, auth_token, next_user_email="", display_obj=None):
    users_info      = {} # {user : user_entry object}
    disp_users_info = {}

    server = "apps-apis.google.com"
    path   = "/a/feeds/user/2.0/{0}?start={1}".format(domain, next_user_email)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsGETRequest(server, path, header)

    # Get user feed
    user_feed = data.UserFeed_M(status, response)

    # Retrieve user information from xml string
    for user_entry in user_feed.entries:
        user_email   = user_entry.getUserEmail()
        users_info[user_email] = user_entry

        if display_obj:
            sn         = user_entry.getSn()
            given_name = user_entry.getGivenName()
            is_admin   = user_entry.isAdmin()
            is_change  = user_entry.isChangePasswordAtNextLogin()
            is_active  = user_entry.isActive()
            disp_users_info[user_email] = { "sn" : sn
                                          , "given_name"           : given_name
                                          , "is_admin?"            : is_admin
                                          , "is_change_pw_needed?" : is_change
                                          , "is_active?"           : is_active
                                          }
            header = ["user_email", "sn", "given_name", "is_admin?"
                                        , "is_change_pw_needed?", "is_active?"]
            value  = {"user_email" : user_email}
            value.update(disp_users_info[user_email])
            display_obj.display(*header, **value)

    # Check 100 over?
    next_user_email = user_feed.getNextLink()
    if "?" in next_user_email:
        next_user_email = next_user_email.split("?")[1].split("=")[1]

    return (users_info, next_user_email)

def get1User(domain, auth_token, user_email):
    # Get additional domain
    (_, mail_domain) = user_email.split("@")

    server = "apps-apis.google.com"
    path   = "/a/feeds/user/2.0/{0}/{1}".format(mail_domain, user_email)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsGETRequest(server, path, header)

    # Get entry
    user_entry = data.UserEntry_M(status, xml_string=response)

    return {user_email: user_entry}

def outputAllUsers(domain, auth_token):
    from GoogleAppsAccountManager import display
    getAllUsers(domain, auth_token, display.Display())
    return True

