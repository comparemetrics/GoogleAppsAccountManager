#
# GoogleAppsAccountManager: group/client
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

from GoogleAppsAccountManager import http, errors
from GoogleAppsAccountManager.group import data

def createGroup( domain
               , auth_token
               , group_id
               , groupname=None
               , description=""
               ):
    from GoogleAppsAccountManager import template

    server = "apps-apis.google.com"
    path   = "/a/feeds/group/2.0/{0}".format(domain)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }
    if groupname is None:
        groupname = group_id
    body   = template.GROUP_ENTRY.format( group_id=group_id
                                        , groupname=groupname
                                        , description=description
                                        , domain=domain
                                        )

    # HTTP Request
    (response, status) = http.httpsPOSTRequest(server, path, header, body)

    group_entry = data.GroupEntry(status, xml_string=response)
    return True

def updateGroup( domain
               , auth_token
               , group_id
               , groupname=None
               , description=None
               ):
    server = "apps-apis.google.com"
    path   = "/a/feeds/group/2.0/{0}/{1}".format(domain, group_id)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    groups_info = get1Group(domain, auth_token, group_id)
    body = ""
    if groupname is not None:
        body = groups_info[group_id].setGroupName(groupname)

    if description is not None:
        body = groups_info[group_id].setGroupDescription(description)

    if body == "":
        raise errors.NoParametersError()

    # HTTP Request
    (response, status) = http.httpsPUTRequest(server, path, header, body)

    group_entry = data.GroupEntry(status, xml_string=response)
    return True

def deleteGroup(domain, auth_token, group_id):
    server = "apps-apis.google.com"
    path   = "/a/feeds/group/2.0/{0}/{1}".format(domain, group_id)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsDELETERequest(server, path, header)

    group_entry = data.GroupEntry(status, xml_string=response)
    return True

def getAllGroupsInDomain(domain, auth_token, display_obj=None):
    disp_groups_info = {}
    groups_info      = {}

    server = "apps-apis.google.com"
    path   = "/a/feeds/group/2.0/{0}?start=".format(domain)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsGETRequest(server, path, header)

    # Get group feed
    group_feed = data.GroupFeed(status, response)

    # Retrieve group information from xml string
    for group_entry in group_feed.entries:
        group_id = group_entry.getGroupId().split("@")[0]
        groups_info[group_id] = group_entry

        if display_obj:
            description = group_entry.getGroupDescription()
            groupname   = group_entry.getGroupName()
            disp_groups_info[group_id] = { "description" : description
                                         , "groupname"   : groupname
                                         }
            header = ["group_id", "groupname", "description"]
            value  = {"group_id" : group_id}
            value.update(disp_groups_info[group_id])
            display_obj.display(*header, **value)

    return True

def outputAllGroupsInDomain(domain, auth_token):
    from GoogleAppsAccountManager import display
    getAllGroupsInDomain(domain, auth_token, display.Display())
    return True

def getAllGroupsOfMember(domain, auth_token, membername, display_obj=None):
    member_groups_info      = {}
    groups                  = []

    server = "apps-apis.google.com"
    path   = ( "/a/feeds/group/2.0/{0}?member={1}&directOnly=false"
               .format(domain, membername)
             )
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsGETRequest(server, path, header)

    # Get group feed
    group_feed = data.GroupFeed(status, response)

    # Retrieve group information from xml string
    for group_entry in group_feed.entries:
        member_groups_info[membername] = group_entry

        if display_obj:
            group_id = group_entry.getGroupId().split("@")[0]
            groups += [group_id]

    if display_obj:
        header = ["membername", "group1:group2:.."]
        value  = {"membername" : membername}
        value.update({ "group1:group2:.." : ":".join(groups)})
        display_obj.display(*header, **value)

    return member_groups_info

def outputAllGroupsOfMember(domain, auth_token, membername):
    from GoogleAppsAccountManager import display
    getAllGroupsOfMember(domain, auth_token, membername, display.Display())
    return True

def get1Group(domain, auth_token, group_id):
    server = "apps-apis.google.com"
    path   = "/a/feeds/group/2.0/{0}/{1}".format(domain, group_id)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsGETRequest(server, path, header)

    # Get group entry
    group_entry = data.GroupEntry(status, xml_string=response)
    group_id   = group_entry.getGroupId().split("@")[0]

    return {group_id : group_entry}

