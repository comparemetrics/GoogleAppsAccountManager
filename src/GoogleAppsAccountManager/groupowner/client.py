#
# GoogleAppsAccountManager: groupowner/client
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

from GoogleAppsAccountManager import http, errors
from GoogleAppsAccountManager.groupowner import data

def getAllOwnersOfGroup(domain, auth_token, group_id, display_obj=None):
    group_owners_info      = {}
    owners                 = []

    #FIXME: if more than 200 entries, start key is needed
    server = "apps-apis.google.com"
    path   = "/a/feeds/group/2.0/{0}/{1}/owner".format(domain, group_id)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsGETRequest(server, path, header)

    # Get group feed
    group_owner_feed = data.GroupOwnerFeed(status, response)

    # Retrieve group information from xml string
    for group_owner_entry in group_owner_feed.entries:
        owner_name = group_owner_entry.getOwnerEmail().split("@")[0]
        group_owners_info[owner_name] = group_owner_entry

        if display_obj:
            owners += [owner_name]

    if display_obj:
        header = ["group_id", "owner_name1:owner_name2:.."]
        value  = {"group_id" : group_id}
        value.update({"owner_name1:owner_name2:.." : ":".join(owners)})
        display_obj.display(*header, **value)

    return group_owners_info

def outputAllOwnersOfGroup(domain, auth_token, group_id):
    from GoogleAppsAccountManager import display
    getAllOwnersOfGroup(domain, auth_token, group_id, display.Display())
    return True

def get1OwnerOfGroup(domain, auth_token, user_name, group_id):
    server = "apps-apis.google.com"
    path   = "/a/feeds/group/2.0/{0}/{1}/owner/{2}".format(domain, group_id, user_name)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsGETRequest(server, path, header)

    # Get group entry
    group_owner_entry = data.GroupOwnerEntry(status, xml_string=response)
    owner_name   = group_owner_entry.getOwnerEmail().split("@")[0]

    return {owner_name : group_owner_entry}

def assignOwnerToGroup(domain, auth_token, owner_name, group_id):
    from GoogleAppsAccountManager import template
    server = "apps-apis.google.com"
    path   = "/a/feeds/group/2.0/{0}/{1}/owner".format(domain, group_id)
    header = { "Content-type"   : "application/atom+xml"
             , "Authorization"  : "GoogleLogin auth={0}".format(auth_token)
             }
    body   = template.GROUP_OWNER_ENTRY.format( domain=domain
                                              , group_id=group_id
                                              , owner_name=owner_name
                                              )

    # HTTP Request
    (response, status) = http.httpsPOSTRequest(server, path, header, body)

    # Get group feed
    group_owner_entry = data.GroupOwnerEntry(status, xml_string=response)
    return True

def deleteOwnerFromGroup(domain, auth_token, owner_name, group_id):
    server = "apps-apis.google.com"
    path   = ( "/a/feeds/group/2.0/{0}/{1}/owner/{2}"
               .format(domain, group_id, owner_name)
             )
    header = { "Content-type"   : "application/atom+xml"
             , "Authorization"  : "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsDELETERequest(server, path, header)

    group_owner_entry = data.GroupOwnerEntry(status, xml_string=response)
    return True

