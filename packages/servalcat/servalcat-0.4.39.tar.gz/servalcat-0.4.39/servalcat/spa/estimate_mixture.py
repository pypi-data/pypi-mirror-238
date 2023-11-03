"""
Author: "Keitaro Yamashita, Garib N. Murshudov"
MRC Laboratory of Molecular Biology
    
This software is released under the
Mozilla Public License, version 2.0; see LICENSE.
"""
from __future__ import absolute_import, division, print_function, generators
import gemmi
import numpy
import pandas
from servalcat.utils import logger
from servalcat import spa
from servalcat import utils

def add_arguments(parser):
    parser.description = 'Estimate parameters for pure and mixture data'

    parser.add_argument('--model', nargs="+", action="append",
                        required=True, 
                        help="")
    parser.add_argument('--map',
                        help='Input map file(s)')
    parser.add_argument("--halfmaps",  nargs=2)
    parser.add_argument('--pixel_size', type=float,
                        help='Override pixel size (A)')
    parser.add_argument('--mask', help='Mask file')
    parser.add_argument('-r', '--mask_radius',
                        type=float,
                        help='')
    parser.add_argument('-d', '--resolution',
                        type=float,
                        required=True,
                        help='')
    parser.add_argument('-o', '--fsc_out',
                        default="fsc.dat",
                        help='')
    parser.add_argument("--b_before_mask", type=float)
    parser.add_argument('--no_sharpen_before_mask', action='store_true',
                        help='By default half maps are sharpened before masking by std of signal and unsharpened after masking. This option disables it.')
# add_arguments()

def parse_args(arg_list):
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    return parser.parse_args(arg_list)
# parse_args()
