# -*- coding: utf-8 -*-
#
# GoogleAppsAccountManager: frontend/ou
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

# OU HELP
OU_HELP = """Usage: gapps-tool ou <subcommand>

Available subcommands:
  create          - Create organizational unit
  modify          - Modify organizational unit
  delete          - Delete organizational unit
  moveuser        - Move user to organizational unit
  list            - List all ous
  listuserswithou - List all users with ou

"""

# Subcommand list
__subcommand__ = { "create"         : "_create"
                 , "modify"         : "_modify"
                 , "delete"         : "_delete"
                 , "moveuser"       : "_moveuser"
                 , "list"           : "_list"
                 , "listuserswithou": "_listuserswithou"
                 , "create_f"       : "_create_f"
                 , "modify_f"       : "_modify_f"
                 , "delete_f"       : "_delete_f"
                 , "moveuser_f"     : "_moveuser_f"
                 }

import sys
from GoogleAppsAccountManager.organizationalunit import client as OU
from GoogleAppsAccountManager.organizationalunituser import client as OU_U
from GoogleAppsAccountManager.frontend import _func, _messages

def run(options, parser, my_name):
    from GoogleAppsAccountManager.frontend import _runSubcommand
    _runSubcommand(options, parser, my_name, __subcommand__, OU_HELP)

def _create(options, parser):
    # Set parser options 
    parser.add_argument( "ou_path"
                       , action = "store"
                       , help   = "Organizational unit full path (e.g. /development/sales)."
                       )
    parser.add_argument( "-d", "--description"
                       , action  = "store"
                       , default = ""
                       , help    = "Specify organizational unit description."
                       )
    parser.add_argument( "-b", "--block-inheritance"
                       , action  = "store_true"
                       , default = False
                       , help    = "Block inheritance (default = False)."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Get Customer ID
    try:
        customer_id = __getCustomerId(auth_token)
    except:
        return False

    # Check ou has full path
    if namespace.ou_path[0] != "/":
        sys.stderr.write(_messages.OU_HAS_NOT_FULL_PATH)
        return False

    # Check block/unblock inheritance
    if namespace.block_inheritance == True:
        block_inheritance = "true"
    else:
        block_inheritance = "false"

    # Operation
    return _func.operate( OU.createOu
                        , namespace.ou_path
                        , parser.prog
                        , namespace.result_file
                               , auth_token
                               , customer_id
                               , namespace.ou_path            # ou path
                               , namespace.description        # ou description
                               , block_inheritance            # block inheritance
                        )

def _modify(options, parser):
    # Set parser options 
    parser.add_argument( "ou_path"
                       , action = "store"
                       , help   = "Organizational unit full path (e.g. /development/sales)."
                       )
    parser.add_argument( "-d", "--description"
                       , action  = "store"
                       , default = None
                       , help    = "Specify organizational unit description."
                       )
    parser.add_argument( "-b", "--block-inheritance"
                       , action  = "store_true"
                       , default = False
                       , help    = "Block inheritance."
                       )
    parser.add_argument( "-B", "--unblock-inheritance"
                       , action  = "store_true"
                       , default = False
                       , help    = "Unblock inheritance."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Get Customer ID
    try:
        customer_id = __getCustomerId(auth_token)
    except:
        return False

    # Check ou has full path
    if namespace.ou_path[0] != "/":
        sys.stderr.write(_messages.OU_HAS_NOT_FULL_PATH)
        return False

    # Check block/unblock inheritance
    if ( namespace.block_inheritance == True
             and namespace.unblock_inheritance == True ):
        sys.stderr.write(_messages.OU_BLOCK_UNBLOCK_BOTH)
        return False
    elif namespace.block_inheritance == True:
        block_inheritance = "true"
    elif namespace.unblock_inheritance == True:
        block_inheritance = "false"
    else:
        block_inheritance = None

    # Operation
    return _func.operate( OU.updateOu
                        , namespace.ou_path
                        , parser.prog
                        , namespace.result_file
                               , auth_token
                               , customer_id
                               , namespace.ou_path            # ou path
                               , namespace.description        # ou description
                               , block_inheritance            # block inheritance
                        )

def _delete(options, parser):
    # Set parser options 
    parser.add_argument( "ou_path"
                       , action = "store"
                       , help   = "Organizational unit full path (e.g. /development/sales)."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Get Customer ID
    try:
        customer_id = __getCustomerId(auth_token)
    except:
        return False

    # Check ou has full path
    if namespace.ou_path[0] != "/":
        sys.stderr.write(_messages.OU_HAS_NOT_FULL_PATH)
        return False

    # Operation
    return _func.operate( OU.deleteOu
                        , namespace.ou_path
                        , parser.prog
                        , namespace.result_file
                               , auth_token
                               , customer_id
                               , namespace.ou_path            # ou path
                        )

def _moveuser(options, parser):
    # Set parser options 
    parser.add_argument( "user_name"
                       , action  = "store"
                       , help    = "User name."
                       )
    parser.add_argument( "new_ou_path"
                       , action = "store"
                       , help   = "Organizational unit full path (e.g. /development/sales)."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Get Customer ID
    try:
        customer_id = __getCustomerId(auth_token)
    except:
        return False

    # Check ou has full path
    if namespace.new_ou_path[0] != "/":
        sys.stderr.write(_messages.OU_HAS_NOT_FULL_PATH)
        return False

    # Operation
    return _func.operate( OU_U.moveUserToOu
                        , namespace.new_ou_path
                        , "{} \"{}\"".format( parser.prog
                                            , namespace.user_name.lower()
                                            )
                        , namespace.result_file
                          , auth_token
                          , customer_id
                          , "{}@{}".format( namespace.user_name.lower()
                                          , namespace.domain
                                          )              # user name
                          , namespace.new_ou_path        # ou path
                        )

def _list(options, parser):
    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Get Customer ID
    try:
        customer_id = __getCustomerId(auth_token)
    except:
        return False

    # Operation
    OU.outputAllOusInDomain(auth_token, customer_id)

    return True

def _listuserswithou(options, parser):
    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Get Customer ID
    try:
        customer_id = __getCustomerId(auth_token)
    except:
        return False

    # Operation
    OU_U.outputAllUsersWithOu(auth_token, customer_id)

    return True

############################# CSV operation #############################

def _create_f(options, parser):
    import csv

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Get Customer ID
    try:
        customer_id = __getCustomerId(auth_token)
    except:
        return False

    # Get records from csv file
    with open(namespace.csv_file) as f:
        reader = csv.DictReader(f)

        # Check header
        header = f.next().replace("\n", "").split(",")
        must_keys = ["ou_path", "description", "block_inheritance"]
        if not _func.checkValidHeader(header, *must_keys):
            return False
        f.seek(0, 0)

        # Read csv
        for record in reader:
            must_values = ["ou_path"]
            if not _func.checkRecordHasValue(record, *must_values):
                continue

            # Check ou has full path
            if record["ou_path"][0] != "/":
                sys.stderr.write(_messages.OU_HAS_NOT_FULL_PATH)
                continue

            # Check block/unblock inheritance
            block_inheritance = record["block_inheritance"].lower()
            if block_inheritance == "true":
                block_inheritance = "true"
            else:
                block_inheritance = "false"

            # Operation
            _func.operate( OU.createOu
                         , record["ou_path"]
                         , parser.prog
                         , namespace.result_file
                                , auth_token
                                , customer_id
                                , record["ou_path"]            # ou path
                                , record["description"]        # ou description
                                , block_inheritance            # block inheritance
                         )
        return True

def _modify_f(options, parser):
    import csv

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Get Customer ID
    try:
        customer_id = __getCustomerId(auth_token)
    except:
        return False

    # Get records from csv file
    with open(namespace.csv_file) as f:
        reader = csv.DictReader(f)

        # Check header
        header = f.next().replace("\n", "").split(",")
        must_keys = ["ou_path", "description", "block_inheritance"]
        if not _func.checkValidHeader(header, *must_keys):
            return False
        f.seek(0, 0)

        # Read csv
        for record in reader:
            must_values = ["ou_path"]
            if not _func.checkRecordHasValue(record, *must_values):
                continue

            # Check ou has full path
            if record["ou_path"][0] != "/":
                sys.stderr.write(_messages.OU_HAS_NOT_FULL_PATH)
                continue

            # Check block/unblock inheritance
            block_inheritance = record["block_inheritance"].lower()
            if block_inheritance == "true":
                block_inheritance = "true"
            elif block_inheritance == "false":
                block_inheritance = "false"
            else:
                block_inheritance = None

            # Operation
            _func.operate( OU.updateOu
                         , record["ou_path"]
                         , parser.prog
                         , namespace.result_file
                             , auth_token
                             , customer_id
                             , record["ou_path"]               # ou path
                             , _func.replaceSpace2None(
                                        record["description"]) # ou description
                             , block_inheritance               # block inheritance
                         )
        return True

def _delete_f(options, parser):
    import csv

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Get Customer ID
    try:
        customer_id = __getCustomerId(auth_token)
    except:
        return False

    # Get records from csv file
    with open(namespace.csv_file) as f:
        reader = csv.DictReader(f)

        # Check header
        header = f.next().replace("\n", "").split(",")
        must_keys = ["ou_path"]
        if not _func.checkValidHeader(header, *must_keys):
            return False
        f.seek(0, 0)

        # Read csv
        for record in reader:
            must_values = ["ou_path"]
            if not _func.checkRecordHasValue(record, *must_values):
                continue

            # Check ou has full path
            if record["ou_path"][0] != "/":
                sys.stderr.write(_messages.OU_HAS_NOT_FULL_PATH)
                continue

            # Operation
            _func.operate( OU.deleteOu
                         , record["ou_path"]
                         , parser.prog
                         , namespace.result_file
                              , auth_token
                              , customer_id
                              , record["ou_path"]            # ou path
                         )
        return True

def _moveuser_f(options, parser):
    import csv

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Get Customer ID
    try:
        customer_id = __getCustomerId(auth_token)
    except:
        return False

    # Get records from csv file
    with open(namespace.csv_file) as f:
        reader = csv.DictReader(f)

        # Check header
        header = f.next().replace("\n", "").split(",")
        must_keys = ["user_name", "ou_path"]
        if not _func.checkValidHeader(header, *must_keys):
            return False
        f.seek(0, 0)

        # Read csv
        for record in reader:
            must_values = ["user_name", "ou_path"]
            if not _func.checkRecordHasValue(record, *must_values):
                continue

            # Check ou has full path
            if record["ou_path"][0] != "/":
                sys.stderr.write(_messages.OU_HAS_NOT_FULL_PATH)
                continue

            _func.operate( OU_U.moveUserToOu
                         , record["ou_path"]
                         , "{} \"{}\"".format( parser.prog
                                             , record["user_name"].lower()
                                             )
                         , namespace.result_file
                              , auth_token
                              , customer_id
                              , "{}@{}".format( record["user_name"]
                                              , namespace.domain
                                              )          # user name
                              , record["ou_path"]        # ou path
                         )
        return True

############################# Get customer id #############################
def __getCustomerId(auth_token):
    try:
        return OU.getCustomerId(auth_token)
    except Exception, e:
        import traceback
        traceback.print_exc()
        return False
