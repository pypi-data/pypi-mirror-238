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
import argparse
from servalcat.utils import logger
from servalcat import spa
from servalcat import utils

"""
library(ggplot2)
library(reshape2)
d=read.csv("./tst.csv")
ggplot(melt(d, id=c("X","d_min","d_max")), aes(x=X, y=value, col=variable)) + geom_line()
"""

def add_arguments(parser):
    parser.description = 'FSC calculation'

    parser.add_argument('--model',
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
                        help='Default: Nyquist')
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

def fsc_average(n, fsc):
    sel = fsc == fsc # filter nan
    n, fsc = n[sel], fsc[sel]
    return sum(n*fsc)/sum(n)
# fsc_average()

def randomized_f(f):
    #print("SIZE=", len(f))#, len(f.index))
    phase = numpy.random.uniform(0, 2, size=len(f)) * numpy.pi
    rf = numpy.abs(f) * (numpy.cos(phase) + 1j*numpy.sin(phase))
    return rf
# randomized_f()

def calc_fsc(hkldata, labs):#, fsc_label):
    print("FSC for", labs)
    assert len(labs) == 2
    ret = []
    for i_bin, idxes in hkldata.binned():
        F1, F2 = hkldata.df[labs[0]].to_numpy()[idxes], hkldata.df[labs[1]].to_numpy()[idxes]
        fsc = numpy.real(numpy.corrcoef(F1, F2)[1,0])
        #stats.loc[i_bin, fsc_label] = fsc
        ret.append(fsc)
    return ret

"""import line_profiler
profile = line_profiler.LineProfiler()
import atexit
atexit.register(profile.print_stats)
@profile"""
def calc_randomized_fsc(hkldata, mask, labs_half, labs_half_masked, randomize_fsc_at=0.8):
    stats = hkldata.binned_df[["d_min", "d_max"]].copy()
    stats["ncoeffs"] = 0
    stats["fsc"] = 0.
    #stats.merge(calc_fsc(hkldata, labs_half, "fsc_half_unmasked"))
    #stats.merge(calc_fsc(hkldata, labs_half_masked, "fsc_half_masked"))
    stats["fsc_half_unmasked"] = calc_fsc(hkldata, labs_half)
    stats["fsc_half_masked"] = calc_fsc(hkldata, labs_half_masked)

    labs_rand = [x+"_rand" for x in labs_half_masked]
    hkldata.df[labs_rand[0]] = hkldata.df[labs_half[0]]
    hkldata.df[labs_rand[1]] = hkldata.df[labs_half[1]]

    # Randomize masked F
    rand_start_bin = None
    for i_bin, idxes in hkldata.binned():
        fsc_half = stats["fsc_half_unmasked"][i_bin]
        if rand_start_bin is None and fsc_half < randomize_fsc_at:
            rand_start_bin = i_bin
            logger.writeln(" randomize phase beyond {:.2f} A (bin {})".format(stats["d_max"][i_bin], i_bin))

        if rand_start_bin is not None:
            #print("randomizing", i_bin)
            hkldata.df.loc[idxes, labs_rand[0]] = randomized_f(hkldata.df[labs_half[0]].to_numpy()[idxes])
            #g[labs_rand[1]] = randomized_f(g[labs_half[1]].to_numpy())
            hkldata.df.loc[idxes, labs_rand[1]] = randomized_f(hkldata.df[labs_half[1]].to_numpy()[idxes])

    # Multiply mask
    for i in range(2):
        g = hkldata.fft_map(labs_rand[i], grid_size=mask.shape)
        g.array[:] *= mask
        fg = gemmi.transform_map_to_f_phi(g)
        hkldata.df[labs_rand[i]] = fg.get_value_by_hkl(hkldata.miller_array())

    """
    tmp = utils.maps.mask_and_fft_maps([[grid1], [grid2]], hkldata.d_min_max()[0]-1e-6, mask)
    print(hkldata.df)
    print(tmp.df)
    # TODO efficient update!
    del hkldata.df[labs_rand[0]]# = tmp.df.F_map1
    del hkldata.df[labs_rand[1]]# = tmp.df.F_map2
    del tmp.df["FP"]
    tmp.df.rename(columns=dict(F_map1=labs_rand[0], F_map2=labs_rand[1]), inplace=True)
    hkldata.merge_df(tmp.df)
    print(hkldata.df)
    """
    # Calc randomized fsc
    stats["fsc_half_masked_rand"] = calc_fsc(hkldata, labs_rand)

    # Calc corrected fsc
    stats["fsc_half_masked_corrected"] = 0.
    for i_bin in stats.index:
        if i_bin < rand_start_bin + 2: # RELION way # FIXME rand_start_bin can be None
            stats.loc[i_bin, "fsc_half_masked_corrected"] = stats["fsc_half_masked"][i_bin]
        else:
            fscn = stats["fsc_half_masked_rand"][i_bin]
            fsct = stats["fsc_half_masked"][i_bin]
            #print(i_bin, fsct, fscn)
            stats.loc[i_bin, "fsc_half_masked_corrected"] = (fsct - fscn) / (1. - fscn)
            
    global_res = 999.
    print(stats[stats["fsc_half_masked_corrected"] > 0.143])
    for i_bin in stats.index:
        if stats["fsc_half_masked_corrected"][i_bin] < 0.143:
            break
        #global_res = stats["d_min"][i_bin]
        #global_res = 0.5*(1./stats[["d_min", "d_max"]][i_bin].sum(axis=1))
        global_res = 1./(0.5*(1./stats["d_min"][i_bin]+1./stats["d_max"][i_bin]))
    
    logger.writeln("resolution = {:.2f} A".format(global_res))

    return stats, global_res
# calc_randomized_fsc()

def main(args):
    if not args.model:
        if not args.no_sharpen_before_mask:
            logger.writeln("WARNING: no model specified. setting --no_sharpen_before_mask.")
        args.no_sharpen_before_mask = True

    if args.halfmaps:
        maps = utils.fileio.read_halfmaps(args.halfmaps, pixel_size=args.pixel_size)
        assert maps[0][0].shape == maps[1][0].shape
        assert maps[0][0].unit_cell == maps[1][0].unit_cell
        assert maps[0][1] == maps[1][1]
        unit_cell = maps[0][0].unit_cell
    elif args.map:
        maps = [utils.fileio.read_ccp4_map(args.map, pixel_size=args.pixel_size)]
        unit_cell = maps[0][0].unit_cell
    else:
        raise SystemExit("No input map found.")

    if args.resolution is None:
        args.resolution = utils.maps.nyquist_resolution(maps[0][0])
        logger.writeln("WARNING: --resolution is not specified. Using Nyquist resolution: {:.2f}".format(args.resolution))
        
    if args.model:
        st = utils.fileio.read_structure(args.model)
        st.cell = unit_cell
        st.spacegroup_hm = "P1"
        if len(st.ncs) > 0:
            utils.model.expand_ncs(st)
    else:
        st = None
    
    if args.mask:
        logger.writeln("Input mask file: {}".format(args.mask))
        mask = utils.fileio.read_ccp4_map(args.mask)[0]
    elif args.mask_radius is not None: # TODO use different mask for different model! by chain as well!
        mask = utils.maps.mask_from_model(st, args.mask_radius, grid=maps[0][0])
    else:
        mask = None
    
    if mask is not None:
        if args.no_sharpen_before_mask or len(maps) < 2:
            logger.writeln("Applying mask..")
            masked_maps = [[gemmi.FloatGrid(numpy.array(ma[0], copy=False)*mask, unit_cell, ma[0].spacegroup)]+ma[1:]
                           for ma in maps]
        else:
            logger.writeln("Sharpen-mask-unsharpen..")
            b_before_mask = args.b_before_mask
            if b_before_mask is None: b_before_mask = spa.run_refmac.determine_b_before_mask(st, maps, maps[0][1], mask, args.resolution)
            masked_maps = utils.maps.sharpen_mask_unsharpen(maps, mask, args.resolution, b=b_before_mask)
    else:
        masked_maps = []

    labs_half_masked, labs_half = [], []
    hkldata = utils.maps.mask_and_fft_maps(maps, args.resolution)
    if masked_maps:
        hkldata.df.rename(columns=dict(F_map1="F_map1_nomask", F_map2="F_map2_nomask", FP="FP_nomask"),
                          inplace=True)
        tmp = utils.maps.mask_and_fft_maps(masked_maps, args.resolution)
        hkldata.merge(tmp.df) # TODO slow!
        labs_half_masked = ["F_map1", "F_map2"]
        labs_half = ["F_map1_nomask", "F_map2_nomask"]
    else:
        labs_half = ["F_map1", "F_map2"]

    lab_fc = []
    if args.model:
        lab_fc = "FC"
        hkldata.df[lab_fc] = utils.model.calc_fc_fft(st, args.resolution - 1e-6, source="electron",
                                                     miller_array=hkldata.miller_array())
    else:
        lab_fc = None
        
    hkldata.setup_relion_binning()

    if labs_half_masked and labs_half:
        stats = calc_randomized_fsc(hkldata, mask, labs_half, labs_half_masked)
        #stats.to_csv("tst.csv")
        return stats

    stats = calc_fsc(hkldata, labs_fc=labs_fc, lab_f="FP", labs_half=labs_half, labs_half_masked=labs_half_masked)
    with open(args.fsc_out, "w") as ofs:
        if args.mask:
            ofs.write("# Mask= {}\n".format(args.mask))
        elif args.mask_radius:
            ofs.write("# Mask_radius= {}\n".format(args.mask_radius))
        for lab, xyzin in zip(labs_fc, args.model):
            ofs.write("# {} from {}\n".format(lab, xyzin))

        ofs.write(stats.to_string(index=False, index_names=False)+"\n")
        for k in stats:
            if k.startswith("fsc_FC_"):
                logger.writeln("FSCaverage of {} = {:.4f}".format(k, fsc_average(stats.ncoeffs, stats[k])), fs=ofs)
            if k.startswith("Rcmplx_FC_"):
                logger.writeln("Average of {} = {:.4f}".format(k, fsc_average(stats.ncoeffs, stats[k])), fs=ofs)

    logger.writeln("See {}".format(args.fsc_out))
# main()

if __name__ == "__main__":
    import sys
    args = parse_args(sys.argv[1:])
    stats, global_res = main(args)
    stats.to_csv("tst.csv")
    print(global_res)
