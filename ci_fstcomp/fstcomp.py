# -*- coding: utf-8 -*-

import logging
import math
import os

import numpy as np
import pandas as pd

from .dataframe import add_fstcomp_columns, del_fstcomp_columns, remove_meta_data_fields

from .std_io import get_dataframe, load_data


class FstCompError(Exception):
    pass


def fstcomp(file1: str, file2: str, exclude_meta=False, cmp_number_of_fields=True, columns=['nomvar', 'etiket', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4'], verbose=False, e_max=0.0001, e_c_cor=0.00001) -> bool:
    """Utility used to compare the contents of two RPN standard files (record by record).

    :param file1: path to file 1
    :type file1: str
    :param file2: path to file 2
    :type file2: str
    :param columns: columns to be considered, defaults to ['nomvar', 'etiket', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4']
    :type columns: list, optional
    :param verbose: if activated prints more information, defaults to False
    :type verbose: bool, optional
    :raises StandardFileError: type of error that will be raised
    :return: True if files are sufficiently similar else False
    :rtype: bool
    """
    logging.info('ci_fstcomp -a %s -b %s' % (file1, file2))

    if not os.path.exists(file1):
        raise FstCompError('ci_fstcomp - %s does not exist' % file1)
    if not os.path.exists(file2):
        raise FstCompError('ci_fstcomp - %s does not exist' % file2)
    # open and read files
    df1 = get_dataframe(file1)
    df2 = get_dataframe(file2)

    return fstcomp_df(df1, df2, exclude_meta, cmp_number_of_fields, columns, print_unmatched=verbose, e_max=e_max, e_c_cor=e_c_cor)


def fstcomp_df(df1: pd.DataFrame, df2: pd.DataFrame, exclude_meta=False, cmp_number_of_fields=True, columns=['nomvar', 'etiket', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4'], print_unmatched=False, e_max=0.0001, e_c_cor=0.00001) -> bool:
    path1 = df1.path.unique()[0]
    path2 = df2.path.unique()[0]

    columns_to_keep = columns.copy()
    columns_to_keep.extend(['d', 'key'])
    df1 = df1[columns_to_keep]
    df2 = df2[columns_to_keep]

    df1 = df1.sort_values(by=columns)
    df2 = df2.sort_values(by=columns)

    success = True
    pd.options.display.float_format = '{:0.6E}'.format
    # check if both df have records
    if df1.empty or df2.empty:
        logging.error('you must supply files witch contain records')
        if df1.empty:
            logging.error('file 1 is empty')
        if df2.empty:
            logging.error('file 2 is empty')
        raise FstCompError('ci_fstcomp - one of the files is empty')

    if exclude_meta:
        df1 = remove_meta_data_fields(df1)
        df2 = remove_meta_data_fields(df2)

    if cmp_number_of_fields:
        if len(df1.index) != len(df2.index):
            logging.error('file 1 (%s) and file 2 (%s) dont have the same number of records' %
                          (len(df1.index), len(df2.index)))
            unique1, counts1 = np.unique(df1.nomvar.to_numpy(), return_counts=True)
            unique2, counts2 = np.unique(df2.nomvar.to_numpy(), return_counts=True)
            vars1 = dict(zip(unique1, counts1))
            vars2 = dict(zip(unique2, counts2))
            logging.error('file 1 %s' % vars1)
            logging.error('file 2 %s' % vars2)
            return False
    # create common fields
    if print_unmatched:
        logging.debug('\n%s' % df1[['nomvar', 'etiket', 'ni', 'nj', 'nk', 'dateo']])
        logging.debug('\n%s' % df2[['nomvar', 'etiket', 'ni', 'nj', 'nk', 'dateo']])
        logging.debug('\n%s' % df1[['ip1', 'ip2', 'ip3', 'deet', 'npas']])
        logging.debug('\n%s' % df2[['ip1', 'ip2', 'ip3', 'deet', 'npas']])
        logging.debug('\n%s' % df1[['grtyp', 'ig1', 'ig2', 'ig3', 'ig4']])
        logging.debug('\n%s' % df2[['grtyp', 'ig1', 'ig2', 'ig3', 'ig4']])

    common = pd.merge(df1, df2, how='inner', on=columns)
    # Rows in df1 Which Are Not Available in df2
    common_with_1 = common.merge(df1, how='outer', indicator=True).loc[lambda x: x['_merge'] == 'left_only']
    # Rows in df2 Which Are Not Available in df1
    common_with_2 = common.merge(df2, how='outer', indicator=True).loc[lambda x: x['_merge'] == 'right_only']

    missing = pd.concat([common_with_1, common_with_2], ignore_index=True)

    if exclude_meta:
        missing = remove_meta_data_fields(missing)

    if len(common.index) != 0:
        if len(common_with_1.index) != 0:
            if print_unmatched:
                logging.error('df in file 1 that were not found in file 2 - excluded from comparison')
                logging.error('\n%s' % common_with_1.to_string())
        if len(common_with_2.index) != 0:
            if print_unmatched:
                logging.error('df in file 2 that were not found in file 1 - excluded from comparison')
                logging.error('\n%s' % common_with_2.to_string())
    else:
        logging.error('ci_fstcomp - no common df to compare')
        if not df1.empty:
            logging.error('A \n%s' % df1[['nomvar', 'etiket', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3',
                          'deet', 'npas', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4']].reset_index(drop=True).to_string())
        logging.info('----------')
        if not df2.empty:
            logging.error('B \n%s' % df2[['nomvar', 'etiket', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3',
                          'deet', 'npas', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4']].reset_index(drop=True).to_string())
        raise FstCompError('ci_fstcomp - no common df to compare')

    # force free some memory
    del df1
    del df2

    diff = common

    # Sort by key to speed up reading of the first file.
    diff = diff.sort_values(by='key_x')

    diff = add_fstcomp_columns(diff)

    diff, success = compute_fstcomp_stats(diff, path1, path2, e_max, e_c_cor)

    diff = diff.loc[(diff.c_cor != -1.) & (diff.nomvar.str.startswith('<'))]

    diff = del_fstcomp_columns(diff)

    if len(diff.index):
        logging.info('\n%s' % diff[['nomvar', 'etiket', 'ip1', 'ip2', 'ip3', 'e_rel_max', 'e_rel_moy', 'var_a', 'var_b', 'c_cor', 'moy_a',
                     'moy_b', 'bias', 'e_max', 'e_moy']].to_string(formatters={'level': '{:,.6f}'.format, 'diff_percent': '{:,.1f}%'.format}))

    if len(missing.index):
        logging.error('missing df')
        logging.error('\n%s' % missing[['nomvar', 'etiket', 'ip1', 'ip2', 'ip3']].to_string(
            header=False, formatters={'level': '{:,.6f}'.format}))
        return False

    return success


def compute_fstcomp_stats(diff: pd.DataFrame, path1: str, path2: str, e_max=0.0001, e_c_cor=0.00001) -> bool:
    success = True

    df_list = np.array_split(diff, math.ceil(len(diff.index)/100))
    for df in df_list:
        load_data(path1, df, x=True)
        load_data(path2, df)

        if logging.root.level <= logging.DEBUG:
            logging.debug('diff dx\n%s' % df[['nomvar', 'd_x']])
            logging.debug('diff dy\n%s' % df[['nomvar', 'd_y']])

        vstats = np.vectorize(stats, otypes=['float32', 'float32', 'float32', 'float32',
                              'float32', 'float32', 'float32', 'float32', 'float32', 'float32', 'str', 'bool'])

        df['e_rel_max'], df['e_rel_moy'], df['var_a'], df['var_b'], df['c_cor'], df['moy_a'], df['moy_b'], df['bias'], df['e_max'], df['e_moy'], df['nomvar'], df['success'] = vstats(
            df['d_x'].values, df['d_y'].values, df['nomvar'].values, np.full_like(df['nomvar'], e_c_cor, dtype='float32'), np.full_like(df['nomvar'], e_max, dtype='float32'))

        df['d_x'] = None
        df['d_y'] = None

    diff = pd.concat(df_list, ignore_index=True)

    return diff, df.loc[df.success == False].empty


def stats(a, b, nomvar, e_c_cor, e_max):
    success = True
    new_nomvar = nomvar

    if np.allclose(a, b):
        return 0., 0., 0., 0., -1., 0., 0., 0., 0., 0., new_nomvar, success

    errabs = np.abs(a-b)
    errmoy = np.mean(errabs)

    errmax = np.max(errabs)

    derr = np.where(a != 0., np.abs(1.-b/a), np.where(b != 0., np.abs(1.-a/b), 0.))
    derr = np.where(derr < 0., 0., derr)

    errrelmax = np.max(derr)

    errrelmoy = np.mean(derr)

    moya = np.sum(a)/a.size
    moyb = np.sum(b)/a.size

    aa = a-moya
    bb = b-moyb
    ccor = np.sum(aa * bb)

    bias = moyb-moya

    sa2 = np.sum(aa**2)
    sb2 = np.sum(bb**2)

    vara = sa2/a.size
    varb = sb2/a.size

    if (sa2*sb2 != 0.):
        ccor = ccor/np.sqrt(sa2*sb2)
    elif (sa2 == 0. and sb2 == 0.):
        ccor = 1.0
    elif (sa2 == 0.):
        ccor = np.sqrt(varb)
    else:
        ccor = np.sqrt(vara)

    if (not (-e_c_cor <= abs(ccor-1.0) <= e_c_cor)) or (not (-e_max <= errmax <= e_max)):
        new_nomvar = ''.join(['<', nomvar, '>'])
        success = False

    return errrelmax, errrelmoy, vara, varb, ccor, moya, moyb, bias, errmax, errmoy, new_nomvar, success
