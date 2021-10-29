# -*- coding: utf-8 -*-
import os
from pathlib import Path

from .dataframe import *
from .fstcomp import *
from .std_io import *

p = Path(os.path.abspath(__file__))
v_file = open(p.parent / 'VERSION')
__version__ = v_file.readline().strip()
v_file.close()
