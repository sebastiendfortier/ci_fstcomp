# -*- coding: utf-8 -*-
import logging
from .dataframe import clean_dataframe, strip_string_values
try:
    import rpnpy.librmn.all as rmn
except ImportError as e:
    logging.critical("Could not import rpnpy.librmn.all (" + str(e) +
                     "), this package is only available through the environment via PYTHONPATH set by doing an . r.load.dot:")
    logging.critical("'. r.load.dot eccc/mrd/rpn/MIG/ENV/migdep/5.1.1 eccc/mrd/rpn/MIG/ENV/rpnpy/2.1.2'")
    import sys
    sys.exit(1)

import logging
import pandas as pd
import os
rmn.fstopt(rmn.FSTOP_MSGLVL, rmn.FSTOPI_MSG_CATAST, setOget=0)


def get_dataframe(path):
    if os.path.isfile(path):
        if maybeFST(path):
            file_id = rmn.fstopenall(path, rmn.FST_RO)
            keys = rmn.fstinl(file_id)
            records = [rmn.fstprm(key) for key in keys]

            df = pd.DataFrame(records)
            df = strip_string_values(df)
            df['d'] = None
            df['path'] = path
            # for i in df.index:
            #   df.at[i,'d'] = rmn.fstluk(int(df.at[i,'key']))['d']
            rmn.fstcloseall(file_id)
            df = clean_dataframe(df)
            return df

    logging.error('invalid file: %s' % path)
    return pd.DataFrame(dtype=object)


def maybeFST(filename):
    with open(filename, 'rb') as f:
        buf = f.read(16)
        if len(buf) < 16:
            return False
        # Same check as c_wkoffit in librmn
        return buf[12:] == b'STDR'


def load_data(path, df, x=False):
    iun = rmn.fstopenall(path)
    for i in df.index:
        if x:
            df.at[i, 'd_x'] = rmn.fstluk(int(df.at[i, 'key_x']))['d']
        else:
            df.at[i, 'd_y'] = rmn.fstluk(int(df.at[i, 'key_y']))['d']
    rmn.fstcloseall(iun)
    return df
