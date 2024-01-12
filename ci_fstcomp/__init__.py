# -*- coding: utf-8 -*-
import os
import pkg_resources
from pathlib import Path

from .dataframe import *
from .fstcomp import *
from .std_io import *

def _get_version():
   try:
       version = pkg_resources.resource_string('ci_fstcomp', 'VERSION').decode('utf-8').strip()
   except IOError:
       version = 'unknown'
   return version

__version__ = _get_version()
