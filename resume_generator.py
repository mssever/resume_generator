#!/usr/bin/env python3

'''
This program generates resumes. Given a master resume source, it can generate 
tailored resumes. That way, you can maintain only one resume and generate 
whichever versions you need. This greatly simplifies the resume creating 
process.
'''

import os
import sys

if sys.version_info.major >= 3 and sys.version_info.minor >= 6:
    import resgen.startup
    import resgen.config
    
    config = resgen.config.get_config()
    config.basedir = os.path.dirname(os.path.realpath(__file__))
    config.progname = sys.argv[0]
    with open(os.path.join(config.basedir, 'resgen', 'data', 'version.txt')) as f:
        config.version = f.read().strip()
    config.version_string = config.progname + ' ' + config.version
    sys.exit(resgen.startup.main())
else:
    sys.exit('ERROR: This program requires Python 3.6 or higher.\nCurrent Python:\t' + sys.version)
