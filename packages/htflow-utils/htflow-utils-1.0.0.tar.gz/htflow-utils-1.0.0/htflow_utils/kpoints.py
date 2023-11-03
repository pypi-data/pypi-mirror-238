import math

from pymatgen.io.vasp import Kpoints


class MeshFromDensity:
    """
    Class to find classic Monkhorst-Pack meshes which may
    or my not be Gamma-Centred from a given k-point density.
    Provides also capabilities to check if meshes generated from similar
    densities are equivalent. Meshes for slabs are adapted according to
    the lower symmetry conditions.
    """

    def __init__(
            self,
            structure,
            target_density,
            compare_density=10.0,
            is_slab="Auto",
            min_vac=6.0,
            force_gamma=False,
    ):
        """
        Initializes the class and sets internal variables.

        :param structure: Pymatgen representation of the structure.
        :type structure: pymatgen.core.structure.Structure

        :param target_density: Desired minimal density of kpoints along each
            reciprocal lattice vector in 1/Angstrom.
        :type target_density: float

        :param compare_density: Density for which the mesh of the target
            density is to be compared to. in 1/Angstrom. Defaults to 10.0.
        :type compare_density: float, optional

        :param is_slab: If the passed structure is to be considered to be a
            slab. If "True" it is considered to be a slab, if "False" it is
            considered to be bulk, if "Auto", it is attempted to find out,
            defaults to "Auto".
        :type is_slab: bool/str, optional

        :param min_vac: Thickness threshold in angstroms to define a region as a
            vacuum region. Defaults to 6.0.
        :type min_vac: float, optional

        :param force_gamma: If Gamma-centred meshes are to be forces (not
            applicable for generalized meshes!). Defaults to False.
        :type force_gamma: bool, optional
        """

        self.struct = structure.copy()
        self.dens = target_density
        self.compare_dens = compare_density
        self.min_vac = min_vac
        self.force_gamma = force_gamma
        self.klm = structure.lattice.reciprocal_lattice.abc

        if is_slab:
            self.slab = True
        elif is_slab in ["Auto", "auto", "automatic", "Automatic"]:
            self.slab = "detect_automatically"
        else:
            self.slab = False

    def __make_mesh(self, density):
        """
        Return the subdivisions along each lattice vector.

        Consider also if the structure is a slab.

        :param density: Desired minimal density of kpoints along each
            reciprocal lattice vector in 1/Angstrom.
        :type density: float

        :return: Subdivisions along each lattice vector.
        :rtype: tuple
        """

        k, l, m = self.klm
        k1 = math.ceil(k * density)
        k2 = math.ceil(l * density)
        k3 = math.ceil(m * density)
        if self._is_slab():
            k3 = 1
        return tuple([k1, k2, k3])

    def _is_slab(self):
        """
        Figures out if the passed structure is a slab.

        Automatic detection might fail for slabs that are set up in a non-standard way!

        :return: True if the structure is considered a slab, False if not.
        :rtype: bool
        """

        if self.slab:
            return True
        elif self.slab == "detect_automatically":
            z_axis = self.struct.lattice.c
            z_coords = []
            for s in self.struct.sites:
                z_coords.append(s.coords[2])

            thickness = max(z_coords) - min(z_coords)
            if z_axis - thickness >= self.min_vac:
                return True
            else:
                return False
        else:
            return False

    def get_kpoints(self):
        """
        Return a Kpoint object with the desired density of kpoints.

        :return: Kpoint object
        :rtype: pymatgen.io.vasp.Kpoints
        """

        mesh = self.__make_mesh(self.dens)
        is_hexagonal = self.struct.lattice.is_hexagonal()
        # has_odd = any(i % 2 == 1 for i in mesh)

        if is_hexagonal or self.force_gamma:
            kpoints = Kpoints.gamma_automatic(kpts=mesh)
        else:
            kpoints = Kpoints.monkhorst_automatic(kpts=mesh)

        return kpoints

    def are_meshes_the_same(self):
        """
        Compares conventional Monkhorst-Pack meshes and Gamma centered meshes.

        To test if a different target density actually provides a different
        mesh than a reference density.

        :return: True if meshes are the same, False otherwise.
        :rtype: bool
        """

        mesh_1 = self.__make_mesh(self.dens)
        mesh_2 = self.__make_mesh(self.compare_dens)
        if mesh_1 == mesh_2:
            return True
        else:
            return False
