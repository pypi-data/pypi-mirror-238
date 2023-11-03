"""
Author: "Keitaro Yamashita, Garib N. Murshudov"
MRC Laboratory of Molecular Biology
    
This software is released under the
Mozilla Public License, version 2.0; see LICENSE.
"""
from __future__ import absolute_import, division, print_function, generators
import gemmi
from servalcat import utils

def run(model_in, refmac_mtz):
    st, _ = utils.fileio.read_structure_from_pdb_and_mmcif(model_in)
    st.expand_ncs(gemmi.HowToNameCopiedChain.Short)
    monlib = None
    
    m = gemmi.read_mtz_file(refmac_mtz)
    d_min = m.resolution_high()
    fc = m.get_f_phi("FC", "PHIC")
    fc_all = m.get_f_phi("FC_ALL", "PHIC_ALL")
    fc_all_ls = m.get_f_phi("FC_ALL_LS", "PHIC_ALL_LS")

    myfc = utils.model.calc_fc_fft(st, d_min, cutoff=1e-7, monlib=monlib, source="electron")
    hkldata = utils.hkl.HklData(m.cell, m.spacegroup, utils.hkl.df_from_asu_data(myfc, "FCserval"))
    hkldata.merge_asu_data(fc, "FCrefmac")
    
# run()
    

if __name__ == "__main__":
    import sys
    
    model_in = sys.argv[1]
    refmac_mtz = sys.argv[2]
    run(model_in, refmac_mtz)
