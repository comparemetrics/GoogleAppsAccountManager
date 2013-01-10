#
# GoogleAppsAccountManager: multipledomainnickname/client
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-29, since 2012-12-29
#

from GoogleAppsAccountManager import http, errors
from GoogleAppsAccountManager.multipledomainnickname import data

def createAlias( domain
               , auth_token
               , user_email
               , alias_email
               ):
    from GoogleAppsAccountManager import template

    # Get additional domain
    (alias_name, alias_domain) = alias_email.split("@")

    server = "apps-apis.google.com"
    path   = "/a/feeds/alias/2.0/{0}".format(alias_domain)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    body   = template.ALIAS_ENTRY_M.format( alias_name=alias_name
                                          , alias_domain=alias_domain
                                          , user_email=user_email
                                          )

    # HTTP Request
    (response, status) = http.httpsPOSTRequest(server, path, header, body)

    nickname_entry = data.AliasEntry_M(status, xml_string=response)
    return True

def deleteAlias(domain, auth_token, alias_email):
    # Get additional domain
    (_, mail_domain) = alias_email.split("@")

    server = "apps-apis.google.com"
    path   = "/a/feeds/alias/2.0/{0}/{1}".format(mail_domain, alias_email)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsDELETERequest(server, path, header)

    nickname_entry = data.AliasEntry_M(status, xml_string=response)
    return True

def getAllAliasesOfUser(domain, auth_token, user_email, display_obj=None):
    # Get additional domain
    (_, mail_domain) = user_email.split("@")

    aliases_info    = {}
    alias_emails    = []

    server = "apps-apis.google.com"
    path   = "/a/feeds/alias/2.0/{0}?userEmail={1}".format(mail_domain, user_email)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsGETRequest(server, path, header)

    # Get feed
    nickname_feed = data.AliasFeed_M(status, response)

    # Retrieve information from xml string
    for nickname_entry in nickname_feed.entries:
        alias_email                 = nickname_entry.getAliasEmail()
        aliases_info[alias_email]   = nickname_entry

        if display_obj:
            alias_emails += [alias_email]

    if display_obj:
        header = ["user_email", "alias_email1:alias_email2:..."]
        value  = {"user_email" : user_email}
        value.update({"alias_email1:alias_email2:..." : ":".join(alias_emails)})
        display_obj.display(*header, **value)

    return aliases_info

def outputAllAliasesOfUser(domain, auth_token, user_email):
    from GoogleAppsAccountManager import display
    getAllAliasesOfUser(domain, auth_token, user_email, display.Display())
    return True

def getAllAliases(domain, auth_token, display_obj=None):
    aliases_info = {} # {user : nickname_entry object}

    next_alias_email = "!"
    while next_alias_email != "":
        ( tmp_aliases_info
        , next_alias_email ) = get100Aliases(domain, auth_token, next_alias_email, display_obj)
        aliases_info.update(tmp_aliases_info)

    return aliases_info

def get100Aliases(domain, auth_token, next_alias_email="", display_obj=None):
    aliases_info      = {} # {user : nickname_entry object}
    disp_aliases_info = {}

    server = "apps-apis.google.com"
    path   = "/a/feeds/alias/2.0/{0}?start={1}".format(domain, next_alias_email)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsGETRequest(server, path, header)

    # Get user feed
    alias_feed = data.AliasFeed_M(status, response)

    # Retrieve user information from xml string
    for nickname_entry in alias_feed.entries:
        alias_email   = nickname_entry.getAliasEmail()
        aliases_info[alias_email] = nickname_entry

        if display_obj:
            user_email = nickname_entry.getUserEmail()
            disp_aliases_info[alias_email] = { "user_email" : user_email }
            header = ["alias_email", "user_email"]
            value  = {"alias_email" : alias_email}
            value.update(disp_aliases_info[alias_email])
            display_obj.display(*header, **value)

    # Check 100 over?
    next_alias_email = alias_feed.getNextLink()
    if "?" in next_alias_email:
        next_alias_email = next_alias_email.split("?")[1].split("=")[1]

    return (aliases_info, next_alias_email)

def get1Alias(domain, auth_token, alias_email):
    # Get additional domain
    (_, mail_domain) = alias_email.split("@")

    server = "apps-apis.google.com"
    path   = "/a/feeds/alias/2.0/{0}/{1}".format(mail_domain, alias_email)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsGETRequest(server, path, header)

    # Get entry
    nickname_entry = data.AliasEntry_M(status, xml_string=response)

    return {alias_email: nickname_entry}

def outputAllAliases(domain, auth_token):
    from GoogleAppsAccountManager import display
    getAllAliases(domain, auth_token, display.Display())
    return True

