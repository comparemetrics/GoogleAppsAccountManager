# -*- coding: utf-8 -*-
#
# GoogleAppsAccountManager: frontend/nickname2
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2013-01-16, since 2013-01-16
#

# NICKNAME2 HELP
NICKNAME_HELP2 = """Usage: gapps-tool nickname2 <subcommand> 

Available subcommands:
  create          - Create nickname_email
  delete          - Delete nickname_email
  list            - List all nickname_emails
  listnicknamesof - List all nickname_emails of user_email

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
from GoogleAppsAccountManager.multipledomainnickname import client as NICKNAME2
from GoogleAppsAccountManager.frontend import _func, _messages

def run(options, parser, my_name):
    from GoogleAppsAccountManager.frontend import _runSubcommand
    _runSubcommand(options, parser, my_name, __subcommand__, NICKNAME_HELP2)

def _create(options, parser):
    # Set parser options
    parser.add_argument( "user_email"
                       , action = "store"
                       , help   = "User name."
                       )
    parser.add_argument( "nickname_email"
                       , action = "store"
                       , help   = "Nickname."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    return _func.operate( NICKNAME2.createAlias
                        , namespace.nickname_email.lower()
                        , parser.prog
                        , namespace.result_file
                               , namespace.domain
                               , auth_token
                               , namespace.user_email.lower()     # user_email
                               , namespace.nickname_email.lower() # nickname_email
                        )

def _delete(options, parser):
    # Set parser options 
    parser.add_argument( "nickname_email"
                       , action = "store"
                       , help   = "Nickname."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    return _func.operate( NICKNAME2.deleteAlias
                        , namespace.nickname_email.lower()
                        , parser.prog
                        , namespace.result_file
                               , namespace.domain
                               , auth_token
                               , namespace.nickname_email.lower()    # nickname_email
                        )

def _list(options, parser):
    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    NICKNAME2.outputAllAliases(namespace.domain, auth_token)

    return True

def _listnicknamesof(options, parser):
    # Set parser options
    parser.add_argument( "user_email"
                       , action = "store"
                       , help   = "User name."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    NICKNAME2.outputAllAliasesOfUser(namespace.domain, auth_token, namespace.user_email.lower())

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
        must_keys = ["user_email", "nickname_email"]
        if not _func.checkValidHeader(header, *must_keys):
            return False
        f.seek(0, 0)

        # Read csv
        for record in reader:
            must_values = ["user_email", "nickname_email"]
            if not _func.checkRecordHasValue(record, *must_values):
                continue

            # Operation
            _func.operate( NICKNAME2.createAlias
                         , record["nickname_email"].lower()
                         , parser.prog
                         , namespace.result_file
                                , namespace.domain
                                , auth_token
                                , record["user_email"].lower()  # user_email
                                , record["nickname_email"]      # nickname_email
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
        must_keys = ["nickname_email"]
        if not _func.checkValidHeader(header, *must_keys):
            return False
        f.seek(0, 0)

        # Read csv
        for record in reader:
            must_values = ["nickname_email"]
            if not _func.checkRecordHasValue(*must_values):
                continue

            # Operation
            _func.operate( NICKNAME2.deleteAlias
                         , record["nickname_email"].lower()
                         , parser.prog
                         , namespace.result_file
                                , namespace.domain
                                , auth_token
                                , record["nickname_email"].lower()  # nickname_email
                         )

        return True

