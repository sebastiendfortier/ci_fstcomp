#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CLI application that compares 2 fst files.    

Example::    
    
  ci_fstcomp -a file 1 -b file2    
    

"""
import argparse
import csv
import logging
import sys
from typing import TextIO

from ci_fstcomp import fstcomp

try:
    # Python2
    from StringIO import StringIO
except ImportError:
    # Python3
    from io import StringIO


def make_list(csv_str):
    if csv_str != "":
        f = StringIO(csv_str)
        reader = csv.reader(f, delimiter=',')
        column_list = []
        [column_list.append(row) for row in reader]
        return column_list[0]
    return []


def cli():

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-a', type=str, required=True, help='path to file a')
    parser.add_argument('-b', type=str, required=True, help='path to file b')
    # parser.add_argument('--ignore', type=str, default="", help='columns to ignore as csv, ex.: --ignore "etiket,ip1"')
    parser.add_argument('--c-cor-thr', type=float, default=.0000001,
                        help='corelation error threshold (default: .0000001)')
    parser.add_argument('--e-max-thr', type=float, default=.0000001,
                        help='relative error threshold (default: .0000001)')
    parser.add_argument('--exclude_meta', type=bool, default=False, help='exclude meta data fields from comparison')
    parser.add_argument('--cmp_number_of_fields', type=bool, default=False,
                        help='compare the number of fields in each file')
    parser.add_argument('--log_level', type=int, default=logging.INFO, help='set logging level, default logging.INFO')
    parser.add_argument('--log_stream', type=TextIO, default=sys.stdout, help='set logging stream, default sys.stdout')

    args = parser.parse_args()

    logging.basicConfig(level=args.log_level, stream=args.log_stream)

    logging.debug('ci_fstcomp -a %s -b %s' % (args.a, args.b))

    status = 0  # in error

    # base_columns=['nomvar', 'etiket', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4']
    # new_list = [item for item in base_columns if item not in ignore_items]
    # columns_to_consider = new_list

    # status = ci_fstcomp(file1:args.a, file2:args.b, exclude_meta=args.exclude_meta, cmp_number_of_fields=args.cmp_num_fields, ignore=ignore_items,columns=columns_to_consider, verbose=False, e_max=args.e_max_thr1, e_c_cor=args.c_cor_thr)
    status = fstcomp(file1=args.a, file2=args.b, exclude_meta=args.exclude_meta,
                     cmp_number_of_fields=args.cmp_number_of_fields, verbose=False, e_max=args.e_max_thr, e_c_cor=args.c_cor_thr)

    # reverse status for ci
    return not(status)


if __name__ == '__main__':
    exit(cli())
