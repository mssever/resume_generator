#!/usr/local/env python3

'''
This program generates résumés. Given a master résumé source, it can generate
tailored résumés. That way, you can maintain only one résumé and generate
whichever versions you need. This greatly simplifies the résumé creating
process.
'''

import os
import sys

if sys.version_info.major >= 3 and sys.version_info.minor >= 6:
    import resgen.startup
    import resgen.config
    
    config = resgen.config.get_config()
    config.basedir = os.path.dirname(os.path.realpath(__file__))
    sys.exit(resgen.startup.main())
else:
    sys.exit('This program requires Python 3.6 or higher.{sep}Current Python:\t{ver}'.format(sep=os.linesep, ver=sys.version))
