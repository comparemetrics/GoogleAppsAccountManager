#
# GoogleAppsAccountManager: display
# Copyright (C) 2012-2013 KAMEI Yutaka
#
# License: GNU General Public License version 2 or later
# Date: 2012-12-28, since 2012-12-28
#

import sys

class Display(object):
    header_already_out_flag = False

    def display(self, *header, **header_val):
        if not self.header_already_out_flag:
            field = "{0}\n".format(",".join(header))
            sys.stdout.write(field)
            self.header_already_out_flag = True
    
        field = "{0}\n".format(",".join(map(lambda x: str(header_val[x]), header)))
        sys.stdout.write(field)
        sys.stdout.flush()
