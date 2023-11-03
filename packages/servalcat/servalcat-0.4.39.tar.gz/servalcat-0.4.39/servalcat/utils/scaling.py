"""
Author: "Keitaro Yamashita, Garib N. Murshudov"
MRC Laboratory of Molecular Biology
    
This software is released under the
Mozilla Public License, version 2.0; see LICENSE.
"""
def dwf_aniso(unit_cell, aniso, hkl):
    return numpy.exp(-2*numpy.pi**2*aniso.transformed_by(unit_cell.fractionalization_matrix).r_u_r(hkl))

def dwf_iso(unit_cell, b, hkl):
    svec = numpy.dot(unit_cell.fractionalization_matrix, numpy.transpose(hkl)).T
    return numpy.exp(-b*numpy.sum(svec**2, axis=1)/4)

class InitialScaler(object):
    def __init__(self, fo_asu, fc_asu, aniso=False):
        self.aniso = aniso
        self.unit_cell = fo_asu.unit_cell
        self.miller_array = fo_asu.miller_array
        self.use_log = False
        #self.loss_f = lambda z: numpy.log(1+z)
        #self.loss_g = lambda z: 1./(1+z)
        #self.loss_f = lambda z: 2*(numpy.sqrt(1+z)-1)
        #self.loss_g = lambda z: (1+z)**(-1/2)
        self.loss_f = lambda z: z
        self.loss_g = lambda z: 1.
        Ainv = self.unit_cell.fractionalization_matrix
        
        self.svec = numpy.dot(Ainv, numpy.transpose(self.miller_array)).T
        self.Fo = fo_asu.value_array
        self.Fc = fc_asu.value_array
        if self.use_log:
            self.Fo = numpy.abs(fo_asu.value_array)
            self.Fc = numpy.abs(fc_asu.value_array)

        # Initial linear scale
        k = numpy.sum(numpy.real(2*self.Fo * numpy.conj(self.Fc)))/numpy.sum(numpy.abs(self.Fc)**2)
        if self.aniso:
            self.x = numpy.zeros(7)
        else:
            self.x = numpy.zeros(2)
            
        self.x[0] = k

        # Debug
        if 0:
            e = 1.e-8
            x=self.x
            num=numpy.zeros(len(x))
            for i in range(len(x)):
                y = numpy.copy(x)
                f_0 = self.f(y)
                y[i] += e
                f_1 = self.f(y)
                num[i]=(f_1-f_0)/e
            print("num=", num)
            ana=self.df(x)
            print("ana=", ana)
            print("err=", numpy.abs(ana-num)/num)

    def f(self, x):
        k = x[0]
        if self.aniso:
            u = gemmi.SMat33d(*x[1:])
            k_tmp = dwf_aniso(self.unit_cell, u, self.miller_array)
        else:
            k_tmp = dwf_iso(self.unit_cell, x[1], self.miller_array)

        if self.use_log:
            return numpy.sum(numpy.abs(numpy.log(self.Fo)-numpy.log(k)-numpy.log(k_tmp)-numpy.log(self.Fc))**2)
        else:
            return self.loss_f(numpy.sum(numpy.abs(self.Fo-k*k_tmp*self.Fc)**2))
    # f()

    def df(self, x):
        k = x[0]
        ret = numpy.zeros(len(x))
        fofc = 2*numpy.real(self.Fo*numpy.conj(self.Fc))
        fc2 = numpy.abs(self.Fc)**2

        if self.aniso:
            u = gemmi.SMat33d(*x[1:])
            k_aniso = dwf_aniso(self.unit_cell, u, self.miller_array)
            pi2 = numpy.pi**2
            ret[0] = numpy.sum(-k_aniso*fofc + 2*k*k_aniso**2*fc2)

            tmp = ((0,0), (1,1), (2,2), (0,1), (0,2), (1,2))
            #svec = self.miller_array.
            for i in range(1, 7):
                n, m = tmp[i-1]
                deriv = self.svec[:,n]*self.svec[:,m]
                if i > 3: deriv *= 2
                ret[i] = numpy.sum(2*pi2*k*deriv*k_aniso*fofc - 4*pi2*k**2*deriv*k_aniso**2*fc2)
        else:
            k_iso = dwf_iso(self.unit_cell, x[1], self.miller_array)
            s2 = numpy.sum(self.svec**2, axis=1)
            ret[0] = numpy.sum(-k_iso*fofc + 2*k*k_iso**2*fc2)
            ret[1] = numpy.sum(k*k_iso*s2/4*fofc - k**2*s2/2*k_iso**2*fc2)

            ret *= self.loss_g(numpy.sum(numpy.abs(self.Fo-k*k_iso*self.Fc)**2))

        return ret
    # f()

    def run(self):
        #f, df = self.f(self.x), self.df(self.x)
        f = self.f(self.x)
        df = self.df(self.x)
        print("# initial  f= %.6e" % f)
        print("# initial df=", df)
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
        df = self.df(self.x)
        print("#   final  f= %.6e" % f)
        print("#   final df=", df)
        print("#   final  x=", self.x)

    # run()

    def get_scales(self):
        if self.aniso:
            u = gemmi.SMat33d(*self.x[1:])
            k_tmp = dwf_aniso(self.unit_cell, u, self.miller_array)
        else:
            k_tmp = dwf_iso(self.unit_cell, self.x[1], self.miller_array)

        return 1./self.x[0]/k_tmp
    # get_scales()
# class InitialScaler
