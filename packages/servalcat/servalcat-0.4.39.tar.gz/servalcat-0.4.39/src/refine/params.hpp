// Copyright 2023 MRC Laboratory of Molecular Biology
//

#ifndef GEMMI_REFINE_PARAMS_HPP_
#define GEMMI_REFINE_PARAMS_HPP_

namespace gemmi {

struct AtomParams {
  std::vector<Atom*> atoms;
  std::vector<bool> exclude_geom;
  std::vector<bool> exclude_ll_grad;
  std::vector<int> pos_adp; // position of ADP in parameter vector
  std::vector<bool> is_aniso; // need it?
  int n_params = 0;
  bool refine_xyz;
  bool refine_adp;

  AtomParams(Model &model, bool refine_xyz, bool refine_adp)
    : refine_xyz(refine_xyz), refine_adp(refine_adp) {
    assert(refine_xyz); // now it's assumed
    const int n_atoms = count_atom_sites(model);
    atoms.resize(n_atoms);
    for (CRA cra : model.all())
      atoms[cra.atom->serial-1] = cra.atom;

    exclude_geom.resize(n_atoms, false);
    exclude_ll_grad.resize(n_atoms, false);

    if (refine_xyz)
      n_params += n_atoms * 3;
    
    if (refine_adp) {
      pos_adp.resize(n_atoms);
      int i = refine_xyz ? n_atoms * 3 : 0;
      for (CRA cra : model.all()) {
        pos_adp[cra.atom->serial-1] = i;
        i += cra.atom->aniso.nonzero() ? 6 : 1;
      }
      n_params = i;
    }
  }

  void set_x(const std::vector<double>& x) {
    assert(x.size() == n_params);
    int i = 0;
    if (refine_xyz)
      for (auto a : atoms) {
        a->pos = {x[i], x[i+1], x[i+2]};
        i += 3;
      }
    if (refine_adp)
      for (auto a : atoms) {
        if (a->aniso.nonzero()) { // what happens if aniso is given after construction?
          a->aniso = {x[i], x[i+1], x[i+2], x[i+3], x[i+4], x[i+5]};
          i+= 6;
        }
        else
          a->b_iso = x[i++];
      }
    assert(i == n_params);
  }
  std::vector<double> get_x() const {
    std::vector<double> x;
    x.reserve(n_params);
    if (refine_xyz)
      for (auto a : atoms)
        for (int i = 0; i < 3; ++i)
          x.push_back(a->pos.at(i));
    if (refine_adp)
      for (auto a : atoms) {
        if (a->aniso.nonzero()) // what happens if aniso is given after construction?
          for (auto u : a->aniso.elements_pdb())
            x.push_back(u);
        else
          x.push_back(a->b_iso);
      }
    return x;
  }

  void find_position() {

  }
};

} // namespace gemmi
#endif
