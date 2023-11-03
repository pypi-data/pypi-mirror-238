"""
Author: "Keitaro Yamashita, Garib N. Murshudov"
MRC Laboratory of Molecular Biology
    
This software is released under the
Mozilla Public License, version 2.0; see LICENSE.
"""
from __future__ import absolute_import, division, print_function, generators
import gemmi
import numpy
import json
import os
import argparse
from servalcat.utils import logger
from servalcat import utils

def add_arguments(parser):
    parser.description = 'Run REFMAC5 for small molecule crystallography'
    parser.add_argument('--exe', default="refmac5", help='refmac5 binary')
    parser.add_argument('--cif', help="cif file containing model and data")
    parser.add_argument('--sg', help="Space group")
    parser.add_argument('--model', 
                        help='Input atomic model file')
    parser.add_argument('--hklin',
                        help='Input reflection file')
    parser.add_argument('--hklin_labs', nargs='+',
                        help='column names to be used')
    parser.add_argument('--blur', type=float,
                        help='Apply B-factor blurring to --hklin')
    parser.add_argument('--resolution',
                        type=float,
                        help='')
    parser.add_argument('--ligand', nargs="*", action="append",
                        help="restraint dictionary cif file(s)")
    parser.add_argument('--ncycle', type=int, default=10)
    #parser.add_argument('--jellybody', action='store_true')
    #parser.add_argument('--jellybody_params', nargs=2, type=float,
    #                    metavar=("sigma", "dmax"), default=[0.01, 4.2])
    parser.add_argument('--hydrogen', default="all", choices=["all", "yes", "no"],
                        help="all: add riding hydrogen atoms, yes: use hydrogen atoms if present, no: remove hydrogen atoms in input")
    parser.add_argument('--no_hout', action='store_true', help="do not write hydrogen atoms in the output model")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--weight_auto_scale', type=float,
                       help="'weight auto' scale value. automatically determined from resolution and mask/box volume ratio if unspecified")
    group.add_argument('--weight_matrix', type=float,
                       help="weight matrix value")
    parser.add_argument('--invert', action='store_true', help="invert handednes")
    parser.add_argument('--bref', choices=["aniso","iso","iso_then_aniso"], default="aniso")
    parser.add_argument('--unrestrained', action='store_true')
    parser.add_argument('--bulk_solvent', action='store_true')
    parser.add_argument('-s', '--source', choices=["electron", "xray", "neutron"], default="electron") #FIXME
    parser.add_argument('--keywords', nargs='+', action="append",
                        help="refmac keyword(s)")
    parser.add_argument('--keyword_file', nargs='+', action="append",
                        help="refmac keyword file(s)")
    parser.add_argument('--external_restraints_json')
    parser.add_argument('--show_refmac_log', action='store_true')
    parser.add_argument('--output_prefix', default="refined",
                        help='output file name prefix')
    parser.add_argument("--monlib",
                        help="Monomer library path. Default: $CLIBD_MON")
# add_arguments()
                        
def parse_args(arg_list):
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    return parser.parse_args(arg_list)
# parse_args()

def write_mtz(mtz_out, asudata, hklf, blur=None):
    data = numpy.hstack((asudata.miller_array,
                         asudata.value_array["value"][:,numpy.newaxis],
                         asudata.value_array["sigma"][:,numpy.newaxis]))
    mtz = gemmi.Mtz()
    mtz.spacegroup = asudata.spacegroup
    mtz.cell = asudata.unit_cell
    mtz.add_dataset('HKL_base')
    for label in ['H', 'K', 'L']: mtz.add_column(label, 'H')

    if hklf == 3:
        mtz.add_column("F", "F")
        mtz.add_column("SIGF", "Q")
    else:
        mtz.add_column("I", "J")
        mtz.add_column("SIGI", "Q")

    mtz.set_data(data)
    if blur is not None: utils.hkl.blur_mtz(mtz, blur)
    mtz.write_to_file(mtz_out)
# write_mtz()

def make_invert_tr(sg, cell):
    ops = sg.operations()
    coh = sg.change_of_hand_op()
    ops.change_basis_forward(sg.change_of_hand_op())
    new_sg = gemmi.find_spacegroup_by_ops(ops)
    tr = cell.op_as_transform(coh)
    return new_sg, tr
# make_invert_tr()
    
def main(args):
    if not args.cif and not (args.model and args.hklin):
        raise SystemExit("Give [--model and --hklin] or --cif")

    if args.sg:
        try:
            sg_user = gemmi.SpaceGroup(args.sg)
            logger.writeln("User-specified space group: {}".format(sg_user.xhm()))
        except ValueError:
            raise SystemExit("Error: Unknown space group '{}'".format(args.sg))
    else:
        sg_user = None

    mtz_in = "input.mtz" # always write this file as an input for Refmac
    if args.cif:
        asudata, ss, info = utils.fileio.read_smcif_shelx(args.cif)
        st = utils.model.cx_to_mx(ss)
        if sg_user:
            if not asudata.unit_cell.is_compatible_with_spacegroup(sg_user):
                raise SystemExit("Error: Specified space group {} is incompatible with the unit cell parameters {}".format(sg_user.xhm(),
                                                                                                                           asudata.unit_cell.parameters))
            
            asudata.spacegroup = sg_user
        write_mtz(mtz_in, asudata, info.get("hklf"), args.blur)
    else:
        st = utils.fileio.read_structure(args.model)
        sg_st = st.find_spacegroup()
        if utils.fileio.is_mmhkl_file(args.hklin): # TODO may be unmerged mtz
            mtz = utils.fileio.read_mmhkl(args.hklin)
            if not mtz.cell.approx(st.cell, 1e-3):
                logger.writeln(" Warning: unit cell mismatch!")
            if sg_user:
                if not mtz.cell.is_compatible_with_spacegroup(sg_user):
                    raise SystemExit("Error: Specified space group {} is incompatible with the unit cell parameters {}".format(sg_user.xhm(),
                                                                                                                               mtz.cell.parameters))
                mtz.spacegroup = sg_user
                logger.writeln(" Writing {} as space group {}".format(mtz_in, sg_user.xhm()))
            elif mtz.spacegroup != sg_st:
                logger.writeln(" Warning: space group mismatch between model and mtz")
                if mtz.cell.is_compatible_with_spacegroup(sg_st):
                    logger.writeln("  Taking space group from model.")
                    mtz.spacegroup = sg_st
                    logger.writeln("  Writing {} as space group {}".format(mtz_in, sg_st.xhm()))
                else:
                    logger.writeln("  Model space group is incompatible with mtz unit cell. Ignoring model space group.")

            if args.hklin_labs:
                try: mtz = utils.hkl.mtz_selected(mtz, args.hklin_labs)
                except RuntimeError as e:
                    raise SystemExit("Error: {}".format(e))
            if args.blur is not None: utils.hkl.blur_mtz(mtz, args.blur)
            mtz.write_to_file(mtz_in)
            st.cell = mtz.cell
            st.spacegroup_hm = mtz.spacegroup.xhm()
        elif args.hklin.endswith(".hkl"):
            asudata, hklf = utils.fileio.read_smcif_hkl(args.hklin, st.cell, sg_st)
            # TODO check consistency with model cell and sg
            write_mtz(mtz_in, asudata, hklf, args.blur)
            st.cell = asudata.unit_cell
            st.spacegroup_hm = asudata.spacegroup.xhm()
        else:
            raise SystemExit("Error: unsupported hkl file: {}".format(args.hklin))

    if args.invert:
        logger.writeln("Inversion of structure is requested.")
        old_sg = st.find_spacegroup()
        new_sg, tr = make_invert_tr(old_sg, st.cell)
        logger.writeln(" new space group = {} (no. {})".format(new_sg.xhm(), new_sg.number))
        st[0].transform_pos_and_adp(tr)
        if old_sg != new_sg:
            st.spacegroup_hm = new_sg.xhm()
            # overwrite mtz
            mtz = gemmi.read_mtz_file(mtz_in)
            mtz.spacegroup = new_sg
            mtz.write_to_file(mtz_in)

    if args.keyword_file:
        args.keyword_file = sum(args.keyword_file, [])
        for f in args.keyword_file:
            logger.writeln("Keyword file: {}".format(f))
            assert os.path.exists(f)
    else:
        args.keyword_file = []
            
    if args.keywords:
        args.keywords = sum(args.keywords, [])
    else:
        args.keywords = []

    for m in st:
        for chain in m:
            # Fix if they are blank TODO if more than one chain/residue?
            if chain.name == "": chain.name = "A"
            for res in chain:
                if res.name == "": res.name = "00"

    # FIXME in some cases mtz space group should be modified. 
    utils.fileio.write_model(st, prefix="input", pdb=True, cif=True)

    if args.ligand: args.ligand = sum(args.ligand, [])

    prefix = "refined"
    if args.bref == "aniso":
        args.keywords.append("refi bref aniso")
    elif args.bref == "iso_then_aniso":
        prefix = "refined_1_iso"
        
    if args.unrestrained:
        args.keywords.append("refi type unre")
        args.no_hout = False
    else:
        monlib = utils.restraints.load_monomer_library(st, monomer_dir=args.monlib, cif_files=args.ligand, 
                                                       stop_for_unknowns=False)

    # no bulk solvent by default
    if not args.bulk_solvent:
        args.keywords.append("solvent no")

    # Run Refmac
    refmac = utils.refmac.Refmac(prefix=prefix, global_mode="cx",
                                 exe=args.exe,
                                 source=args.source,
                                 monlib_path=args.monlib,
                                 xyzin="input.mmcif",
                                 hklin=mtz_in,
                                 ncycle=args.ncycle,
                                 weight_matrix=args.weight_matrix,
                                 weight_auto_scale=args.weight_auto_scale,
                                 hydrogen=args.hydrogen,
                                 hout=not args.no_hout,
                                 resolution=args.resolution,
                                 keyword_files=args.keyword_file,
                                 keywords=args.keywords)
    refmac.set_libin(args.ligand)
    refmac_summary = refmac.run_refmac()

    if args.bref == "iso_then_aniso":
        refmac2 = refmac.copy(xyzin=prefix+".mmcif",
                              prefix="refined_2_aniso")
        refmac2.keywords.append("refi bref aniso")
        refmac_summary = refmac2.run_refmac()

if __name__ == "__main__":
    import sys
    args = parse_args(sys.argv[1:])
    main(args)

