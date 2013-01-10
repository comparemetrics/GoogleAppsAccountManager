# -*- coding: utf-8 -*-
#
# GoogleAppsAccountManager: frontend/group
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

# GROUP HELP
GROUP_HELP = """Usage: gapps-tool group <subcommand>

Available subcommands:
  create          - Create group
  modify          - Modify group
  delete          - Delete group
  addmember       - Add member to group
  deletemember    - Delete member from group
  assignowner     - Assign owner to group
  demoteowner     - Demote user from group's owner to member
  list            - List all groups
  listgroupsof    - List groups of the user
  listmembersof   - List members of the group
  listownersof    - List owners of the group

"""

# Subcommand list
__subcommand__ = { "create"         : "_create"
                 , "modify"         : "_modify"
                 , "delete"         : "_delete"
                 , "addmember"      : "_addmember"
                 , "deletemember"   : "_deletemember"
                 , "assignowner"    : "_assignowner"
                 , "demoteowner"    : "_demoteowner"
                 , "list"           : "_list"
                 , "listgroupsof"   : "_listgroupsof"
                 , "listmembersof"  : "_listmembersof"
                 , "listownersof"   : "_listownersof"
                 , "create_f"       : "_create_f"
                 , "modify_f"       : "_modify_f"
                 , "delete_f"       : "_delete_f"
                 , "addmember_f"    : "_addmember_f"
                 , "deletemember_f" : "_deletemember_f"
                 }

import sys
from GoogleAppsAccountManager.group import client as GROUP
from GoogleAppsAccountManager.groupmember import client as GROUP_M
from GoogleAppsAccountManager.groupowner import client as GROUP_O
from GoogleAppsAccountManager.frontend import _func, _messages

def run(options, parser, my_name):
    from GoogleAppsAccountManager.frontend import _runSubcommand
    _runSubcommand(options, parser, my_name, __subcommand__, GROUP_HELP)

def _create(options, parser):
    # Set parser options 
    parser.add_argument( "group_id"
                       , action = "store"
                       , help   = "Group id (not group name)."
                       )
    parser.add_argument( "-n", "--group-name"
                       , action  = "store"
                       , help    = "Group name. This is UTF-8 encoded string."
                       )
    parser.add_argument( "-d", "--description"
                       , action  = "store"
                       , default = ""
                       , help    = "Specify group description."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    return _func.operate( GROUP.createGroup
                        , namespace.group_id.lower()
                        , parser.prog
                        , namespace.result_file
                               , namespace.domain
                               , auth_token
                               , namespace.group_id.lower()  # group id
                               , namespace.group_name        # group name
                               , namespace.description       # group description
                        )

def _modify(options, parser):
    # Set parser options 
    parser.add_argument( "group_id"
                       , action = "store"
                       , help   = "Group id (not group name)."
                       )
    parser.add_argument( "-n", "--group-name"
                       , action  = "store"
                       , default = None
                       , help    = "Group name. This is UTF-8 encoded string."
                       )
    parser.add_argument( "-d", "--description"
                       , action  = "store"
                       , default = None
                       , help    = "Specify group description."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    return _func.operate( GROUP.updateGroup
                        , namespace.group_id.lower()
                        , parser.prog
                        , namespace.result_file
                               , namespace.domain
                               , auth_token
                               , namespace.group_id.lower()  # group id
                               , namespace.group_name        # group name
                               , namespace.description       # group description
                        )

def _delete(options, parser):
    # Set parser options 
    parser.add_argument( "group_id"
                       , action = "store"
                       , help   = "Group id (not group name)."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    return _func.operate( GROUP.deleteGroup
                        , namespace.group_id.lower()
                        , parser.prog
                        , namespace.result_file
                               , namespace.domain
                               , auth_token
                               , namespace.group_id.lower()  # group id
                        )

def _addmember(options, parser):
    # Set parser options 
    parser.add_argument( "member_name"
                       , action = "store"
                       , help   = "Member name."
                       )
    parser.add_argument( "group_id"
                       , action = "store"
                       , help   = "Group id (not group name)."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    return _func.operate( GROUP_M.addMemberToGroup
                        , namespace.group_id.lower()
                        , "{} \"{}\"".format( parser.prog
                                            , namespace.member_name.lower()
                                            )
                        , namespace.result_file
                               , namespace.domain
                               , auth_token
                               , namespace.member_name.lower()  # member name
                               , namespace.group_id.lower()     # group id
                        )

def _deletemember(options, parser):
    # Set parser options 
    parser.add_argument( "member_name"
                       , action = "store"
                       , help   = "Member name."
                       )
    parser.add_argument( "group_id"
                       , action = "store"
                       , help   = "Group id (not group name)."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    group_owners_info = GROUP_O.getAllOwnersOfGroup(
                                        namespace.domain
                                      , auth_token
                                      , namespace.group_id.lower()
                                      )

    if group_owners_info.has_key(namespace.member_name.lower()):
        _func.operate( GROUP_O.deleteOwnerFromGroup
                     , namespace.group_id.lower()
                     , "{} \"{}\"".format( "demote"
                                         , namespace.member_name.lower()
                                         )
                     , namespace.result_file
                            , namespace.domain
                            , auth_token
                            , namespace.member_name.lower()  # member name
                            , namespace.group_id.lower()     # group id
                     )

    return _func.operate( GROUP_M.deleteMemberFromGroup
                        , namespace.group_id.lower()
                        , "{} \"{}\"".format( parser.prog
                                            , namespace.member_name.lower()
                                            )
                        , namespace.result_file
                               , namespace.domain
                               , auth_token
                               , namespace.member_name.lower()  # member name
                               , namespace.group_id.lower()     # group id
                        )

def _assignowner(options, parser):
    # Set parser options 
    parser.add_argument( "member_name"
                       , action = "store"
                       , help   = "Member name."
                       )
    parser.add_argument( "group_id"
                       , action = "store"
                       , help   = "Group id (not group name)."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    group_members_info = GROUP_M.getAllMembersOfGroup(
                                        namespace.domain
                                      , auth_token
                                      , namespace.group_id.lower()
                                      )

    if not group_members_info.has_key(namespace.member_name.lower()):
        add_result = _func.operate( GROUP_M.addMemberToGroup
                          , namespace.group_id.lower()
                          , "{} \"{}\"".format( "addmember"
                                              , namespace.member_name.lower()
                                              )
                          , namespace.result_file
                                 , namespace.domain
                                 , auth_token
                                 , namespace.member_name.lower()  # member name
                                 , namespace.group_id.lower()     # group id
                          )
        if not add_result:
            sys.stderr.write(_messages.GROUP_ASSIGNED_OWNER)
            return False

    return _func.operate( GROUP_O.assignOwnerToGroup
                        , namespace.group_id.lower()
                        , "{} \"{}\"".format( parser.prog
                                            , namespace.member_name.lower()
                                            )
                        , namespace.result_file
                               , namespace.domain
                               , auth_token
                               , namespace.member_name.lower()  # member name
                               , namespace.group_id.lower()     # group id
                        )

def _demoteowner(options, parser):
    # Set parser options 
    parser.add_argument( "member_name"
                       , action = "store"
                       , help   = "Member name."
                       )
    parser.add_argument( "group_id"
                       , action = "store"
                       , help   = "Group id (not group name)."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    return _func.operate( GROUP_O.deleteOwnerFromGroup
                        , namespace.group_id.lower()
                        , "{} \"{}\"".format( parser.prog
                                            , namespace.member_name.lower()
                                            )
                        , namespace.result_file
                               , namespace.domain
                               , auth_token
                               , namespace.member_name.lower()  # member name
                               , namespace.group_id.lower()     # group id
                        )

def _list(options, parser):
    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    GROUP.outputAllGroupsInDomain(namespace.domain, auth_token)

    return True

def _listgroupsof(options, parser):
    # Set parser options 
    parser.add_argument( "member_name"
                       , action = "store"
                       , help   = "Member name."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    GROUP.outputAllGroupsOfMember(namespace.domain, auth_token, namespace.member_name.lower())

    return True

def _listmembersof(options, parser):
    # Set parser options 
    parser.add_argument( "group_id"
                       , action = "store"
                       , help   = "Group name."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    GROUP_M.outputAllMembersOfGroup(namespace.domain, auth_token, namespace.group_id.lower())

    return True

def _listownersof(options, parser):
    # Set parser options 
    parser.add_argument( "group_id"
                       , action = "store"
                       , help   = "Group name."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    GROUP_O.outputAllOwnersOfGroup(namespace.domain, auth_token, namespace.group_id.lower())

    return True

############################# CSV operation #############################

def _create_f(options, parser):
    import csv

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Get records from csv file
    with open(namespace.csv_file) as f:
        reader = csv.DictReader(f)

        # Check header
        header = f.next().replace("\n", "").split(",")
        must_keys = ["group_id", "group_name", "description"]
        if not _func.checkValidHeader(header, *must_keys):
            return False
        f.seek(0, 0)

        # Read csv
        for record in reader:
            must_values = ["group_id"]
            if not _func.checkRecordHasValue(record, *must_values):
                continue

            # Operation
            _func.operate( GROUP.createGroup
                         , record["group_id"].lower()
                         , parser.prog
                         , namespace.result_file
                                , namespace.domain
                                , auth_token
                                , record["group_id"].lower()     # group id
                                , record["group_name"]           # group name
                                , record["description"]          # description
                         )
        return True

def _modify_f(options, parser):
    import csv

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Get records from csv file
    with open(namespace.csv_file) as f:
        reader = csv.DictReader(f)

        # Check header
        header = f.next().replace("\n", "").split(",")
        must_keys = ["group_id", "group_name", "description"]
        if not _func.checkValidHeader(header, *must_keys):
            return False
        f.seek(0, 0)

        # Read csv
        for record in reader:
            must_values = ["group_id"]
            if not _func.checkRecordHasValue(record, *must_values):
                continue

            # Operation
            _func.operate( GROUP.updateGroup
                , record["group_id"].lower()
                , parser.prog
                , namespace.result_file
                    , namespace.domain
                    , auth_token
                    , record["group_id"].lower()                     # group id
                    , _func.replaceSpace2None(record["group_name"])  # group name
                    , _func.replaceSpace2None(record["description"]) # description
                )
        return True

def _delete_f(options, parser):
    import csv

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Get records from csv file
    with open(namespace.csv_file) as f:
        reader = csv.DictReader(f)

        # Check header
        header = f.next().replace("\n", "").split(",")
        must_keys = ["group_id"]
        if not _func.checkValidHeader(header, *must_keys):
            return False
        f.seek(0, 0)

        # Read csv
        for record in reader:
            must_values = ["group_id"]
            if not _func.checkRecordHasValue(record, *must_values):
                continue

            # Operation
            _func.operate( GROUP.deleteGroup
                , record["group_id"].lower()
                , parser.prog
                , namespace.result_file
                    , namespace.domain
                    , auth_token
                    , record["group_id"].lower()                    # group id
                )
        return True

def _addmember_f(options, parser):
    import csv

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Get records from csv file
    with open(namespace.csv_file) as f:
        reader = csv.DictReader(f)

        # Check header
        header = f.next().replace("\n", "").split(",")
        must_keys = ["member_name", "group_id"]
        if not _func.checkValidHeader(header, *must_keys):
            return False
        f.seek(0, 0)

        # Read csv
        for record in reader:
            must_values = ["member_name", "group_id"]
            if not _func.checkRecordHasValue(record, *must_values):
                continue

            # Operation
            _func.operate( GROUP_M.addMemberToGroup
                        , record["group_id"].lower()
                        , "{} \"{}\"".format( parser.prog
                                            , record["member_name"].lower()
                                            )
                        , namespace.result_file
                        , namespace.domain
                        , auth_token
                        , record["member_name"].lower()        # member name
                        , record["group_id"].lower()           # group id
                    )
        return True

def _deletemember_f(options, parser):
    import csv

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Get records from csv file
    with open(namespace.csv_file) as f:
        reader = csv.DictReader(f)

        # Check header
        header = f.next().replace("\n", "").split(",")
        must_keys = ["member_name", "group_id"]
        if not _func.checkValidHeader(header, *must_keys):
            return False
        f.seek(0, 0)

        # Read csv
        for record in reader:
            must_values = ["member_name", "group_id"]
            if not _func.checkRecordHasValue(record, *must_values):
                continue

            # Operation
            _func.operate( GROUP_M.deleteMemberFromGroup
                        , record["group_id"].lower()
                        , "{} \"{}\"".format( parser.prog
                                            , record["member_name"].lower()
                                            )
                        , namespace.result_file
                        , namespace.domain
                        , auth_token
                        , record["member_name"].lower()        # member name
                        , record["group_id"].lower()           # group id
                    )
        return True

