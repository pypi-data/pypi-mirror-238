"""
Author: "Keitaro Yamashita, Garib N. Murshudov"
MRC Laboratory of Molecular Biology
    
This software is released under the
Mozilla Public License, version 2.0; see LICENSE.
"""
from __future__ import absolute_import, division, print_function, generators
import gemmi
import numpy
from servalcat import utils

def add_arguments(parser):
    parser.description = 'Find translation for a model'
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--halfmaps", nargs=2, help="Input half map files")
    group.add_argument("--map")
    parser.add_argument('--pixel_size', type=float,
                        help='Override pixel size (A)')
    parser.add_argument("-d", '--resolution', type=float, required=True)
    parser.add_argument('-m', '--mask', help="mask file")
    parser.add_argument('-o','--output_prefix',
                        help='output file name prefix')
# add_arguments()
                        
def parse_args(arg_list):
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    return parser.parse_args(arg_list)
# parse_args()

def find_translation(st, maps, d_min):
    fc_asu = utils.model.calc_fc_fft(st, d_min, r_cut=1e-7, source="electron")
    fo_asu = gemmi.transform_map_to_f_phi(m).prepare_asu_data(dmin=d_min)

    assert numpy.all(fc_asu.miller_array == fo_asu.miller_array)

    fo_asu.value_array[:] = fo_asu.value_array * numpy.conj(fc_asu.value_array)
    gr = fo_asu.transform_f_phi_to_map(exact_size=m.shape)
    utils.maps.write_ccp4_map("fofcstar.mrc", gr)
# find_translation()

def main(args):
    m, _ = utils.fileio.read_ccp4_map("../full_map_cropped.mrc")

    st = gemmi.read_structure("../overlayResults.pdb")
    st.cell = m.unit_cell
    st.spacegroup_hm = "P 1"

    
# main()


if __name__ == "__main__":
    import sys
    args = parse_args(sys.argv[1:])
    main(args)

