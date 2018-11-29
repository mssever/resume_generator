#!/usr/local/env python3

import sys

if sys.version_info.major >= 3 and sys.version_info.minor >= 6:
    import resume_generator.startup
    sys.exit(resume_generator.startup.main())
else:
    sys.exit('This program requires Python 3.6 or higher.\nCurrent Python:\t' + sys.version)
