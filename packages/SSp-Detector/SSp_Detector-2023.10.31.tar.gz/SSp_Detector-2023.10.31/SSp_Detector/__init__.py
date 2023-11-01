import logging
import os
from .ssp_detector import *
from outdated import warn_if_outdated
path=os.path.abspath(os.path.dirname(__name__))

#Define logger
logging.basicConfig(format='%(asctime)s|%(levelname)s|%(message)',datefmt='%y-%b-%d %H:%M:%S')

__author__='Simon J. Guillot <simon.guillot@inserm.fr>'
DISTNAME='SSp_Detector'
VERSION=''
if not VERSION:
    pr=DISTNAME.lower().replace("-","_").replace(" ","_")
    with open(os.path.join(path,pr,pr,'__version__.py')) as v:
        VERSION='\n'+v.read()
else:
    VERSION=VERSION
__version__=VERSION

#Warn if newer version is available
warn_if_outdated('SSp_Detector',__version__)
