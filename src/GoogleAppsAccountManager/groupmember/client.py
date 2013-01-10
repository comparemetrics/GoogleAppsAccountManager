#
# GoogleAppsAccountManager: groupmember/client
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

from GoogleAppsAccountManager import http, errors
from GoogleAppsAccountManager.groupmember import data

def getAllMembersOfGroup(domain, auth_token, group_id, display_obj=None):
    group_members_info      = {}
    members                 = []

    server = "apps-apis.google.com"
    path   = "/a/feeds/group/2.0/{0}/{1}/member".format(domain, group_id)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsGETRequest(server, path, header)

    # Get group feed
    group_member_feed = data.GroupMemberFeed(status, response)

    # Retrieve group information from xml string
    for group_member_entry in group_member_feed.entries:
        membername = group_member_entry.getMemberId().split("@")[0]
        group_members_info[membername] = group_member_entry

        if display_obj:
            members += [membername]

    if display_obj:
        header = ["group_id", "membername1:membername2:.."]
        value  = {"group_id" : group_id}
        value.update({"membername1:membername2:.." : ":".join(members)})
        display_obj.display(*header, **value)

    return group_members_info

def outputAllMembersOfGroup(domain, auth_token, group_id):
    from GoogleAppsAccountManager import display
    getAllMembersOfGroup(domain, auth_token, group_id, display.Display())
    return True

def addMemberToGroup(domain, auth_token, membername, group_id):
    from GoogleAppsAccountManager import template
    server = "apps-apis.google.com"
    path   = "/a/feeds/group/2.0/{0}/{1}/member".format(domain, group_id)
    header = { "Content-type"   : "application/atom+xml"
             , "Authorization"  : "GoogleLogin auth={0}".format(auth_token)
             }
    body   = template.GROUP_MEMBER_ENTRY.format( domain=domain
                                               , group_id=group_id
                                               , membername=membername
                                               )

    # HTTP Request
    (response, status) = http.httpsPOSTRequest(server, path, header, body)

    # Get group feed
    group_member_entry = data.GroupMemberEntry(status, xml_string=response)
    return True

def deleteMemberFromGroup(domain, auth_token, membername, group_id):
    server = "apps-apis.google.com"
    path   = ( "/a/feeds/group/2.0/{0}/{1}/member/{2}"
               .format(domain, group_id, membername)
             )
    header = { "Content-type"   : "application/atom+xml"
             , "Authorization"  : "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsDELETERequest(server, path, header)

    group_member_entry = data.GroupMemberEntry(status, xml_string=response)
    return True

