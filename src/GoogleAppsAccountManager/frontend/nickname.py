# -*- coding: utf-8 -*-
#
# GoogleAppsAccountManager: frontend/nickname
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

# NICKNAME HELP
NICKNAME_HELP = """Usage: gapps-tool nickname <subcommand> 

Available subcommands:
  create          - Create nickname
  delete          - Delete nickname
  list            - List all nicknames
  listnicknamesof - List all nicknames of user

"""

# Subcommand list
__subcommand__ = { "create"          : "_create"
                 , "delete"          : "_delete"
                 , "list"            : "_list"
                 , "listnicknamesof" : "_listnicknamesof"
                 , "create_f"        : "_create_f"
                 , "delete_f"        : "_delete_f"
                 }

import sys
from GoogleAppsAccountManager.nickname import client as NICKNAME
from GoogleAppsAccountManager.frontend import _func, _messages

def run(options, parser, my_name):
    from GoogleAppsAccountManager.frontend import _runSubcommand
    _runSubcommand(options, parser, my_name, __subcommand__, NICKNAME_HELP)

def _create(options, parser):
    # Set parser options
    parser.add_argument( "user_name"
                       , action = "store"
                       , help   = "User name."
                       )
    parser.add_argument( "nickname"
                       , action = "store"
                       , help   = "Nickname."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    return _func.operate( NICKNAME.createNickname
                        , namespace.nickname.lower()
                        , parser.prog
                        , namespace.result_file
                               , namespace.domain
                               , auth_token
                               , namespace.user_name.lower()    # user
                               , namespace.nickname.lower()     # nickname
                        )

def _delete(options, parser):
    # Set parser options 
    parser.add_argument( "nickname"
                       , action = "store"
                       , help   = "Nickname."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    return _func.operate( NICKNAME.deleteNickname
                        , namespace.nickname.lower()
                        , parser.prog
                        , namespace.result_file
                               , namespace.domain
                               , auth_token
                               , namespace.nickname.lower()    # nickname
                        )

def _list(options, parser):
    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    NICKNAME.outputAllNicknames(namespace.domain, auth_token)

    return True

def _listnicknamesof(options, parser):
    # Set parser options
    parser.add_argument( "user_name"
                       , action = "store"
                       , help   = "User name."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    NICKNAME.outputAllNicknamesOfUser(namespace.domain, auth_token, namespace.user_name.lower())

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
        must_keys = ["user_name", "nickname"]
        if not _func.checkValidHeader(header, *must_keys):
            return False
        f.seek(0, 0)

        # Read csv
        for record in reader:
            must_values = ["user_name", "nickname"]
            if not _func.checkRecordHasValue(record, *must_values):
                continue

            # Operation
            _func.operate( NICKNAME.createNickname
                         , record["nickname"].lower()
                         , parser.prog
                         , namespace.result_file
                                , namespace.domain
                                , auth_token
                                , record["user_name"].lower()  # user
                                , record["nickname"]           # nickname
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
        must_keys = ["nickname"]
        if not _func.checkValidHeader(header, *must_keys):
            return False
        f.seek(0, 0)

        # Read csv
        for record in reader:
            must_values = ["nickname"]
            if not _func.checkRecordHasValue(*must_values):
                continue

            # Operation
            _func.operate( NICKNAME.deleteNickname
                         , record["nickname"].lower()
                         , parser.prog
                         , namespace.result_file
                                , namespace.domain
                                , auth_token
                                , record["nickname"].lower()  # nickname
                         )

        return True

