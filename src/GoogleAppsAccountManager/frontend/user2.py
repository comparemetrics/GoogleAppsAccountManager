# -*- coding: utf-8 -*-
#
# GoogleAppsAccountManager: frontend/user2
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2013-01-01, since 2013-01-01
#

# USER2 HELP
USER2_HELP = """Usage: gapps-tool user2 <subcommand> 

Available subcommands:
  create          - Create user
  modify          - Modify user
  delete          - Delete user
  disable         - Disable user
  enable          - Enable user
  passwd          - Change user's password
  assignadmin     - Assign administrator to user
  demoteadmin     - Demote user fromt Administrtor to general user
  list            - List all users

"""

# Subcommand list
__subcommand__ = { "create"      : "_create"
                 , "modify"      : "_modify"
                 , "delete"      : "_delete"
                 , "disable"     : "_disable"
                 , "enable"      : "_enable"
                 , "passwd"      : "_passwd"
                 , "assignadmin" : "_assignadmin"
                 , "demoteadmin" : "_demoteadmin"
                 , "list"        : "_list"
                 , "create_f"    : "_create_f"
                 , "modify_f"    : "_modify_f"
                 , "delete_f"    : "_delete_f"
                 , "disable_f"   : "_disable_f"
                 , "enable_f"    : "_enable_f"
                 }

import sys
from GoogleAppsAccountManager.multipledomainuser import client as USER2
from GoogleAppsAccountManager.frontend import _func, _messages

def run(options, parser, my_name):
    from GoogleAppsAccountManager.frontend import _runSubcommand
    _runSubcommand(options, parser, my_name, __subcommand__, USER2_HELP)

def _create(options, parser):
    # Set parser options
    parser.add_argument( "user_email"
                       , action = "store"
                       , help   = "User's mail address."
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
    parser.add_argument(       "--assign-administrator"
                       , action  = "store_const"
                       , const   = "true"
                       , default = "false"
                       , help    = "Assign administrator to user (default = not assign)."
                       )
    parser.add_argument(       "--no-change-password-at-next-login"
                       , action  = "store_const"
                       , const   = "false"
                       , default = "true"
                       , help    = ( "If this flag specified, "
                                     "user do not have to change password "
                                     "at next login (default = True)."
                                   )
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
    return _func.operate( USER2.createUser
                        , namespace.user_email.lower()
                        , parser.prog
                        , namespace.result_file
                               , namespace.domain
                               , auth_token
                               , namespace.user_email.lower()   # user
                               , hash_password                  # password
                               , namespace.sn                   # sn
                               , namespace.given_name           # given name
                               , hash_function_name             # function name
                               , suspended                      # suspended
                               , namespace.assign_administrator # assign admin?
                               , namespace.no_change_password_at_next_login # no change?
                        )

def _modify(options, parser):
    # Set parser options 
    parser.add_argument( "user_email"
                       , action = "store"
                       , help   = "User's mail address."
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
    parser.add_argument(       "--assign-administrator"
                       , action  = "store_true"
                       , default = False
                       , help    = "Assign administrator to user."
                       )
    parser.add_argument(       "--demote-administrator"
                       , action  = "store_true"
                       , default = False
                       , help    = "Demote user from administrator to general user."
                       )
    parser.add_argument(       "--change-password-at-next-login"
                       , action  = "store_true"
                       , default = False
                       , help    = "User must change password at next login."
                       )
    parser.add_argument(       "--no-change-password-at-next-login"
                       , action  = "store_true"
                       , default = False
                       , help    = "User do not have to change password at next login."
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

    # Check assign admin/non-admin
    is_admin = _func.getTrueOrFalse( namespace.assign_administrator
                                   , namespace.demote_administrator
                                   )
    if is_admin == False:
        return False

    # Check must change password or not
    is_change_password = _func.getTrueOrFalse( namespace.change_password_at_next_login
                                             , namespace.no_change_password_at_next_login
                                             )
    if is_change_password == False:
        return False

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    return _func.operate( USER2.updateUser
                        , namespace.user_email.lower()
                        , parser.prog
                        , namespace.result_file
                               , namespace.domain
                               , auth_token
                               , namespace.user_email.lower()   # user
                               , hash_password                  # password
                               , namespace.sn                   # sn
                               , namespace.given_name           # given name
                               , hash_function_name             # function name
                               , suspended                      # suspended
                               , is_admin                       # assign admin?
                               , is_change_password             # no change?
                        )

def _delete(options, parser):
    # Set parser options 
    parser.add_argument( "user_email"
                       , action = "store"
                       , help   = "User's mail address."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    return _func.operate( USER2.deleteUser
                        , namespace.user_email.lower()
                        , parser.prog
                        , namespace.result_file
                               , namespace.domain
                               , auth_token
                               , namespace.user_email.lower()    # user
                        )

def _disable(options, parser):
    # Set parser options 
    parser.add_argument( "user_email"
                       , action = "store"
                       , help   = "User's mail address."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    return _func.operate( USER2.updateUser
                        , namespace.user_email.lower()
                        , parser.prog
                        , namespace.result_file
                               , namespace.domain
                               , auth_token
                               , namespace.user_email.lower()    # user
                               , is_suspended="true"             # suspended
                        )

def _enable(options, parser):
    # Set parser options 
    parser.add_argument( "user_email"
                       , action = "store"
                       , help   = "User's mail address."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    return _func.operate( USER2.updateUser
                        , namespace.user_email.lower()
                        , parser.prog
                        , namespace.result_file
                               , namespace.domain
                               , auth_token
                               , namespace.user_email.lower()    # user
                               , is_suspended="false"            # suspended
                        )

def _passwd(options, parser):
    # Set parser options 
    parser.add_argument( "user_email"
                       , action = "store"
                       , help   = "User's mail address."
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
    return _func.operate( USER2.updateUser
                        , namespace.user_email.lower()
                        , parser.prog
                        , namespace.result_file
                             , namespace.domain
                             , auth_token
                             , namespace.user_email.lower()            # user
                             , password = hash_password                # password
                             , hash_function_name = hash_function_name # function
                        )

def _assignadmin(options, parser):
    # Set parser options 
    parser.add_argument( "user_email"
                       , action = "store"
                       , help   = "User's mail address."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    return _func.operate( USER2.updateUser
                        , namespace.user_email.lower()
                        , parser.prog
                        , namespace.result_file
                             , namespace.domain
                             , auth_token
                             , namespace.user_email.lower()            # user
                             , is_admin="true"                         # admin true
                        )

def _demoteadmin(options, parser):
    # Set parser options 
    parser.add_argument( "user_email"
                       , action = "store"
                       , help   = "User's mail address."
                       )

    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    return _func.operate( USER2.updateUser
                        , namespace.user_email.lower()
                        , parser.prog
                        , namespace.result_file
                             , namespace.domain
                             , auth_token
                             , namespace.user_email.lower()            # user
                             , is_admin="false"                        # admin false
                        )

def _list(options, parser):
    # Get options
    namespace = parser.parse_args(options)

    # Get auth token
    auth_token = _func.getAuthTokenByLogin(namespace.admin_name, namespace.domain)

    # Operation
    USER2.outputAllUsers(namespace.domain, auth_token)

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
        must_keys = ["user_email", "password", "sn", "given_name", "must_change_pw_next", "lock"]
        if not _func.checkValidHeader(header, *must_keys):
            return False
        f.seek(0, 0)

        # Read csv
        for record in reader:
            must_values = ["user_email", "password", "sn", "given_name"]
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

            # Check must change password at next login
            is_change_password = record["must_change_pw_next"].lower()
            if is_change_password == "false":
                is_change_password = "false"
            else:
                is_change_password = "true"

            # Operation
            _func.operate( USER2.createUser
                         , record["user_email"].lower()
                         , parser.prog
                         , namespace.result_file
                                , namespace.domain
                                , auth_token
                                , record["user_email"].lower() # user
                                , hash_password                # password
                                , record["sn"]                 # sn
                                , record["given_name"]         # given name
                                , hash_function_name           # function name
                                , suspended                    # suspended
                                , is_change_password=is_change_password # no change
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
        must_keys = ["user_email", "password", "sn", "given_name", "must_change_pw_next", "lock"]
        if not _func.checkValidHeader(header, *must_keys):
            return False
        f.seek(0, 0)

        # Read csv
        for record in reader:
            must_values = ["user_email"]
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

            # Check must change password at next login
            is_change_password = record["must_change_pw_next"].lower()
            if is_change_password == "false":
                is_change_password = "false"
            elif is_change_password == "true":
                is_change_password = "true"
            else:
                is_change_password = None

            # Operation
            _func.operate( USER2.updateUser
                         , record["user_email"].lower()
                         , parser.prog
                         , namespace.result_file
                             , namespace.domain
                             , auth_token
                             , record["user_email"].lower()                  # user
                             , hash_password                                 # password
                             , _func.replaceSpace2None(record["sn"])         # sn
                             , _func.replaceSpace2None(record["given_name"]) # given name
                             , hash_function_name                            # function name
                             , suspended                                     # suspended
                             , is_change_password=is_change_password         # is change
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
        must_keys = ["user_email"]
        if not _func.checkValidHeader(header, *must_keys):
            return False
        f.seek(0, 0)

        # Read csv
        for record in reader:
            must_values = ["user_email"]
            if not _func.checkRecordHasValue(*must_values):
                continue

            # Operation
            _func.operate( USER2.deleteUser
                         , record["user_email"].lower()
                         , parser.prog
                         , namespace.result_file
                                , namespace.domain
                                , auth_token
                                , record["user_email"].lower()  # user
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
        must_keys = ["user_email"]
        if not _func.checkValidHeader(header, *must_keys):
            return False
        f.seek(0, 0)

        # Read csv
        for record in reader:
            must_values = ["user_email"]
            if not _func.checkRecordHasValue(*must_values):
                continue

            # Operation
            _func.operate( USER2.updateUser
                         , record["user_email"].lower()
                         , parser.prog
                         , namespace.result_file
                                , namespace.domain
                                , auth_token
                                , record["user_email"].lower()  # user
                                , is_suspended="true"             # suspended
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
        must_keys = ["user_email"]
        if not _func.checkValidHeader(header, *must_keys):
            return False
        f.seek(0, 0)

        # Read csv
        for record in reader:
            must_values = ["user_email"]
            if not _func.checkRecordHasValue(*must_values):
                continue

            # Operation
            _func.operate( USER2.updateUser
                         , record["user_email"].lower()
                         , parser.prog
                         , namespace.result_file
                                , namespace.domain
                                , auth_token
                                , record["user_email"].lower()  # user
                                , is_suspended="false"            # suspended
                         )

        return True

