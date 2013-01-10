#
# GoogleAppsAccountManager: frontend/_messages
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

########################### Result messages ###########################
SUCCESS_RESULT = (
"""[{date}],{target},{operation} succeeded
"""
)
FAILED_RESULT = (
"""[{date}],{target},{operation} failed,{detail}
"""
)

########################### Error messages ###########################
ADMIN_OR_DOMIN_NOT_SPECIFIED = (
"""Admin name or domain is not specified in command-line or config file.
"""
)

ADMIN_LOGIN_FAILED = (
"""Failed to login by administrator's account. Check password.
"""
)

USER_LOCK_UNLOCK_BOTH = (
"""Lock and unlock options exist at the same time.
"""
)

CONFLICTED_OPTIONS = (
"""Conflicted options specified.
"""
)

OU_HAS_NOT_FULL_PATH = (
"""ou_path prefix does not have "/" character. Retry with "/".
"""
)

OU_BLOCK_UNBLOCK_BOTH = (
"""block_inheritance and unblock_inheritance options exist at the same time.
"""
)

GROUP_ASSIGNED_OWNER = (
"""Cannot assign group id to owner. Specify user name.
"""
)
