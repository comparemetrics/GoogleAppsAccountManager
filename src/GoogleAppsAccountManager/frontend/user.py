# -*- coding: utf-8 -*-
#
# GoogleAppsAccountManager: frontend/user
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

# USER HELP
USER_HELP = """Usage: gapps-tool user <subcommand> 

Available subcommands:
  create          - Create user
  modify          - Modify user
  delete          - Delete user
  disable         - Disable user
  enable          - Enable user
  passwd          - Change user's password
  list            - List all users

"""

# Subcommand list
__subcommand__ = { "create"   : "_create"
                 , "modify"   : "_modify"
                 , "delete"   : "_delete"
                 , "disable"  : "_disable"
                 , "enable"   : "_enable"
                 , "passwd"   : "_passwd"
                 , "list"     : "_list"
                 , "create_f" : "_create_f"
                 , "modify_f" : "_modify_f"
                 , "delete_f" : "_delete_f"
                 , "disable_f": "_disable_f"
                 , "enable_f" : "_enable_f"
                 }

import sys
from GoogleAppsAccountManager.user import client as USER
from GoogleAppsAccountManager.frontend import _func, _messages

def run(options, parser, my_name):
    from GoogleAppsAccountManager.frontend import _runSubcommand
    _runSubcommand(options, parser, my_name, __subcommand__, USER_HELP)

def _create(options, parser):
    # Set parser options
    parser.add_argument( "user_name"
                       , action = "store"
                       , help   = "User name."
                       )
    parser.add_argument( "sn"
                       , action = "store"
                       , help   = "Family name."
                       )
    parser.add_argument( "given_name"
                       , action = "store"
                       , help   = "Given name."
                       )
    parser.add_argument( "-m", "--md5"
                       , action  = "store_true"
                       , default = False
                       , help    = "Use MD5 hash function (default = SHA-1)."
                       )
    parser.add_argument( "-L", "--lock"
                       , action  = "store_true"
                       , default = False
                       , help    = "Lock a user's account."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Check hash function name
    if namespace.md5 == True:
        hash_function_name = "MD5"
    else:
        hash_function_name = "SHA-1"

    # Check lock/unlock
    if namespace.lock == True:
        suspended = "true"
    else:
        suspended = "false"

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Get user's password
    hash_password = _func.getHashedPassword_interactive(hash_function_name)

    # Operation
    return _func.operate( USER.createUser
                        , namespace.user_name.lower()
                        , parser.prog
                        , namespace.result_file
                               , namespace.domain
                               , auth_token
                               , namespace.user_name.lower()    # user
                               , hash_password                  # password
                               , namespace.sn                   # sn
                               , namespace.given_name           # given name
                               , hash_function_name             # function name
                               , suspended                      # suspended
                        )

def _modify(options, parser):
    # Set parser options 
    parser.add_argument( "user_name"
                       , action = "store"
                       , help   = "User name."
                       )
    parser.add_argument( "-p", "--password"
                       , action = "store"
                       , help   = "Specify password."
                       )
    parser.add_argument( "-m", "--md5"
                       , action  = "store_true"
                       , default = False
                       , help    = "Use MD5 hash function (default = SHA-1)."
                       )
    parser.add_argument( "-L", "--lock"
                       , action  = "store_true"
                       , default = False
                       , help    = "Lock a user's account."
                       )
    parser.add_argument( "-U", "--unlock"
                       , action  = "store_true"
                       , default = False
                       , help    = "Unock a user's account."
                       )
    parser.add_argument( "-s", "--sn"
                       , action = "store"
                       , help   = "Specify sn."
                       )
    parser.add_argument( "-g", "--given-name"
                       , action = "store"
                       , help   = "Specify given_name."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Check hash function name
    if namespace.md5:
        hash_function_name = "MD5"
    else:
        hash_function_name = "SHA-1"
    hash_password = _func.getHashedPassword(namespace.password, hash_function_name)

    # Check lock/unlock
    suspended = _func.getTrueOrFalse(namespace.lock, namespace.unlock)
    if suspended == False:
        return False

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    return _func.operate( USER.updateUser
                        , namespace.user_name.lower()
                        , parser.prog
                        , namespace.result_file
                               , namespace.domain
                               , auth_token
                               , namespace.user_name.lower()    # user
                               , hash_password                  # password
                               , namespace.sn                   # sn
                               , namespace.given_name           # given name
                               , hash_function_name             # function name
                               , suspended                      # suspended
                        )

def _delete(options, parser):
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
    return _func.operate( USER.deleteUser
                        , namespace.user_name.lower()
                        , parser.prog
                        , namespace.result_file
                               , namespace.domain
                               , auth_token
                               , namespace.user_name.lower()    # user
                        )

def _disable(options, parser):
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
    return _func.operate( USER.updateUser
                        , namespace.user_name.lower()
                        , parser.prog
                        , namespace.result_file
                               , namespace.domain
                               , auth_token
                               , namespace.user_name.lower()    # user
                               , suspended="true"               # suspended
                        )

def _enable(options, parser):
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
    return _func.operate( USER.updateUser
                        , namespace.user_name.lower()
                        , parser.prog
                        , namespace.result_file
                               , namespace.domain
                               , auth_token
                               , namespace.user_name.lower()    # user
                               , suspended="false"              # suspended
                        )

def _passwd(options, parser):
    # Set parser options 
    parser.add_argument( "user_name"
                       , action = "store"
                       , help   = "User name."
                       )
    parser.add_argument( "-m", "--md5"
                       , action  = "store_true"
                       , default = False
                       , help    = "Use MD5 hash function (default = SHA-1)."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Check option
    if namespace.md5 == True:
        hash_function_name = "MD5"
    else:
        hash_function_name = "SHA-1"

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Get user's password
    hash_password = _func.getHashedPassword_interactive(hash_function_name)

    # Operation
    return _func.operate( USER.updateUser
                        , namespace.user_name.lower()
                        , parser.prog
                        , namespace.result_file
                             , namespace.domain
                             , auth_token
                             , namespace.user_name.lower()             # user
                             , password = hash_password                # password
                             , hash_function_name = hash_function_name # function
                        )

def _list(options, parser):
    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    USER.outputAllUsers(namespace.domain, auth_token)

    return True

############################# CSV operation #############################

def _create_f(options, parser):
    import csv

    # Set parser options 
    parser.add_argument( "-m", "--md5"
                       , action  = "store_true"
                       , default = False
                       , help    = "Use MD5 hash function (default = SHA-1)."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Check hash function name
    if namespace.md5 == True:
        hash_function_name = "MD5"
    else:
        hash_function_name = "SHA-1"

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Get records from csv file
    with open(namespace.csv_file) as f:
        reader = csv.DictReader(f)

        # Check header
        header = f.next().replace("\n", "").split(",")
        must_keys = ["user_name", "password", "sn", "given_name", "lock"]
        if not _func.checkValidHeader(header, *must_keys):
            return False
        f.seek(0, 0)

        # Read csv
        for record in reader:
            must_values = ["user_name", "password", "sn", "given_name"]
            if not _func.checkRecordHasValue(record, *must_values):
                continue

            # password hashed
            hash_password = _func.getHashedPassword( record["password"]
                                                   , hash_function_name
                                                   )

            # Check suspended
            suspended = record["lock"].lower()
            if suspended == "true":
                suspended = "true"
            else:
                suspended = "false"

            # Operation
            _func.operate( USER.createUser
                         , record["user_name"].lower()
                         , parser.prog
                         , namespace.result_file
                                , namespace.domain
                                , auth_token
                                , record["user_name"].lower()  # user
                                , hash_password                # password
                                , record["sn"]                 # sn
                                , record["given_name"]         # given name
                                , hash_function_name           # function name
                                , suspended                    # suspended
                         )
        return True

def _modify_f(options, parser):
    import csv

    # Set parser options 
    parser.add_argument( "-m", "--md5"
                       , action  = "store_true"
                       , default = False
                       , help    = "Use MD5 hash function (default = SHA-1)."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Check hash function name
    if namespace.md5 == True:
        hash_function_name = "MD5"
    else:
        hash_function_name = "SHA-1"

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Get records from csv file
    with open(namespace.csv_file) as f:
        reader = csv.DictReader(f)

        # Check header
        header = f.next().replace("\n", "").split(",")
        must_keys = ["user_name", "password", "sn", "given_name", "lock"]
        if not _func.checkValidHeader(header, *must_keys):
            return False
        f.seek(0, 0)

        # Read csv
        for record in reader:
            must_values = ["user_name"]
            if not _func.checkRecordHasValue(*must_values):
                continue

            # Get hashed password
            hash_password = _func.getHashedPassword( record["password"]
                                                   , hash_function_name
                                                   )

            # Check suspended
            suspended = record["lock"].lower()
            if suspended == "true":
                suspended = "true"
            elif suspended == "false":
                suspended = "false"
            else:
                suspended = None

            # Operation
            _func.operate( USER.updateUser
                         , record["user_name"].lower()
                         , parser.prog
                         , namespace.result_file
                             , namespace.domain
                             , auth_token
                             , record["user_name"].lower()                   # user
                             , hash_password                                 # password
                             , _func.replaceSpace2None(record["sn"])         # sn
                             , _func.replaceSpace2None(record["given_name"]) # given name
                             , hash_function_name                            # function name
                             , suspended                                     # suspended
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
        must_keys = ["user_name"]
        if not _func.checkValidHeader(header, *must_keys):
            return False
        f.seek(0, 0)

        # Read csv
        for record in reader:
            must_values = ["user_name"]
            if not _func.checkRecordHasValue(*must_values):
                continue

            # Operation
            _func.operate( USER.deleteUser
                         , record["user_name"].lower()
                         , parser.prog
                         , namespace.result_file
                                , namespace.domain
                                , auth_token
                                , record["user_name"].lower()  # user
                         )

        return True

def _disable_f(options, parser):
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
        must_keys = ["user_name"]
        if not _func.checkValidHeader(header, *must_keys):
            return False
        f.seek(0, 0)

        # Read csv
        for record in reader:
            must_values = ["user_name"]
            if not _func.checkRecordHasValue(*must_values):
                continue

            # Operation
            _func.operate( USER.updateUser
                         , record["user_name"].lower()
                         , parser.prog
                         , namespace.result_file
                                , namespace.domain
                                , auth_token
                                , record["user_name"].lower()  # user
                                , suspended="true"             # suspended
                         )

        return True

def _enable_f(options, parser):
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
        must_keys = ["user_name"]
        if not _func.checkValidHeader(header, *must_keys):
            return False
        f.seek(0, 0)

        # Read csv
        for record in reader:
            must_values = ["user_name"]
            if not _func.checkRecordHasValue(*must_values):
                continue

            # Operation
            _func.operate( USER.updateUser
                         , record["user_name"].lower()
                         , parser.prog
                         , namespace.result_file
                                , namespace.domain
                                , auth_token
                                , record["user_name"].lower()  # user
                                , suspended="false"            # suspended
                         )

        return True

