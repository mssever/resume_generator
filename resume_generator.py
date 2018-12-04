#!/usr/bin/env python3
#-*- coding: utf-8 -*-

'''
This program generates résumés. Given a master résumé source, it can generate
tailored résumés. That way, you can maintain only one résumé and generate
whichever versions you need. This greatly simplifies the résumé creating
process.
'''

import os
import sys

ver = sys.version_info
if ver.major > 3 or (ver.major == 3 and ver.minor >= 6):
    import resgen.startup
    import resgen.config
    
    config = resgen.config.get_config()
    config.basedir = os.path.dirname(os.path.realpath(__file__))
    exit(resgen.startup.main())
else:
    exit('ERROR: This program requires Python 3.6 or higher.{sep}Current Python:\t{ver}'.format(sep=os.linesep, ver=sys.version))
