#
# GoogleAppsAccountManager: template
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

USER_ENTRY = """<?xml version='1.0' encoding='UTF-8'?>
<entry xmlns='http://www.w3.org/2005/Atom' xmlns:apps='http://schemas.google.com/apps/2006' xmlns:gd='http://schemas.google.com/g/2005'>
    <id>https://apps-apis.google.com/a/feeds/{domain}/user/2.0/{user_name}</id>
    <updated>1970-01-01T00:00:00.000Z</updated>
    <category scheme='http://schemas.google.com/g/2005#kind' term='http://schemas.google.com/apps/2006#user'/>
    <title type='text'>{user_name}</title>
    <link rel='self' type='application/atom+xml' href='https://apps-apis.google.com/a/feeds/{domain}/user/2.0/{user_name}'/>
    <link rel='edit' type='application/atom+xml' href='https://apps-apis.google.com/a/feeds/{domain}/user/2.0/{user_name}'/>
    <apps:login
        userName='{user_name}'
        password='{password}'
        hash_function_name='{hash_function_name}'
        suspended='{suspended}'
        ipWhitelisted='false'
        admin='false'
        changePasswordAtNextLogin='false'
        agreedToTerms='false'/>
    <apps:quota limit='{limit}'/>
    <apps:name familyName='{sn}' givenName='{given_name}'/>
    <gd:feedLink rel='http://schemas.google.com/apps/2006#user.nicknames' href='https://apps-apis.google.com/a/feeds/{domain}/nickname/2.0?username={user_name}'/>
    <gd:feedLink rel='http://schemas.google.com/apps/2006#user.emailLists' href='https://apps-apis.google.com/a/feeds/{domain}/emailList/2.0?recipient={user_name}%40{domain}'/>
</entry>"""

GROUP_ENTRY = """<?xml version='1.0' encoding='UTF-8'?>
<entry xmlns='http://www.w3.org/2005/Atom' xmlns:apps='http://schemas.google.com/apps/2006'>
    <id>https://apps-apis.google.com/a/feeds/group/2.0/{domain}/{group_id}%40{domain}</id>
    <updated>1970-01-01T00:00:00.000Z</updated>
    <link rel='self' type='application/atom+xml' href='https://apps-apis.google.com/a/feeds/group/2.0/{domain}/{group_id}%40{domain}'/>
    <link rel='edit' type='application/atom+xml' href='https://apps-apis.google.com/a/feeds/group/2.0/{domain}/{group_id}%40{domain}'/>
    <apps:property name='groupId' value='{group_id}@{domain}'/>
    <apps:property name='groupName' value='{groupname}'/>
    <apps:property name='emailPermission' value='Domain'/>
    <apps:property name='permissionPreset' value='TeamDomain'/>
    <apps:property name='description' value='{description}'/>
</entry>"""

GROUP_MEMBER_ENTRY = """<?xml version='1.0' encoding='UTF-8'?>
<entry xmlns='http://www.w3.org/2005/Atom' xmlns:apps='http://schemas.google.com/apps/2006'>
    <id>https://apps-apis.google.com/a/feeds/group/2.0/{domain}/{group_id}/member/{membername}%40{domain}</id>
    <updated>1970-01-01T00:00:00.000Z</updated>
    <link rel='self' type='application/atom+xml' href='https://apps-apis.google.com/a/feeds/group/2.0/{domain}/{group_id}/member/{membername}%40{domain}'/>
    <link rel='edit' type='application/atom+xml' href='https://apps-apis.google.com/a/feeds/group/2.0/{domain}/{group_id}/member/{membername}%40{domain}'/>
    <apps:property name='memberType' value='User'/>
    <apps:property name='memberId' value='{membername}@{domain}'/>
    <apps:property name='directMember' value='true'/>
</entry>"""

GROUP_OWNER_ENTRY = """<?xml version='1.0' encoding='UTF-8'?>
<entry xmlns='http://www.w3.org/2005/Atom' xmlns:apps='http://schemas.google.com/apps/2006'>
    <id>https://apps-apis.google.com/a/feeds/group/2.0/{domain}/{group_id}/owner/{owner_name}%40{domain}</id>
    <updated>2012-12-28T14:01:44.389Z</updated>
    <link rel='self' type='application/atom+xml' href='https://apps-apis.google.com/a/feeds/group/2.0/{domain}/{group_id}/owner/{owner_name}%40{domain}'/>
    <link rel='edit' type='application/atom+xml' href='https://apps-apis.google.com/a/feeds/group/2.0/{domain}/{group_id}/owner/{owner_name}%40{domain}'/>
    <apps:property name='email' value='{owner_name}@{domain}'/>
    <apps:property name='type' value='User'/>
</entry>
"""

OU_ENTRY = """<?xml version='1.0' encoding='UTF-8'?>
<entry xmlns='http://www.w3.org/2005/Atom' xmlns:apps='http://schemas.google.com/apps/2006'>
    <id>https://apps-apis.google.com/a/feeds/orgunit/2.0/{customer_id}/{ou_name_quote}</id>
    <updated>1970-01-01T00:00:00.000Z</updated>
    <link rel='self' type='application/atom+xml' href='https://apps-apis.google.com/a/feeds/orgunit/2.0/{customer_id}/{ou_name_quote}'/>
    <link rel='edit' type='application/atom+xml' href='https://apps-apis.google.com/a/feeds/orgunit/2.0/{customer_id}/{ou_name_quote}'/>
    <apps:property name='description' value='{description}'/>
    <apps:property name='parentOrgUnitPath' value='{ou_parent_path_quote}'/>
    <apps:property name='name' value='{ou_name}'/>
    <apps:property name='blockInheritance' value='{blockInheritance}'/>
</entry>"""

OU_USER_ENTRY = """<?xml version='1.0' encoding='UTF-8'?>
<entry xmlns='http://www.w3.org/2005/Atom' xmlns:apps='http://schemas.google.com/apps/2006'>
    <id>https://apps-apis.google.com/a/feeds/orguser/2.0/{customer_id}/{user_email_quoted}</id>
    <updated>1970-01-01T00:00:00.000Z</updated>
    <link rel='self' type='application/atom+xml' href='https://apps-apis.google.com/a/feeds/orguser/2.0/{customer_id}/{user_email_quoted}'/>
    <link rel='edit' type='application/atom+xml' href='https://apps-apis.google.com/a/feeds/orguser/2.0/{customer_id}/{user_email_quoted}'/>
    <apps:property name='oldOrgUnitPath' value='{old_ou_path_rel}' />
    <apps:property name='orgUnitPath' value='{new_ou_path_rel}' />
</entry>"""

NICKNAME_ENTRY = """<?xml version='1.0' encoding='UTF-8'?>
<entry xmlns='http://www.w3.org/2005/Atom' xmlns:apps='http://schemas.google.com/apps/2006'>
    <id>https://apps-apis.google.com/a/feeds/{domain}/nickname/2.0/{nickname}</id>
    <updated>1970-01-01T00:00:00.000Z</updated>
    <category scheme='http://schemas.google.com/g/2005#kind' term='http://schemas.google.com/apps/2006#nickname'/>
    <title type='text'>{nickname}</title>
    <link rel='self' type='application/atom+xml' href='https://apps-apis.google.com/a/feeds/{domain}/nickname/2.0/{nickname}'/>
    <link rel='edit' type='application/atom+xml' href='https://apps-apis.google.com/a/feeds/{domain}/nickname/2.0/{nickname}'/>
    <apps:nickname name='{nickname}'/>
    <apps:login userName='{user_name}'/>
</entry>
"""

USER_ENTRY_M = """<?xml version='1.0' encoding='UTF-8'?>
<entry xmlns='http://www.w3.org/2005/Atom' xmlns:apps='http://schemas.google.com/apps/2006'>
    <id>https://apps-apis.google.com/a/feeds/user/2.0/{mail_domain}/{user_name}%40{mail_domain}</id>
    <updated>1970-01-01T00:00:00.000Z</updated>
    <link rel='self' type='application/atom+xml' href='https://apps-apis.google.com/a/feeds/user/2.0/{mail_domain}/{user_name}%40{mail_domain}'/>
    <link rel='edit' type='application/atom+xml' href='https://apps-apis.google.com/a/feeds/user/2.0/{mail_domain}/{user_name}%40{mail_domain}'/>
    <apps:property name='password' value='{password}'/>
    <apps:property name='hashFunction' value='{hash_function_name}'/>
    <apps:property name='lastName' value='{sn}'/>
    <apps:property name='isChangePasswordAtNextLogin' value='{is_change_password}'/>
    <apps:property name='isSuspended' value='{is_suspended}'/>
    <apps:property name='userEmail' value='{user_name}@{mail_domain}'/>
    <apps:property name='isAdmin' value='{is_admin}'/>
    <apps:property name='firstName' value='{given_name}'/>
</entry>
"""

ALIAS_ENTRY_M = """<?xml version='1.0' encoding='UTF-8'?>
<entry xmlns='http://www.w3.org/2005/Atom' xmlns:apps='http://schemas.google.com/apps/2006'>
    <id>https://apps-apis.google.com/a/feeds/alias/2.0/{alias_domain}/{alias_name}%40{alias_domain}</id>
    <updated>1970-01-01T00:00:00.000Z</updated>
    <link rel='self' type='application/atom+xml' href='https://apps-apis.google.com/a/feeds/alias/2.0/{alias_domain}/{alias_name}%40{alias_domain}'/>
    <link rel='edit' type='application/atom+xml' href='https://apps-apis.google.com/a/feeds/alias/2.0/{alias_domain}/{alias_name}%40{alias_domain}'/>
    <apps:property name='aliasEmail' value='{alias_name}@{alias_domain}'/>
    <apps:property name='userEmail' value='{user_email}'/>
</entry>
"""
