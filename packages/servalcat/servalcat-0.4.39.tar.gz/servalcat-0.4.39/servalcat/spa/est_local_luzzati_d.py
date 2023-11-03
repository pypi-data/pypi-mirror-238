"""
Author: "Keitaro Yamashita, Garib N. Murshudov"
MRC Laboratory of Molecular Biology
    
This software is released under the
Mozilla Public License, version 2.0; see LICENSE.
"""
from __future__ import absolute_import, division, print_function, generators
import gemmi
import numpy
import scipy.special
import time
from servalcat.utils import logger
from servalcat import utils
import argparse

def add_arguments(parser):
    parser.description = ""
    #parser.add_argument("--halfmaps", nargs=2)
    parser.add_argument('--model', required=True,
                        help='Input atomic model file (PDB or mmCIF/PDBx')
    parser.add_argument("--mrc_b", required=True)
    parser.add_argument("--mrc_rcc", required=True)
    parser.add_argument("--mrc_mcc", required=True)
# add_arguments()

fp = lambda B,smax: 4*numpy.pi*(numpy.sqrt(numpy.pi/2)*scipy.special.erf(numpy.sqrt(B/2)*smax)-smax*numpy.sqrt(B)*numpy.exp(-B*smax**2/2))/B**(3/2)
w = lambda z: numpy.exp(-z**2)*(1-1j*scipy.special.erfi(-z))
fn = lambda B,smax: 4*numpy.pi*numpy.exp(-B*smax**2/2) * (smax*numpy.sqrt(-B)-numpy.sqrt(numpy.pi/2)*numpy.imag(w(numpy.sqrt(-B/2)*smax)))/(-B)**(3/2)

def make_table(smax):
    Bn = numpy.arange(-300,0)
    cn = fn(Bn, smax)
    Bp = numpy.arange(1, 600)
    cp = fp(Bp, smax)

    Bs = numpy.concatenate((Bn, Bp))
    cs = numpy.concatenate((cn, cp))
    order = numpy.argsort(cs)
    Bs, cs = Bs[order], cs[order]

    return Bs, cs
# make_table()

def estimate_error_as_b(st, b_grid, rcc_grid, mcc_grid, smax):
    """
    b_grid: estimated B values (from half map correlation)
    rcc_grid: half map correlation
    mcc_grid: model-map correlation    
    """
    
    b_grid = numpy.array(b_grid)
    rcc_grid = numpy.array(rcc_grid)
    mcc_grid = numpy.array(mcc_grid)
    
    rcc_grid = 2*rcc_grid/(rcc_grid+1) # to full map correlation
    cc_ratio = mcc_grid/rcc_grid

    intb_grid = numpy.empty_like(b_grid)
    intb_grid[b_grid<0] = fn(b_grid[b_grid<0], smax)
    intb_grid[b_grid==0] = 4./3.*numpy.pi*smax**3
    intb_grid[b_grid>0] = fp(b_grid[b_grid>0], smax)

    Bs, cs = make_table(smax)
    B_sum = numpy.interp(cc_ratio*intb_grid, cs, Bs)
    B_error = (B_sum - b_grid) * 2
    B_error = gemmi.FloatGrid(B_error.astype(numpy.float32), st.cell, st.find_spacegroup())
    B_fromcc= gemmi.FloatGrid(b_grid.astype(numpy.float32), st.cell, st.find_spacegroup())
    ccfull  = gemmi.FloatGrid(rcc_grid.astype(numpy.float32), st.cell, st.find_spacegroup())
    ccmodel = gemmi.FloatGrid(mcc_grid.astype(numpy.float32), st.cell, st.find_spacegroup())

    ofs = open("values.dat", "w")
    ofs.write("chain resi resn atom b_iso b_err b_est ccfull ccmodel\n")
    for cra in st[0].all():
        b_err = B_error.interpolate_value(cra.atom.pos)
        b_est = B_fromcc.interpolate_value(cra.atom.pos)
        ccfull_interp = ccfull.interpolate_value(cra.atom.pos)
        ccmodel_interp = ccmodel.interpolate_value(cra.atom.pos)
        ofs.write("{} {} {} {} ".format(cra.chain.name, cra.residue.seqid.num, cra.residue.name, cra.atom.name))
        ofs.write("{:.2f} {:.2f} {:.2f} {:.4f} {:.4f}\n".format(cra.atom.b_iso, b_err, b_est, ccfull_interp, ccmodel_interp))
        cra.atom.b_iso = b_err

    utils.fileio.write_pdb(st, "b_error.pdb")
    utils.fileio.write_mmcif(st, "b_error.mmcif")

    st2 = st.clone()
    for cra in st2[0].all():
        b_err = B_error.interpolate_value(cra.atom.pos)
        cra.atom.b_iso += b_err

    utils.fileio.write_mmcif(st, "b_error_added.mmcif")

    return B_error
# estimate_error_as_b()

def main(args):
    st = utils.fileio.read_structure(args.model)
    b_grid, _ = utils.fileio.read_ccp4_map(args.mrc_b)
    rcc_grid, _ = utils.fileio.read_ccp4_map(args.mrc_rcc)
    mcc_grid, _ = utils.fileio.read_ccp4_map(args.mrc_mcc)
    
    estimate_error_as_b(st, b_grid, rcc_grid, mcc_grid, 1./args.resolution)
# main()

if __name__ == "__main__":
    import sys
    args = parse_args(sys.argv[1:])
    main(args)
