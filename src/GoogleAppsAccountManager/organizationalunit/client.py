#
# GoogleAppsAccountManager: organizationalunit/client
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

import urllib
from GoogleAppsAccountManager import http, errors
from GoogleAppsAccountManager.organizationalunit import data

def getCustomerId(auth_token):
    server = "apps-apis.google.com"
    path   = "/a/feeds/customer/2.0/customerId"
    header = { "Content-type" : "application/atom+xml"
              , "Authorization": "GoogleLogin auth={0}".format(auth_token)
              }

    # HTTP Request
    (response, status) = http.httpsGETRequest(server, path, header)

    customer_id_entry = data.CustomerIdEntry(status, xml_string=response)
    return customer_id_entry.getCustomerId()

def createOu( auth_token
            , customer_id
            , ou_path               # "/ou1/ou1-1/" <-- prefix "/" is needed
            , description=""
            , blockInheritance="false"
            ):
    from GoogleAppsAccountManager import template

    server = "apps-apis.google.com"
    path   = "/a/feeds/orgunit/2.0/{0}".format(customer_id)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    ou_path_rel    = ou_path[1:]
    ou_basename    = ou_path_rel.split("/")[-1]
    ou_parent_path = "/".join(ou_path_rel.split("/")[:-1])
    if ou_parent_path == "":
        ou_parent_path = "/"

    body = template.OU_ENTRY.format(
              customer_id          = customer_id 
            , ou_name              = ou_basename
            , ou_name_quote        = urllib.quote(ou_basename)
            , ou_parent_path_quote = urllib.quote(ou_parent_path)
            , description          = description
            , blockInheritance     = blockInheritance
            )

    # HTTP Request
    (response, status) = http.httpsPOSTRequest(server, path, header, body)

    ou_entry = data.OuEntry(status, xml_string=response)
    return True

def updateOu( auth_token
            , customer_id
            , ou_path
            , description=None
            , blockInheritance=None # true or false
            ):
    ou_path_rel = urllib.quote(ou_path[1:])
    if ou_path_rel == "":
        ou_path_rel = "/"

    server = "apps-apis.google.com"
    path   = "/a/feeds/orgunit/2.0/{0}/{1}".format(customer_id, ou_path_rel)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    ou_info = get1Ou(auth_token, customer_id, ou_path)
    body = ""
    if description is not None:
        body = ou_info[ou_path].setOuDescription(description)

    if blockInheritance is not None:
        if (blockInheritance.lower() == "true" or
                blockInheritance.lower() == "false"):
            body = ou_info[ou_path].setOuBlockInheritance(blockInheritance)
        else:
            raise errors.ArgumentsError(
                    "blockInheritance must be \"true\" or \"false\"\n")

    if body == "":
        raise errors.NoParametersError()

    # HTTP Request
    (response, status) = http.httpsPUTRequest(server, path, header, body)

    ou_entry = data.OuEntry(status, xml_string=response)
    return True

def deleteOu(auth_token, customer_id, ou_path):
    ou_path_rel = urllib.quote(ou_path[1:])
    if ou_path_rel == "":
        raise errors.ArgumentsError("Cannot delete root ou\n")

    server = "apps-apis.google.com"
    path   = "/a/feeds/orgunit/2.0/{0}/{1}".format(customer_id, ou_path_rel)
    header = { "Content-type" : "application/atom+xml"
              , "Authorization": "GoogleLogin auth={0}".format(auth_token)
              }

    # HTTP Request
    (response, status) = http.httpsDELETERequest(server, path, header)

    ou_entry = data.OuEntry(status, xml_string=response)
    return True

def getAllOusInDomain(auth_token, customer_id, display_obj=None):
    ou_info     = {}

    body      = ""
    header = { "Content-type" : "application/atom+xml"
              , "Authorization": "GoogleLogin auth={0}".format(auth_token)
              }

    next_link = None
    while next_link != "!!END!!":
        (tmp_ou_info, next_link) = get100Ous(auth_token, customer_id, next_link, display_obj)
        ou_info.update(tmp_ou_info)

    return ou_info

def get100Ous(auth_token, customer_id, next_link=None, display_obj=None):
    disp_ous_info = {}
    ou_info       = {}

    server = "apps-apis.google.com"
    path   = "/a/feeds/orgunit/2.0/{0}?get=all".format(customer_id)
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
    ou_feed = data.OuFeed(status, response)

    # Retrieve organizational unit information from xml string
    for ou_entry in ou_feed.entries:
        ou_path          = ou_entry.getOuPath()
        ou_info[ou_path] = ou_entry

        if display_obj:
            description = ou_entry.getOuDescription()
            disp_ous_info[ou_path] = {"description" : description}
            header = ["ou_path", "description"]
            value  = {"ou_path" : ou_path}
            value.update(disp_ous_info[ou_path])
            display_obj.display(*header, **value)

    # Check 100 over?
    next_link = ou_feed.getNextLink()

    return (ou_info, next_link)

def outputAllOusInDomain(auth_token, customer_id):
    from GoogleAppsAccountManager import display
    getAllOusInDomain(auth_token, customer_id, display.Display())
    return True

def get1Ou(auth_token, customer_id, ou_path):
    ou_path_rel = urllib.quote(ou_path[1:])
    if ou_path_rel == "":
        ou_path_rel = "/"

    server = "apps-apis.google.com"
    path   = "/a/feeds/orgunit/2.0/{0}/{1}".format(customer_id, ou_path_rel)
    header = { "Content-type" : "application/atom+xml"
             , "Authorization": "GoogleLogin auth={0}".format(auth_token)
             }

    # HTTP Request
    (response, status) = http.httpsGETRequest(server, path, header)

    # Get organizational unit entry
    ou_entry = data.OuEntry(status, xml_string=response)

    return {ou_path: ou_entry}

