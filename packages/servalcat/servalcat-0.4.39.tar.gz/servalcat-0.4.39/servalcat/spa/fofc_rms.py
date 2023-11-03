"""
Author: "Keitaro Yamashita, Garib N. Murshudov"
MRC Laboratory of Molecular Biology
    
This software is released under the
Mozilla Public License, version 2.0; see LICENSE.
"""
from __future__ import absolute_import, division, print_function, generators
import gemmi
import numpy
import scipy.optimize
from servalcat.utils import logger
from servalcat import utils
import argparse

def add_arguments(parser):
    parser.description = 'Fo-Fc map noise estimation'
    parser.add_argument('--fofc',
                        required=True,
                        help="MTZ file")
    parser.add_argument('-m', '--mask',
                        help="mask file")
# add_arguments()

def parse_args(arg_list):
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    return parser.parse_args(arg_list)
# parse_args()

def main(args):
    mask = gemmi.read_ccp4_map(args.mask).grid
# main()

if __name__ == "__main__":
    import sys
    args = parse_args(sys.argv[1:])
    main(args)
