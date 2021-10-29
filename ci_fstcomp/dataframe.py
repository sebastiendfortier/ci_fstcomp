# -*- coding: utf-8 -*-
import pandas as pd


def clean_dataframe(df):
    df = remove_deleted_records(df)
    df = remove_unwanted_columns(df)
    df = df.sort_values(['nomvar', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'datev', 'datyp', 'nbits'])
    return df


def remove_unwanted_columns(df):
    columns_to_keep = ['nomvar', 'typvar', 'etiket', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2',
                       'ip3', 'deet', 'npas', 'datyp', 'nbits', 'grtyp', 'ig1', 'ig2', 'ig3',
                       'ig4', 'datev', 'd', 'path', 'key']
    df = df[columns_to_keep]
    return df


def remove_deleted_records(df):
    if 'dltf' in df.columns:
        df = df.query('dltf == 0')
        df = df.drop(columns=['dltf'], errors='ignore')
    return df


def strip_string_values(df):
    df['nomvar'] = df['nomvar'].str.strip()
    df['etiket'] = df['etiket'].str.strip()
    df['typvar'] = df['typvar'].str.strip()
    df['grtyp'] = df['grtyp'].str.strip()
    return df


def del_fstcomp_columns(diff: pd.DataFrame) -> pd.DataFrame:
    # diff.drop(columns=['abs_diff'], inplace=True,errors='ignore')
    diff.drop(columns=['success'], inplace=True, errors='ignore')
    return diff


def add_fstcomp_columns(diff: pd.DataFrame) -> pd.DataFrame:
    # diff['abs_diff'] = None# = diff['d_x'].copy(deep=True)
    diff['e_rel_max'] = None  # = diff['d_x'].copy(deep=True)
    diff['e_rel_moy'] = None  # = diff['d_x'].copy(deep=True)
    diff['var_a'] = None  # = diff['d_x'].copy(deep=True)
    diff['var_b'] = None  # = diff['d_x'].copy(deep=True)
    diff['c_cor'] = None  # = diff['d_x'].copy(deep=True)
    diff['moy_a'] = None  # = diff['d_x'].copy(deep=True)
    diff['moy_b'] = None  # = diff['d_x'].copy(deep=True)
    diff['bias'] = None  # = diff['d_x'].copy(deep=True)
    diff['e_max'] = None  # = diff['d_x'].copy(deep=True)
    diff['e_moy'] = None  # = diff['d_x'].copy(deep=True)
    diff['success'] = None
    # diff.drop(columns=['d_x', 'd_y'], inplace=True,errors='ignore')
    return diff


def remove_meta_data_fields(df: pd.DataFrame) -> pd.DataFrame:
    df.drop(df[df.nomvar.isin(["^>", ">>", "^^", "!!", "!!SF", "HY", "P0", "PT", "E1", "PN"])].index,
            inplace=True, errors='ignore')
    return df
