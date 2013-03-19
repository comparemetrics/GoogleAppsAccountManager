#
# GoogleAppsAccountManager: frontend/_func
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

import sys
from GoogleAppsAccountManager.frontend import _messages

# Parse config file
#
# Config file name must be "gapps-tool.conf"
# Format like below
#
#   admin_name: "jack"
#   domain: "example.com"
#   result_file: "/var/log/gapp-tool.result"
#
def parseConfig(specified_config=None):
    import os.path

    # Parameters
    admin_name  = "admin_name"
    domain      = "domain"
    result_file = "result_file"

    config_file = None
    if specified_config is not None:
        # Read specified config file
        config_file = open(os.path.expanduser(specified_config), "r")
    else:
        # Read default config files
        default_conf_name = "gapps-tool.conf"
        file_names = [ "/etc/{}"                       .format(default_conf_name)
                     , "/etc/gapps-tool/{}"            .format(default_conf_name)
                     , "~/.config/{}"                  .format(default_conf_name)
                     , "~/.config/gapps-tool/{}"       .format(default_conf_name)
                     , "/opt/test/etc/{}"              .format(default_conf_name)
                     , "/opt/test/etc/gapps-tool/{}"   .format(default_conf_name)
                     , "{}"                            .format(default_conf_name)
                     ]
        for file_name in file_names:
            try:
                config_file = open(os.path.expanduser(file_name), "r")
            except:
                pass
            else:
                break

    if config_file is None:
        return None

    param_dict = "{" + config_file.read().replace("\n", ",") + "}"
    try:
        param_dict = eval(param_dict)
    except Exception, e:
        return str(e)

    if not param_dict.has_key("admin_name") or not param_dict.has_key("domain"):
        return None
    else:
        return param_dict

# Login and get auth token
def getAuthTokenByLogin(admin_name, domain):
    import getpass
    from GoogleAppsAccountManager import login

    admin_pass  = getpass.getpass("Administrator's Password:", stream=sys.stderr)
    admin_email = "{}@{}".format(admin_name, domain)
    return login.clientLogin(admin_email, admin_pass)

# Get user's password by interactive shell
def getHashedPassword_interactive(hash_function_name):
    import getpass
    import hashlib
    MAX_RETRY = 3

    if hash_function_name == "SHA-1":
        hashMethod = hashlib.sha1
    elif hash_function_name == "MD5":
        hashMethod = hashlib.md5
    else:
        sys.stderr.write("{} is not supported.\n".format(hash_function_name))
        raise Exception()
    
    for cnt in range(MAX_RETRY):
        user_pass  = getpass.getpass("New User's Password:", stream=sys.stderr)
        check_pass = getpass.getpass("Retype new User's Password:", stream=sys.stderr)
        if user_pass == check_pass:
            return hashMethod(user_pass).hexdigest()
        sys.stderr.write("Sorry, passwords do not match.\n")

    sys.stderr.write("Try again.\n")
    raise Exception()

# Get user's password
def getHashedPassword(plain_pass, hash_function_name):
    import hashlib
    if plain_pass is None:
        return None
    if hash_function_name == "SHA-1":
        return hashlib.sha1(plain_pass).hexdigest()
    elif hash_function_name == "MD5":
        return hashlib.md5(plain_pass).hexdigest()

# Get "true" string, "false" string or None
# e.g. When you want to handle --lock and --unlock options,
#      this may be of help.
#
# A and notA arguments must be True or False boolean object.
def getTrueOrFalse(A, notA):
    if (A == True) and (notA == True):
        sys.stderr.write(_messages.CONFLICTED_OPTIONS)
        return False
    elif A == True:
        return "true"
    elif notA == True:
        return "false"
    else:
        return None

# Check record has correct field
# record must be dictionary
def checkRecordHasKey(record, *fields):
    for key in fields:
        if not record.has_key(key):
            sys.stderr.write("error: csv record is not correct.\n")
            return False
    return True

# Check csv file has correct header
def checkValidHeader(header, *must_keys):
    for key in must_keys:
        if not key in header:
            sys.stderr.write(
                    "error: Invalid csv header. CSV header must be like below.\n"
                    "\n{}\n\n".format(",".join(must_keys))
                    )
            return False
    return True

# Check record has value
def checkRecordHasValue(record, *fields):
    for key in fields:
        if record[key] == "":
            sys.stderr.write("error: {} must have value.\n".format(key))
            return False
    return True

# Replace space to None object
def replaceSpace2None(val, orig="", src=None):
    if val == orig:
        return src
    else:
        return val

# Core operation
def operate(f, target, operation_name, result_file, *args, **kwargs):
    import time
    from GoogleAppsAccountManager import errors

    try:
        f(*args, **kwargs)
    except errors.ResponseError_xml, e:
        detail = ( "error code \"{}\": invalid input \"{}\": reason \"{}\""
                  .format(e.error_code, e.invalid_input, e.reason)
                 )
        sys.stdout.write( _messages.FAILED_RESULT
                         .format( target = target
                                , operation = operation_name
                                , detail = detail
                                , date = time.strftime("%b %d %H:%M:%S")
                                )
                        )
        if result_file is not None:
            with open(result_file, "a") as f:
                f.write( _messages.FAILED_RESULT
                        .format( target = target
                               , operation = operation_name
                               , detail = detail
                               , date = time.strftime("%b %d %H:%M:%S")
                               )
                       )
        return False
    except errors.ResponseError_string, e:
        detail = e.reason
        sys.stdout.write( _messages.FAILED_RESULT
                         .format( target = target
                                , operation = operation_name
                                , detail = detail
                                , date = time.strftime("%b %d %H:%M:%S")
                                )
                        )
        if result_file is not None:
            with open(result_file, "a") as f:
                f.write( _messages.FAILED_RESULT
                        .format( target = target
                               , operation = operation_name
                               , detail = detail
                               , date = time.strftime("%b %d %H:%M:%S")
                               )
                       )
        return False
    except errors.NoParametersError, e:
        detail = "No parameters specified"
        sys.stdout.write( _messages.FAILED_RESULT
                         .format( target = target
                                , operation = operation_name
                                , detail = detail
                                , date = time.strftime("%b %d %H:%M:%S")
                                )
                        )
        if result_file is not None:
            with open(result_file, "a") as f:
                f.write( _messages.FAILED_RESULT
                        .format( target = target
                               , operation = operation_name
                               , detail = detail
                               , date = time.strftime("%b %d %H:%M:%S")
                               )
                       )
        return False
    except Exception, e:
        import traceback
        traceback.print_exc()
        return False
    else:
        if "list" in operation_name:
            return True

        sys.stdout.write( _messages.SUCCESS_RESULT
                         .format( target = target
                                , operation = operation_name
                                , date = time.strftime("%b %d %H:%M:%S")
                                )
                        )
        if result_file is not None:
            with open(result_file, "a") as f:
                f.write( _messages.SUCCESS_RESULT
                        .format( target = target
                               , operation = operation_name
                               , date = time.strftime("%b %d %H:%M:%S")
                               )
                       )
        return True

