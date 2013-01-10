#
# GoogleAppsAccountManager: nickname/client
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

from GoogleAppsAccountManager import http, errors
from GoogleAppsAccountManager.nickname import data

def createNickname( domain
                  , auth_token
                  , user_name
                  , nickname
                  ):
    from GoogleAppsAccountManager import template

    server = "apps-apis.google.com"
    path   = "/a/feeds/{0}/nickname/2.0".format(domain)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    body   = template.NICKNAME_ENTRY.format( user_name=user_name
                                           , nickname=nickname
                                           , domain=domain
                                           )

    # HTTP Request
    (response, status) = http.httpsPOSTRequest(server, path, header, body)

    nickname_entry = data.NicknameEntry(status, xml_string=response)
    return True

def deleteNickname(domain, auth_token, nickname):
    server = "apps-apis.google.com"
    path   = "/a/feeds/{0}/nickname/2.0/{1}".format(domain, nickname)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsDELETERequest(server, path, header)

    nickname_entry = data.NicknameEntry(status, xml_string=response)
    return True

def getAllNicknamesOfUser(domain, auth_token, user_name, display_obj=None):
    nicknames_info    = {}
    nicknames         = []

    server = "apps-apis.google.com"
    path   = "/a/feeds/{0}/nickname/2.0?username={1}".format(domain, user_name)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsGETRequest(server, path, header)

    # Get feed
    nickname_feed = data.NicknameFeed(status, response)

    # Retrieve information from xml string
    for nickname_entry in nickname_feed.entries:
        nickname                 = nickname_entry.getNickname()
        nicknames_info[nickname] = nickname_entry

        if display_obj:
            nicknames += [nickname]

    if display_obj:
        header = ["user_name", "nickname1:nickname2:..."]
        value  = {"user_name" : user_name}
        value.update({"nickname1:nickname2:..." : ":".join(nicknames)})
        display_obj.display(*header, **value)

    return nicknames_info

def outputAllNicknamesOfUser(domain, auth_token, user_name):
    from GoogleAppsAccountManager import display
    getAllNicknamesOfUser(domain, auth_token, user_name, display.Display())
    return True

def getAllNicknames(domain, auth_token, display_obj=None):
    nicknames_info = {} # {nickname : nickname_entry object}

    next_nickname = "!"
    while next_nickname != "":
        (tmp_nicknames_info, next_nickname) = get100Nicknames( domain
                                                             , auth_token
                                                             , next_nickname
                                                             , display_obj
                                                             )
        nicknames_info.update(tmp_nicknames_info)

    return nicknames_info

def get100Nicknames(domain, auth_token, next_nickname="", display_obj=None):
    nicknames_info      = {} # {nickname : nickname_entry object}
    disp_nicknames_info = {}

    server = "apps-apis.google.com"
    path   = "/a/feeds/{0}/nickname/2.0?startnickname={1}".format(domain, next_nickname) #FIXME
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsGETRequest(server, path, header)

    # Get feed
    nickname_feed = data.NicknameFeed(status, response)

    # Retrieve information from xml string
    for nickname_entry in nickname_feed.entries:
        nickname                 = nickname_entry.getNickname()
        nicknames_info[nickname] = nickname_entry

        if display_obj:
            user_name    = nickname_entry.getUserName()
            disp_nicknames_info[nickname] = { "user_name" : user_name }
            header = ["nickname", "user_name"]
            value  = {"nickname" : nickname}
            value.update(disp_nicknames_info[nickname])
            display_obj.display(*header, **value)

    # Check 100 over?
    next_nickname = nickname_feed.getNextLink()
    if "?" in next_nickname:
        next_nickname = next_nickname.split("?")[1].split("=")[1]

    return (nicknames_info, next_nickname)

def get1Nickname(domain, auth_token, nickname):
    server = "apps-apis.google.com"
    path   = "/a/feeds/{0}/nickname/2.0/{1}".format(domain, nickname)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsGETRequest(server, path, header)

    # Get entry
    nickname_entry = data.NicknameEntry(status, xml_string=response)

    return {nickname : nickname_entry}

def outputAllNicknames(domain, auth_token):
    from GoogleAppsAccountManager import display
    getAllNicknames(domain, auth_token, display.Display())
    return True

