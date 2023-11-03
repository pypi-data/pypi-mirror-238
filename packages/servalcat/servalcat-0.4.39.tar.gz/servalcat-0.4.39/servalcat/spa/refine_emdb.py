"""
Author: "Keitaro Yamashita, Garib N. Murshudov"
MRC Laboratory of Molecular Biology
    
This software is released under the
Mozilla Public License, version 2.0; see LICENSE.
"""
def get_reso(model_in):
    doc = gemmi.cif.read(model_in)
    block = doc.sole_block()
    reso_str = block.find_value("_em_3d_reconstruction.resolution")
    return reso_str
# get_reso()
