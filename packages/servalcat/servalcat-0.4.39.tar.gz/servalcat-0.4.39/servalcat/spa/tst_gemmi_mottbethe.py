from __future__ import absolute_import, division, print_function, generators
import gemmi
import numpy
import scipy.optimize
import pandas
import time
from servalcat import utils

monlib_path = "/Users/yam/Downloads/ML_up_new"
#monlib_path = "/usr/local/xtal/ccp4/ccp4-7.1/lib/data/monomers"

def calc_fc(st, d_min, blur=0, cutoff=1e-5, rate=1.5):
    print("In calc_fc")
    resnames = st[0].get_all_residue_names()
    monlib = gemmi.read_monomer_lib(monlib_path, resnames)
    topo = gemmi.prepare_topology(st, monlib)
    
    dc = gemmi.DensityCalculatorX()
    dc.d_min = d_min
    dc.blur = blur
    dc.cutoff = cutoff
    dc.rate = rate
    dc.set_grid_cell_and_spacegroup(st)
    dc.addends.subtract_z(except_hydrogen=True)
    dc.initialize_grid()
    dc.add_model_density_to_grid(st[0])
    print("Adjust H")
    topo.adjust_hydrogen_distances(gemmi.Restraints.DistanceOf.Nucleus)
    st.write_pdb('adjusted.pdb')
    print("Put model")
    t = time.time()
    #dc.put_model_density_on_grid(st[0])
    print(" elapsed:", time.time()-t)
    print("Add one by one")
    t = time.time()
    #dc.subtract_hydrogen_z(st[0])
    for cra in st[0].all():
        if cra.atom.is_hydrogen():
            dc.add_c_contribution_to_grid(cra.atom, -1)
    print(" elapsed:", time.time()-t)
    dc.symmetrize_sum()
    grid = gemmi.transform_map_to_f_phi(dc.grid)
    asu_data = grid.prepare_asu_data(dmin=d_min, mott_bethe=True, unblur=dc.blur)
    print(rate, dc.rate, dc.grid.shape)
    return asu_data
# calc_fc()

#def fsc(x, y):
#    denx = numpy.sqrt(numpy.sum(numpy.abs(x)**2))
#    deny = numpy.sqrt(numpy.sum(numpy.abs(y)**2))
#    return numpy.sum(x*numpy.conjugate(y))/denx/deny

def prep_df(st, refmac_mtz, blur=0, cutoff=1e-5, rate=1.5):
    fc_refmac = utils.fileio.read_asu_data_from_mtz(refmac_mtz, ["FC", "PHIC"])
    d_min = numpy.min(fc_refmac.make_d_array()) - 1e-6
    fc_gemmi = calc_fc(st, d_min, blur, cutoff, rate)
    #print(fc_refmac.miller_array, len(fc_refmac.miller_array))
    #print(fc_gemmi.miller_array, len(fc_gemmi.miller_array))
    #print(fc_refmac.value_array)
    #print(fc_gemmi.value_array)

    df_refmac = pandas.DataFrame(data=fc_refmac.miller_array,
                                 columns=["H","K","L"])
    df_refmac["FC_refmac"] = fc_refmac.value_array
    df_gemmi = pandas.DataFrame(data=fc_gemmi.miller_array,
                                columns=["H","K","L"])
    df_gemmi["FC_gemmi"] = fc_gemmi.value_array
    sg = gemmi.SpaceGroup("P1")
    org = numpy.array(df_refmac[["H","K","L"]])
    sg.switch_to_asu(org)#df_refmac[["H","K","L"]])
    #print("refmac")
    #print(numpy.sum(numpy.any(org != df_refmac[["H","K","L"]], axis=1)))
    sel = numpy.any(org != df_refmac[["H","K","L"]], axis=1)
    df_refmac.FC_refmac[sel] = numpy.conj(df_refmac.FC_refmac[sel])
    #print("Org:")
    #print(df_refmac[["H","K","L"]][sel])
    #print("Transformed:")
    #print(org[sel])
    df_refmac[["H","K","L"]] = org
    #df_refmac = df_refmac[sel]
    org = numpy.array(df_gemmi[["H","K","L"]])
    sg.switch_to_asu(org)
    #print("gemmi")
    #print(numpy.sum(numpy.any(org != df_gemmi[["H","K","L"]], axis=1)))
    df_gemmi[["H","K","L"]] = org
    #return
    df = df_refmac.merge(df_gemmi, indicator=True, how="outer")
    df["d"] = fc_refmac.unit_cell.calculate_d_array(df[["H","K","L"]])
    #df["bin"] = numpy.sqrt(df.H**2+df.K**2+df.L**2).astype(numpy.int)
    df["bin"] = (fc_refmac.unit_cell.a/df.d).astype(numpy.int)

    #print(df)
    #print(df[df._merge=="left_only"])
    #print(df[df._merge=="right_only"])
    df=df.sort_values(by=["H","K","L"])
    #print("left_only", df[df._merge=="left_only"].size)
    #print("right_only", df[df._merge=="right_only"].size)
    df = df[df._merge=="both"]
    #df.to_csv("tmp.csv", index=False)
    return df
    #print(df[df.d<1.719])

class Scaler:
    def __init__(self, f1, f2, d):
        """
        Decide scale such that (f1 - k*exp(-b*s^2/4)*f2)**2 -> min
        """
        self.f1 = f1
        self.f2 = f2
        self.s2 = 1/d**2
        self.x = numpy.array([1., 0.])
        # Initial linear scale
        k = numpy.sum(numpy.real(2*self.f1 * numpy.conj(self.f2)))/numpy.sum(numpy.abs(self.f2)**2)
        self.x[0] = k
        
    def f(self, x):
        k, b = x
        k_iso = numpy.exp(-b*self.s2/4)
        return numpy.sum(numpy.abs(self.f1-k*k_iso*self.f2)**2)
    
    def run(self):
        f = self.f(self.x)
        #df = self.df(self.x)
        print("# initial  f= %.6e" % f)
        #print("# initial df=", df)
        print("# initial  x=", self.x)

        status = scipy.optimize.minimize(fun=self.f,
                                         x0=self.x,
                                         #method="L-BFGS-B",
                                         #jac=self.df,
                                         #callback=self.callback
                                         )
        print(status)
        self.x = status.x

        f = self.f(self.x)
        #df = self.df(self.x)
        print("#   final  f= %.6e" % f)
        #print("#   final df=", df)
        print("#   final  x=", self.x)
        
    def get_scale_for_f1(self):
        k, b = self.x
        k_iso = numpy.exp(-b*self.s2/4)
        return 1./k/k_iso
    # get_scales()

    
def run(pdb_in, refmac_mtz):
    st = gemmi.read_structure(pdb_in)
    if len(st.ncs) > 0:
        print("Expanding symmetry.")
        st.expand_ncs(gemmi.HowToNameCopiedChain.Short)

    if 0:
        k, b = 0.84776742, -13.50116766
        for rate in (1.5, 3, 4.5, 6):
            for blur in numpy.arange(0,100,10):
                for cutoff in (5e-5, 5e-6, 5e-7, 5e-8):
                #for cutoff in (5e-9, 5e-10):
                    df = prep_df(st, refmac_mtz, blur, cutoff, rate)
                    df.FC_refmac /= k * numpy.exp(-b/df.d**2/4)
                    fsc = numpy.real(numpy.corrcoef(df.FC_refmac, df.FC_gemmi))[1,0]
                    print(rate, blur, cutoff, fsc)
        return
                                              
    df = prep_df(st, refmac_mtz)
    scaler = Scaler(df.FC_refmac, df.FC_gemmi, df.d)
    scaler.run()
    k = scaler.get_scale_for_f1()
    df.FC_refmac *= k
    
    bins = set(df["bin"])
    for i_bin in bins:
        sel = df.bin==i_bin
        ds = df[sel]
        bin_d_range = numpy.max(ds.d), numpy.min(ds.d)
        fsc = numpy.real(numpy.corrcoef(ds.FC_refmac, ds.FC_gemmi))[1,0]
        print("{:3d} {:7d} {:7.3f} {:7.3f} {:.4f}".format(i_bin, ds.size,
                                                          bin_d_range[0], bin_d_range[1],
                                                          fsc))
    fsc = numpy.real(numpy.corrcoef(df.FC_refmac, df.FC_gemmi))[1,0]
    print("Overall FSC=", fsc)


if __name__ == "__main__":
    import sys
    pdb_in, refmac_mtz = sys.argv[1:]
    run(pdb_in, refmac_mtz)
