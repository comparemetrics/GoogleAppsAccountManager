# -*- coding: utf-8 -*-
#
# GoogleAppsAccountManager: frontend
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

# GLOBAL HELP
GLOBAL_HELP = """Usage: gapps-tool <subcommand>

Available subcommands:
  user            - User management
  user2           - Enhanced user management. This can manage multiple domain
  nickname        - Nickname Management
  nickname2       - Enhanced nickname management. This can manage multiple domain
  group           - Group management
  ou              - Organizational unit management

"""

from GoogleAppsAccountManager.frontend import user, user2, nickname, nickname2, group, ou
import argparse 

def run(subcommand, options):
    # Set global options parser
    parser = argparse.ArgumentParser(description="Google apps account manager")
    parser.add_argument( "-A", "--admin-name"
                       , action   = "store"
                       , required = False
                       , help     = "Administrator's name"
                       )
    parser.add_argument( "-D", "--domain"
                       , action="store"
                       , required = False
                       , help     = "Domain name"
                       )
    parser.add_argument( "-C", "--config"
                       , action="store"
                       , help     = "Specify config file. "
                       )
    parser.add_argument( "-r", "--result-file"
                       , action  = "store"
                       , help    = "Specify result file"
                       )
    parser.add_argument( "-f", "--csv-file"
                       , action   = "store"
                       , help     = "Specify csv file for batching"
                       )

    # Run subcommand
    try:
        subcommand_module = eval(subcommand)
    except Exception, e:
        import sys
        sys.stderr.write(GLOBAL_HELP)
        return False
    else:
        return subcommand_module.run(options, parser, subcommand)

def _runSubcommand(options, parser, my_name, subcommand_dict, help):
    import sys
    from GoogleAppsAccountManager import errors
    from GoogleAppsAccountManager.frontend._func import parseConfig

    # Which subcommand?
    options = list(options)
    try:
        subcommand = options[0]
        parser.prog = "{} {} {}".format(parser.prog, my_name, subcommand)

        if "-f" in options or "--csv-file" in options:
            if subcommand_dict.has_key(subcommand + "_f"):
                subcommand = subcommand + "_f"

        subcommand_func = eval("{}.{}".format(my_name, subcommand_dict[subcommand]))
    except Exception, e:
        sys.stdout.write(help)
        return False

    # "-C" or "--config" specified?
    specified_config = None
    for (i, opt) in enumerate(options):
        if opt in ["-C", "--config"]:
            specified_config = parser.parse_args(options[i:i+2]).config

    # Parse config file
    param_dict = parseConfig(specified_config)

    # Parse result
    must_cnt = 0
    for must in ["-A", "--admin-name", "-D", "--domain"]:
        if must in options:
            must_cnt += 1
    if must_cnt < 2:
        if  param_dict is not None:
            options += [ "-A", param_dict["admin_name"]
                       , "-D", param_dict["domain"]
                       ]
            if param_dict.has_key("result_file"):
                if "-r" in options or "--result-file" in options:
                    pass
                else:
                    options += ["-r", param_dict["result_file"]]
        else:
            sys.stderr.write(_messages.ADMIN_OR_DOMIN_NOT_SPECIFIED)
            return False

    # Operate subcommand
    try:
        return subcommand_func(options[1:], parser)
    except errors.AdminLoginError:
        sys.stderr.write(_messages.ADMIN_LOGIN_FAILED)
        return False

