#!/usr/bin/python
#
# GoogleAppsAccountManager
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

import sys
from distutils.core import setup

setup( name         = 'GoogleAppsAccountManager'
     , version      = '0.9.10'
     , description  = 'Python client library for GoogleApps Provisioning API'
     , author       = 'kamei'
     , author_email = 'sandkamei@gmail.com'
     , license      = 'GPL v2'
     , url          = 'http://www.osstech.co.jp'
     , packages     = [ 'GoogleAppsAccountManager'
                      , 'GoogleAppsAccountManager.frontend'
                      , 'GoogleAppsAccountManager.group'
                      , 'GoogleAppsAccountManager.groupmember'
                      , 'GoogleAppsAccountManager.groupowner'
                      , 'GoogleAppsAccountManager.nickname'
                      , 'GoogleAppsAccountManager.multipledomainuser'
                      , 'GoogleAppsAccountManager.multipledomainnickname'
                      , 'GoogleAppsAccountManager.organizationalunituser'
                      , 'GoogleAppsAccountManager.organizationalunit'
                      , 'GoogleAppsAccountManager.user'
                      ]
     , package_dir  = {'GoogleAppsAccountManager':'src/GoogleAppsAccountManager'}
     , scripts      = ['bin/gapps-tool']
     , data_files   = [('/etc/bash_completion.d', ['bash_completion.d/gapps-tool'])]
     )

