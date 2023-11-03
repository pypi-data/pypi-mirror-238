import itertools
from collections import defaultdict, Counter
from typing import Union, Any

import numpy as np
from numpy import ndarray
from pymatgen.analysis.local_env import BrunnerNN_real
from pymatgen.analysis.molecule_structure_comparator import CovalentRadius
from pymatgen.core import Structure, Lattice
from pymatgen.core.interface import Interface
from pymatgen.core.surface import (
    center_slab,
    Slab,
    get_symmetrically_distinct_miller_indices,
    SlabGenerator,
)
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.transformations.standard_transformations import (
    SupercellTransformation,
)
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform

from htflow_utils.misc_tools import (
    attr_to_dict,
    get_subset_indices,
    get_pmg_sg_params,
)


class Shaper:
    @staticmethod
    def get_layer_spacings(
            struct: Union[Structure, Slab, Interface],
            tol: float = 0.1,
            direction: int = 2,
    ) -> np.array:
        """
        Simple method to calculate the projected heights of the spacings
        between layers in the given structure.

        :param struct: Pymatgen object for the structure.
        :type struct: Union[Structure, Slab, Interface]

        :param tol: Tolerance parameters used in the identification of layers, given in units of Angstroms. Defaults
        to 0.1.
        :type tol: float, optional

        :param direction: Direction in which sites are grouped into layers. Allowed values for direction are 0, 1,
        and 2, which correspond to the
            first, second, and third lattice vectors, respectively. Defaults to 2.
        :type direction: int, optional

        :return: list of floats representing the projected distances between layers
            along the surface normal direction in angstroms.
        :rtype: np.array
        """

        # Layer info that contains the c-coordinates and sites
        layers = Shaper.get_layers(struct, tol, direction)

        # Only the c-coordinates of the layers are needed
        layers_c = sorted(layers.keys())

        # Spacing between consecutive layers are calculated
        d = [x - layers_c[i - 1] for i, x in enumerate(layers_c)]

        # When a periodic boundary is passed, layers wrap over, and we get a
        # negative spacing, to correct, we add 1 to negative spacing values
        d = [s + int(s < 0) for s in d]

        # For slabs with the third lattice vector not along miller
        # direction, we need the projected height to also project the vacuum
        # height
        proj_height = Shaper.get_proj_height(struct)

        return np.round([spacing * proj_height for spacing in d], 10)

    @staticmethod
    def get_proj_height(
            struct: Union[Structure, Slab, Interface],
            region: str = "cell",
            min_vac: float = 4.0,
            direction: int = 2,
            tol: float = 0.1,
    ) -> float:
        """
        Internal method to calculate the projected height of a specific region.
        For more than one slab region, the total height is calculated.

        :param struct: Pymatgen object for the structure.
        :type struct: Union[Structure, Slab, Interface]

        :param region: Region to calculate the projected height for. Can take values
            'cell', 'vacuum', or 'slab'. Defaults to 'cell'.
        :type region: str, optional

        :param min_vac: Thickness threshold in angstroms to define a region as a
            vacuum region. Defaults to 4.0.
        :type min_vac: float, optional

        :param direction: Direction in which sites are grouped into layers. Allowed values for direction are 0, 1,
        and 2, which correspond to the
            first, second, and third lattice vectors, respectively. Defaults to 2.
        :type direction: int, optional

        :param tol: Tolerance parameters used in the identification of layers, given in units of Angstroms. Defaults
        to 0.1.
        :type tol: float, optional

        :raises ValueError: Simple check for region keyword to see if it's one of allowed values.

        :return: Projected height of the region. The thickness or height is projected
            along the hkl direction which is assumed to be the normal direction
            to the first two lattice vectors of the passed structure.
        :rtype: float
        """

        lateral_vecs = [
            struct.lattice.matrix[i] for i in range(3) if i != direction
        ]
        normal = np.cross(*lateral_vecs)
        normal /= np.linalg.norm(normal)
        vec_to_proj = struct.lattice.matrix[direction]
        proj_height = np.abs(np.dot(vec_to_proj, normal))
        if region == "cell":
            return proj_height
        elif region == "slab" or region == "vacuum":
            spacings = Shaper.get_layer_spacings(struct, tol)
            slab_height = sum([s for s in spacings if s < min_vac])
            return (
                slab_height if region == "slab" else proj_height - slab_height
            )
        else:
            raise ValueError(
                'Region must be one of "cell", "vacuum", or "slab"'
            )

    @staticmethod
    def resize(
            struct: Union[Structure, Slab, Interface],
            slab_thickness: Union[int, float] = None,
            vacuum_thickness: Union[int, float] = None,
            tol: float = 0.1,
            chunk_size: int = 1,
            min_thick_A: Union[int, float] = None,
            center: bool = True,
            min_vac: Union[int, float] = 4.0,
    ) -> Union[Structure, Slab, Interface]:
        """
        Resizes the input slab with the desired slab thickness in number of
        layers and the vacuum region in Angstroms. All the attributes
        of sites are preserved by the resizing process.

        :param struct: Pymatgen object for the structure.
        :type struct: Union[Structure, Slab, Interface]

        :param slab_thickness: Desired slab thickness in number of layers. Layers will be removed
            from the bottom until the desired thickness is reached. Defaults to None, in which case the
            slab thickness is not modified.
        :type slab_thickness: Union[int, float], optional

        :param vacuum_thickness: Desired vacuum region thickness in Angstroms. Lattice
            parameters are modified in order to get the correct vacuum. Defaults to None, in which case the
            vacuum thickness is not modified.
        :type vacuum_thickness: Union[int, float], optional

        :param tol: Tolerance parameters used in the identification of layers, given in units of Angstroms. Defaults
        to 0.1.
        :type tol: float, optional

        :param chunk_size: Number of layers that are removed at once. Used to preserve terminations. Defaults to 1.
        :type chunk_size: int, optional

        :param min_thick_A: Minimum slab thickness in Angstroms. Defaults to None, in which case the
            minimum thickness is not checked.
        :type min_thick_A: Union[int, float], optional

        :param center: Whether to center the slab in the cell. Defaults to True.
        :type center: bool, optional

        :param min_vac: Thickness threshold in angstroms to define a region as a
            vacuum region. Defaults to 4.0.
        :type min_vac: Union[int, float], optional

        :return: Resized structure.
        :rtype: Union[Structure, Slab, Interface]
        """
        # Input slab is first centered for the cases where the slab spills
        # outside the box from the top and the bottom
        struct_centered = center_slab(struct.copy())
        initial_thickness = Shaper.get_proj_height(
            struct=struct_centered, region="slab", min_vac=min_vac, tol=tol
        )

        if slab_thickness:
            # Layers (containing sites) are removed from the bottom until
            # the desired slab_thickness is reached
            num_layers = len(Shaper.get_layers(struct_centered, tol))
            layers_to_remove = int(
                chunk_size
                * np.floor((num_layers - slab_thickness) / chunk_size)
            )
            if min_thick_A:
                spacings = [
                    spacing
                    for spacing in Shaper.get_layer_spacings(
                        struct_centered, tol
                    )
                    if spacing < 4.0
                ]
                if initial_thickness > min_thick_A:
                    while (
                            initial_thickness - sum(spacings[:layers_to_remove])
                            < min_thick_A
                    ):
                        layers_to_remove -= chunk_size
                else:
                    print(
                        f"Slab with {struct_centered.miller_index} is already smaller than min_thick_A, "
                        f"resizing halted.."
                    )
                    layers_to_remove = 0
            if layers_to_remove > 0:
                struct_resized = Shaper.remove_layers(
                    struct_centered, layers_to_remove, tol=tol, method="layers"
                )
            else:
                struct_resized = struct_centered
        else:
            struct_resized = struct_centered
        # Vacuum region is modified to the desired thickness
        if vacuum_thickness:
            resized_struct = Shaper.modify_vacuum(
                struct_resized, vacuum_thickness, min_vac=min_vac
            )
        else:
            resized_struct = struct_resized

        if not slab_thickness and not vacuum_thickness:
            print(
                f"Warning! You chose to keep the slab and vacuum thicknesses as they are"
                "during resize. Make sure this is what you want."
            )
            resized_struct = struct_centered if center else struct

        # TODO: Add BVS calculation for the resized structure. Here's a prototype:
        # bbs = kwargs.get('bbs')
        # if bbs:
        #     layers_initial = len(Shaper.get_layers(struct_centered, tol))
        #     layers_resized = len(Shaper.get_layers(resized_struct, tol))
        #     diff = layers_initial - layers_resized
        #     shifts = list(bbs.keys())
        #     top_shift = np.round(resized_struct.shift, 4)
        #     top_shift_index = shifts.index(top_shift)
        #     bot_shift = shifts[(top_shift_index - diff) % len(shifts)]
        #     top_bvs = bbs[top_shift]
        #     bot_bvs = bbs[bot_shift]
        #     resized_struct.energy = {'top': top_bvs, 'bottom': bot_bvs}
        return resized_struct

    @staticmethod
    def modify_vacuum(
            struct: Union[Structure, Slab, Interface],
            vac_thick: Union[int, float],
            method: str = "to_value",
            center: bool = True,
            min_vac: Union[int, float] = 4.0,
    ) -> Union[Structure, Slab, Interface]:
        """
        Method to modify the vacuum region in a structure.

        :param struct: Pymatgen object for the structure.
        :type struct: Union[Structure, Slab, Interface]

        :param vac_thick: Vacuum adjustment amount in Angstroms.
        :type vac_thick: Union[int, float]

        :param method: Whether to set the vacuum to the desired value or adjust the
            vacuum in the structure by the given value. Defaults to 'to_value'.
        :type method: str, optional

        :param center: Whether to center the slab in the resulting structure inside
            the vacuum region. Defaults to True.
        :type center: bool, optional

        :param min_vac: Thickness threshold in angstroms to define a region as a
            vacuum region. Defaults to 4.0.
        :type min_vac: Union[int, float], optional

        :raises ValueError: If method is not 'to_value' or 'adjust'.
        :raises ValueError: If vacuum thickness is less than min_vac.

        :return: Modified structure.
        :rtype: Union[Structure, Slab, Interface]

        .. note::
            The vacuum thickness is defined as the distance between the topmost and
            bottommost sites in the structure. If the vacuum thickness is less than
            the minimum vacuum thickness, the vacuum thickness is set to the minimum
            vacuum thickness.
        """

        # Check if a Slab or Structure is passed and proceed accordingly
        if "miller_index" in vars(struct):
            # Necessary slab attributes to resize the Slab
            attrs = [
                "species",
                "miller_index",
                "oriented_unit_cell",
                "shift",
                "scale_factor",
                "reorient_lattice",
                "reconstruction",
                "site_properties",
                "energy",
            ]
            struct_params = attr_to_dict(struct, attrs)
            out_object = Slab
        else:
            # Necessary structure attributes to resize the Structure
            attrs = ["species", "site_properties"]
            struct_params = attr_to_dict(struct, attrs)
            out_object = Structure

        # To avoid issues with fractional coordinates when scaling vacuum,
        # cartesian coordinates are used
        corrected_params = {
            "coords": struct.cart_coords,
            "coords_are_cartesian": True,
        }
        struct_params.update(corrected_params)

        # Lattice parameters are generated in order to be modified
        lat_attrs = ["a", "b", "c", "alpha", "beta", "gamma"]
        lat_params = attr_to_dict(struct.lattice, lat_attrs)

        # latvec = struct.lattice.matrix
        proj_height = Shaper.get_proj_height(struct)

        # 'c' parameter of the Lattice is modified to adjust vacuum
        # to the desired thickness
        if method == "to_value":
            initial_vac = Shaper.get_proj_height(struct, "vacuum", min_vac)
            lat_params["c"] += (
                    (vac_thick - initial_vac) * lat_params["c"] / proj_height
            )
        elif method == "by_value":
            lat_params["c"] += vac_thick * lat_params["c"] / proj_height

        new_lat = Lattice.from_parameters(**lat_params)

        modified_struct = (
            center_slab(out_object(new_lat, **struct_params))
            if center
            else out_object(new_lat, **struct_params)
        )

        return modified_struct

    @staticmethod
    def get_layers(
            struct: Union[Structure, Slab, Interface],
            tol: float = 0.1,
            direction: int = 2,
    ) -> dict:
        """
        Finds the layers in the structure taking z-direction as the primary
        direction such that the layers form planes parallel to xy-plane.

        :param struct: Pymatgen object for the structure.
        :type struct: Union[Structure, Slab, Interface]

        :param tol: Tolerance parameters used in the identification of layers, given in units of Angstroms. Defaults
        to 0.1.
        :type tol: float, optional

        :param direction: Direction in which sites are grouped into layers. Allowed values for direction are 0, 1,
        and 2, which correspond to the
            first, second, and third lattice vectors, respectively. Defaults to 2.
        :type direction: int, optional

        :return: Dictionary with keys as z-coords of layers and values as the
            indices of sites that belong to that layer.
        :rtype: dict

        """
        # number of sites in the structure
        n = len(struct)
        frac_coords = struct.frac_coords

        # initiate a num_sites dimensional square distance matrix and populate
        dist_matrix = np.zeros((n, n))
        for i, j in itertools.combinations(list(range(n)), 2):
            if i != j:
                cdist = frac_coords[i][direction] - frac_coords[j][direction]
                # cdist = abs(cdist - round(cdist)) * proj_height
                cdist = (
                        abs(cdist - round(cdist)) * struct.lattice.abc[direction]
                )
                dist_matrix[i, j] = cdist
                dist_matrix[j, i] = cdist

        condensed_m = squareform(dist_matrix)
        z = linkage(condensed_m)

        # cluster the sites in the structure based on their c-coordinate
        # and a given tolerance
        clusters = fcluster(z, tol, criterion="distance")
        layers = defaultdict(list)
        for i, v in enumerate(clusters):
            layers[v].append(i)

        # for each layer, find sites that belong to it and assign the first
        # site's c-coord as the c-coord of the layer
        layers = {
            struct.frac_coords[v[0]][direction]: v for k, v in layers.items()
        }
        return layers

    @staticmethod
    def remove_layers(
            slab: Union[Slab, Interface],
            num_layers: int,
            tol: float = 0.1,
            method: str = "target",
            position: str = "bottom",
            center: bool = True,
    ) -> Union[Slab, Interface]:
        """
        Removes layers from the bottom or top of the slab while updating the number
        of bonds broken in the meantime.

        :param slab: Pymatgen Slab or Interface object.
        :type slab: Union[Slab, Interface]

        :param num_layers: Number of layers to remove from the structure.
        :type num_layers: int

        :param tol: Tolerance parameters used in the identification of layers, given in units of Angstroms. Defaults
        to 0.1.
        :type tol: float, optional

        :param method: Whether to remove num_layers or remove layers until the structure has
            num_layers number of layers in total. Options are 'target' and 'layers'.
            Defaults to 'target'.
        :type method: str, optional

        :param position: Side on which the sites should be removed. Available options are 'top'
            and 'bottom'. Defaults to 'bottom'.
        :type position: str, optional

        :param center: Whether to center the slab in the vacuum after removing layers.
            Defaults to 'True'.
        :type center: bool, optional

        :return: A new Slab object with the requested number of layers removed.
        :rtype: Union[Slab, Interface]

        """
        layers = Shaper.get_layers(slab, tol)
        if num_layers > len(layers):
            raise ValueError(
                "Number of layers to remove/target can't exceed \
                             the number of layers in the given slab."
            )
        c_coords = sorted(layers.keys())
        if method == "layers":
            to_remove = (
                c_coords[:num_layers]
                if position == "bottom"
                else c_coords[len(c_coords) - num_layers:]
            )
        elif method == "target":
            to_remove = (
                c_coords[: len(c_coords) - num_layers]
                if position == "bottom"
                else c_coords[num_layers:]
            )
        else:
            raise ValueError(
                f'{method} is not a valid method. Please use either "layers" or "target".'
            )
        indices_list = [layers[c_coord] for c_coord in to_remove]
        flat_list = [item for sublist in indices_list for item in sublist]
        slab_copy = slab.copy()
        slab_copy.remove_sites(flat_list)
        return center_slab(slab_copy) if center else slab_copy

    @staticmethod
    def get_average_layer_spacing(
            slab: Union[Slab, Interface],
            tol: float = 0.1,
            vacuum_threshold: Union[int, float] = 6.0,
    ) -> ndarray:
        """
        Computes the average distance between the slab's layers disregarding the vacuum region.

        :param slab: Pymatgen Slab or Interface object.
        :type slab: Union[Slab, Interface]

        :param tol: Tolerance parameters used in the identification of layers, given in units of Angstroms. Defaults
        to 0.1.
        :type tol: float, optional

        :param vacuum_threshold: Regions larger than this will be treated as vacuum and will not be
            treated as an interlayer spacing. Defaults to 6.0.
        :type vacuum_threshold: Union[int, float], optional

        :return: Average layer spacing.
        :rtype: float

        """
        spacings = Shaper.get_layer_spacings(slab, tol)
        spacings_no_vac = np.delete(
            spacings, np.where(spacings >= vacuum_threshold)
        )
        av_spacing = np.mean(spacings_no_vac)
        return av_spacing

    @staticmethod
    def get_bonds(
            struct: Union[Slab, Structure],
            dtol: float = 0.20,
    ) -> dict:
        """
        Finds all unique bonds in the structure and orders them by bond strength
        using bond valence method and with the assumption that the ideal bond length
        = CovalentRadius(site1) + CovalentRadius(site2).

        ONLY HERE FOR BACKWARDS COMPATIBILITY. WILL SOON BE DEPRECATED.
        USE get_all_bonds INSTEAD and if needed extract the bonds you want,
        i.e. the shortest ones as this method does.

        :param struct: Pymatgen object for the conventional bulk structure.
        :type struct: pymatgen.core.structure.Structure

        :param dtol: Added tolerance to form a bond for the dictionary passed to the slab generation
            algorithm. Defaults to 0.20.
        :type dtol: float, optional

        :return: Collection of bonds that has a 'weight' within a delta of the highest
            weight bond.
        :rtype: dict
        """
        bnn = BrunnerNN_real(cutoff=2 * max(struct.lattice.abc))
        species, indices = np.unique(
            [str(x) for x in struct.species], return_index=True
        )
        bonds = {}
        for i, site_index in enumerate(indices):
            sp1 = species[i]
            for neighbor in bnn.get_nn_info(struct, site_index):
                neighbor = neighbor["site"]
                sp2 = str(neighbor.specie)
                dist = neighbor.nn_distance
                if ((sp1, sp2) not in bonds) and ((sp2, sp1) not in bonds):
                    bonds[(sp1, sp2)] = dist * (1 + dtol)
        return bonds

    @staticmethod
    def get_all_bonds(struct: Union[Slab, Structure, Interface], r: float):
        if struct.site_properties.get("bulk_equivalent") is None:
            sga = SpacegroupAnalyzer(struct)
            struct.add_site_property(
                "bulk_equivalent",
                sga.get_symmetry_dataset()["equivalent_atoms"].tolist(),
            )

        species_list = struct.labels
        bonds = []
        for site_index in range(len(struct)):
            sp1 = species_list[site_index]
            neighbors = struct.get_neighbors(struct[site_index], r)
            for neighbor in neighbors:
                sp2 = species_list[neighbor.index]
                dist = round(neighbor.nn_distance, 6)
                # sort sp1 and sp2 to avoid duplicates
                bond = tuple(sorted((sp1, sp2))) + (dist,)
                if bond not in bonds:
                    bonds.append(bond)

        return bonds

    @staticmethod
    def calculate_bv(r1: float, r2: float, bond_dist: float) -> float:
        """
        Calculates the bond valence using the bond valence method and the assumption that
        the ideal bond length = CovalentRadius(site1) + CovalentRadius(site2).

        :param r1: Covalent radius of the first site.
        :type r1: float

        :param r2: Covalent radius of the second site.
        :type r2: float

        :param bond_dist: Distance between the two sites.
        :type bond_dist: float

        :return: Bond valence.
        :rtype: float
        """
        b, r_0 = 0.37, r1 + r2
        return np.exp((r_0 - bond_dist) / b)

    @staticmethod
    def get_surface_area(struct: Union[Structure, Slab, Interface]) -> float:
        """
        Calculates the surface area of a structure.

        :param struct: Pymatgen object for the structure.
        :type struct: Union[Structure, Slab, Interface]

        :return: Surface area of the structure.
        :rtype: float
        """
        mat = struct.lattice.matrix
        return np.linalg.norm(np.cross(mat[0], mat[1]))

    @staticmethod
    def get_bonds_by_shift(
            sg: SlabGenerator,
            bulk_conv: Structure,
            nn_method: str = "all",
            tol: float = 0.1,
            edge_tol: int = 3,
            cutoff: Union[int, float] = 5.0,
    ) -> tuple[dict[str, dict[Any, Any]], Any]:
        """
        Calculates the bond valence sums of the broken bonds corresponding to all the possible shifts.

        :param sg: SlabGenerator object.
        :type sg: SlabGenerator

        :param bulk_conv: Conventional standard structure that is used to generate the slabs.
        :type bulk_conv: pymatgen.core.structure.Structure

        :param nn_method: Method to use for finding nearest neighbors. Options are 'all' and 'voronoi'.
            Defaults to 'all'.
        :type nn_method: str, optional

        :param tol: Tolerance parameters used in the identification of layers, given in units of Angstroms. Defaults
        to 0.1.
        :type tol: float, optional

        :param edge_tol: Tolerance to use in the identification of the edges. Defaults to 3.
        :type edge_tol: int, optional

        :param cutoff: Cutoff distance for identifying bonds. Defaults to 5.0 Angstroms.
        :type cutoff: Union[int, float], optional

        :return: A tuple containing a dictionary with bond valence sums for each shift and the
            corresponding shift.
        :rtype: tuple[dict[str, dict[Any, Any]], Any]
        """
        unique_sites = np.unique(
            bulk_conv.site_properties["bulk_equivalent"], return_index=True
        )[1]
        c_bulk = {}
        bonds_bulk = {}
        for site_index in unique_sites:
            site = bulk_conv[site_index]
            specie = str(site.specie)
            nn_list = Shaper.get_neighbors(
                bulk_conv, cutoff, nn_method, site_index
            )
            c_bulk[site_index] = len(nn_list)
            bonds_bulk[f"{specie}-{site_index}"] = [
                (
                    f'{str(nn.specie)}-{nn.properties["bulk_equivalent"]}',
                    np.round(nn.nn_distance, 6),
                )
                for nn in nn_list
            ]

        slabs = {
            np.round(slab.shift, 4): slab for slab in sg.get_slabs(ftol=tol)
        }
        area = list(slabs.values())[0].surface_area

        bbs = {}
        for shift, slab in slabs.items():
            layers = Shaper.get_layers(slab, tol)
            layers_c_sorted = sorted(layers.keys())

            if edge_tol > len(layers_c_sorted) or edge_tol == 99:
                top_layers_c_coords = layers_c_sorted
            else:
                top_layers_c_coords = layers_c_sorted[-edge_tol:]
            top_layer_sites = [
                site for k in top_layers_c_coords for site in layers[k]
            ]
            nn_dict = defaultdict(list)
            for site_index in top_layer_sites:
                site = slab[site_index]
                specie = str(site.specie)
                bulk_eq = site.properties["bulk_equivalent"]
                nn_list = Shaper.get_neighbors(
                    slab, cutoff, nn_method, site_index
                )
                nn_list_hr = [
                    (
                        f'{str(nn.specie)}-{nn.properties["bulk_equivalent"]}',
                        np.round(nn.nn_distance, 6),
                    )
                    for nn in nn_list
                ]
                nn_list_hr_bulk = bonds_bulk[f"{specie}-{bulk_eq}"]
                diff = Counter(nn_list_hr_bulk) - Counter(nn_list_hr)
                bonds_broken = list(diff.elements())
                if bonds_broken:
                    nn_dict[f"{specie}-{bulk_eq}"] += bonds_broken
            bbs[shift] = nn_dict
        return bbs, area

    @staticmethod
    def get_bvs(
            bbs: dict[str, dict[Any, Any]], weight: str = "BVS"
    ) -> dict[Any, Any]:
        """
        Calculates the bond valence sum of the broken bonds at each shift.

        :param bbs: Dictionary of bonds broken at each shift.
        :type bbs: dict[str, dict[Any, Any]]

        :param weight: Weighting scheme to be used. Currently supported schemes are 'BVS' and 'equal'.
            Defaults to 'BVS'.
        :type weight: str, optional

        :return: Dictionary of bond valence sums at each shift.
        :rtype: dict[Any, Any]
        """
        cr = CovalentRadius().radius
        bvs_by_shift = {}
        for shift, bonds in bbs.items():
            shift_tot = 0
            for site, nn_list in bonds.items():
                specie = site.split("-")[0]
                if weight == "BVS":
                    shift_tot += sum(
                        [
                            Shaper.calculate_bv(
                                cr[specie], cr[nn[0].split("-")[0]], nn[1]
                            )
                            for nn in nn_list
                        ]
                    )
                elif weight == "equal":
                    shift_tot += len(nn_list)
                else:
                    raise ValueError(f"weight {weight} not recognized!")
            bvs_by_shift[shift] = shift_tot
        return bvs_by_shift

    @staticmethod
    def get_neighbors(bulk_conv, cutoff, nn_method, site_index):
        """
        Gets the neighbors of a site in a structure.

        :param bulk_conv: Bulk structure.
        :type bulk_conv: pymatgen.core.structure.Structure

        :param cutoff: Cut-off radius.
        :type cutoff: float

        :param nn_method: Nearest-neighbor algorithm to be used. Options are 'BNN' and built-in nn finder of Structure.
            Defaults to 'BNN'.
        :type nn_method: str, optional

        :param site_index: Index of the site.
        :type site_index: int

        :return: List of neighbors.
        :rtype: list
        """
        if nn_method == "BNN":
            bnn = BrunnerNN_real(cutoff=cutoff)
            try:
                nn_list = bnn.get_nn_info(bulk_conv, site_index)
            except ValueError:
                bnn = BrunnerNN_real(cutoff=2 * cutoff)
                nn_list = bnn.get_nn_info(bulk_conv, site_index)
            nn_list = [nn["site"] for nn in nn_list]
        else:
            site = bulk_conv[site_index]
            nn_list = bulk_conv.get_neighbors(site=site, r=cutoff)
        return nn_list

    @staticmethod
    def fix_regions(
        struct: Union[Slab, Structure],
        tol: float = 0.1,
        fix_type: str = "z_pos",
        n_middle: int = None,
    ) -> Union[Slab, Structure]:
        """
        Adds site properties to the structure to fix certain ions from moving during a relaxation run.

        :param struct: Pymatgen object for the structure.
        :type struct: Union[Structure, Slab]

        :param tol: Tolerance parameters used in the identification of layers, given in units of Angstroms. Defaults
        to 0.1.
        :type tol: float, optional

        :param fix_type: Type of region fixing to be used. For PES calculations, 'z_pos'
            is usually employed while to simulate bulk in certain slabs,
            we can fix part of the slab completely. Defaults to 'z_pos'.
        :type fix_type: str, optional

        :param n_middle: Number of middle layers to fix. Only used if `fix_type` is 'middle_n'. Defaults to None.
        :type n_middle: int, optional

        :raises Exception: If `fix_type` is not one of 'z_pos', 'top_half', 'bottom_half',
            'top_third', 'bottom_third', 'middle_n'.

        :return: Structure with site properties added to fix certain ions from moving during a relaxation run.
        :rtype: Union[Structure, Slab]

        """
        allowed_fix_types = [
            "z_pos",
            "top_half",
            "bottom_half",
            "top_third",
            "bottom_third",
            "middle_n",
        ]
        if fix_type not in allowed_fix_types:
            raise ValueError(f"Your fix_type is not in {allowed_fix_types}")
        layers = Shaper.get_layers(struct, tol)
        sorted_layers = sorted(layers.keys())
        num_layers = len(layers)
        fix_arr = np.asarray([[True, True, True] for _ in range(len(struct))])
        if fix_type == "z_pos":
            fix_arr[:, 2] = False
        elif fix_type == "middle_n":
            if num_layers % 2 != 0 and n_middle % 2 == 0:
                raise ValueError(
                    f"The number of layers in the slab is odd, please set 'n_middle' to and odd number."
                )
            elif num_layers % 2 == 0 and n_middle % 2 != 0:
                raise ValueError(
                    f"The number of layers in the slab is even, please set 'n_middle' to and even number."
                )
            elif n_middle > num_layers:
                raise ValueError(
                    f"The number of layers in the slab is {num_layers}, please set 'n_middle' to a smaller number."
                )

            start_fix = (num_layers - n_middle) // 2
            end_fix = start_fix + n_middle

            sites = [
                item
                for sublist in [
                    v for k, v in layers.items() if k in sorted_layers[start_fix:end_fix]
                ]
                for item in sublist
            ]
            for site in sites:
                fix_arr[site] = [False, False, False]
        elif fix_type in (
                "top_half",
                "bottom_half",
                "top_third",
                "bottom_third",
        ):
            num_layers_fix = (
                int(num_layers / 2)
                if fix_type.endswith("half")
                else int(num_layers / 3)
            )
            fixed_layers = (
                sorted_layers[:num_layers_fix]
                if fix_type.startswith("bottom")
                else sorted_layers[num_layers_fix:]
            )
            sites = [
                item
                for sublist in [
                    v for k, v in layers.items() if k in fixed_layers
                ]
                for item in sublist
            ]
            for site in sites:
                fix_arr[site] = [False, False, False]
        struct_copy = struct.copy()
        fix_arr = fix_arr.tolist()
        struct_copy.add_site_property("selective_dynamics", fix_arr)
        return struct_copy

    @staticmethod
    def identify_slab(slab: Slab) -> dict:
        """
        Identifies the symmetry and stoichiometry of a given slab.

        :param slab: Pymatgen Slab object.
        :type slab: Slab

        :return: Dictionary containing the symmetry and stoichiometry information.
        :rtype: dict
        """
        sym = slab.is_symmetric()
        bulk = slab.oriented_unit_cell
        slab_reduced_formula = slab.composition.reduced_formula
        bulk_reduced_formula = bulk.composition.reduced_formula
        sto = slab_reduced_formula == bulk_reduced_formula
        return {"symmetric": sym, "stoichiometric": sto}

    @staticmethod
    def generate_slabs(
            bulk_conv: Structure, sg_params: dict, to_file=False
    ) -> tuple[dict, dict]:
        """
        Generates slabs with the given parameters.

        :param bulk_conv: Conventional standard bulk structure from which to generate slabs from.
        :type bulk_conv: pymatgen.core.structure.Structure

        :param sg_params: Parameters used in slab generation.
        :type sg_params: dict

        :param to_file: Whether to write the slabs to a file. Defaults to False.
        :type to_file: bool, optional

        :return: Dictionary containing the generated slabs and dictionary containing the slab parameters.
        :rtype: tuple[dict, dict]

        .. note::
           Check the markdown file in the docs folder for more information on the parameters.
        """
        # First, we check sg_params if it has the required keys and fill the missing
        # ones with the default values.
        # TODO: Find a better way, this is ugly.
        # sg_params = check_input({"sg_params": sg_params}, ["sg_params"])[
        #     "sg_params"
        # ]

        max_index = sg_params.get("max_index")
        miller = sg_params.get("miller")
        if miller and not max_index:
            print(
                f"Generating slabs for the following miller indices: {miller}"
            )
            miller = sg_params.get("miller")
            if isinstance(miller[0], int):
                miller = [(*miller,)]
            else:
                miller = [(*m,) for m in miller]
        elif max_index and not miller:
            miller = get_symmetrically_distinct_miller_indices(
                bulk_conv, max_index
            )
        elif max_index and miller:
            raise ValueError(
                "You cannot specify both max_index and miller parameters."
            )
        else:
            raise ValueError(
                "You must specify either max_index or miller parameters."
            )

        tol = sg_params.get("tol")
        resize = sg_params.get("resize")
        symmetrize = sg_params.get("symmetrize")
        match_ouc_lattice = sg_params.get("match_ouc_lattice")
        calculate_bonds = sg_params.get("calculate_bonds")
        sg_dict = {}
        slabs_dict = {}
        for m in miller:
            # we need some parameters to use in SlabGenerator, so we extract those
            # from the input sg_params and put them in pmg_sg_params
            pmg_sg_params = get_pmg_sg_params(
                bulk_conv=bulk_conv, miller=m, sg_params=sg_params
            )

            # we first try a SlabGenerator with the given sg_params, if things go as
            # expected we proceed with this
            sg = SlabGenerator(**pmg_sg_params)

            d_hkl, pmg_layer_size = Shaper.get_pmg_layer_size(
                bulk_conv=bulk_conv, miller=m, sg=sg, tol=tol
            )

            min_thick_a = sg_params["min_thick_A"]
            # if there is a min_thick_A key in sg_params, we have to ensure that the slabs we initially
            # generate (before resizing) have thicknesses greater than this value. For this, we modify
            # the corresponding min_slab_size parameter in pmg_sg_params by calculating the number of layers
            # needed to reach min_thick_A.
            if min_thick_a:
                final_layer_spacing = Shaper.get_layer_spacings(
                    sg.oriented_unit_cell, tol
                )[-1]
                min_slab_size = max(
                    np.ceil((min_thick_a + final_layer_spacing) / d_hkl),
                    sg_params["slab_thick"],
                )
                pmg_sg_params["min_slab_size"] = min_slab_size
                sg = SlabGenerator(**pmg_sg_params)

            slabs = sg.get_slabs(ftol=tol, symmetrize=symmetrize)
            if not slabs:
                continue

            if match_ouc_lattice:
                # we check if we can get an oriented unit cell with the same lateral lattice
                # parameters and gamma angle as the slab, for consistency with brillouin zone
                # sampling
                ouc = Shaper.get_matching_ouc(slabs[0])
                if ouc:
                    param_modified = False
                else:
                    # if no such ouc exists, we turn off primitive and lll_reduce, since
                    # only when either one or both of these are True, we have issues with
                    # finding matching ouc
                    print(
                        "OUC matching failed with the given sg_params, modifying primitive and lll_reduce.."
                    )
                    pmg_sg_params.update(
                        {"primitive": False, "lll_reduce": False}
                    )
                    sg_modified = SlabGenerator(**pmg_sg_params)
                    slabs_modified = sg_modified.get_slabs(
                        ftol=tol, symmetrize=symmetrize
                    )
                    # we set a flag to show that sg params are modified, and we will assign
                    # this as an attribute to the Slab objects, so that we can tell if the slabs
                    # generated result from a modified sg
                    ouc = Shaper.get_matching_ouc(slabs_modified[0])
                    if ouc:
                        param_modified = True
                        slabs = slabs_modified
                        sg = sg_modified
                    else:
                        # if we still don't have a matching ouc, which should not happen
                        # we print and a non-matching ouc is used instead.
                        print(
                            f"Matching oriented unit cell cannot be found. Your reference energies"
                            f"might not be suitable for a surface energy convergence scheme."
                        )
                        param_modified = False

                # we change the oriented unit cells of slabs to the matching ouc that we find.
                if ouc:
                    for slab in slabs:
                        slab.oriented_unit_cell = ouc

                # we assign attributes to slabs if they result from a modified sg, and this is done after resizing
                # because as soon as a pymatgen structure is copied (such is the case in Shaper.resize()), it loses
                # all attributes not defined in the copy method. Since param_modified is such an attribute, we need
                # to add it after resizing the slabs.
            else:
                param_modified = False

            for slab in slabs:
                slab.param_modified = param_modified

            # resize flag is used generate slabs with user-defined thicknesses in number of layers.
            # This is done by removing layers from the bottom of the pymatgen generated slabs since
            # they are usually thicker than one would expect.
            slab_thick, vac_thick = (
                sg_params["slab_thick"],
                sg_params["vac_thick"],
            )
            if resize:
                # if we want to preserve terminations, we must remove layers in chunks
                # and these chunk sizes are determined by pmg_layer_size
                preserve_terminations = sg_params.get("preserve_terminations")
                chunk_size = pmg_layer_size if preserve_terminations else 1

                slabs = [
                    Shaper.resize(
                        slab,
                        slab_thick,
                        vac_thick,
                        tol=tol,
                        chunk_size=chunk_size,
                        min_thick_A=min_thick_a,
                    )
                    for slab in slabs
                ]
            else:
                # TODO: Remove this once resize is confirmed working. Only here to generate
                # TODO: slabs with sizes comparable to the initial slab_thick with pymatgen
                # slab_thick_pmg = np.ceil(slab_thick / pmg_layer_size)
                # pmg_sg_params.update({'min_slab_size': slab_thick_pmg})
                # sg = SlabGenerator(**pmg_sg_params)
                # slabs = sg.get_slabs(ftol=tol, symmetrize=symmetrize)
                # THIS NOW JUST RESIZES THE VACUUM AND LEAVES THE SLABS UNTOUCHED
                slabs = [
                    Shaper.resize(slab, vacuum_thickness=vac_thick, tol=tol)
                    for slab in slabs
                ]

            # check if slabs list is empty, which only happens when symmetrize is True
            # and the sg can not find symmetric slabs.
            try:
                slabs[0]
            except IndexError:
                print(
                    f"Symmetric slabs could not be generated for {m} orientation. Increasing slab_thick"
                    " may or may not solve this issue."
                )
                continue

            for slab in slabs:
                slab.pmg_layer_size = pmg_layer_size

            # TODO: Remove this once we decide where to filter out large slabs
            # max_nsites = sg_params.get('max_nsites', None)
            # if max_nsites:
            #     slabs = [slab for slab in slabs if slab.num_sites <= max_nsites]
            # try:
            #     slab = slabs[0]
            # except IndexError:
            #     print(f'No slabs could be generated for {m} orientation because all'
            #           f' slabs have more than {max_nsites} sites.')
            #     continue

            # we assign energies (bond valence sums of broken bonds) to each slab, in this case
            # unique terminations, and also the pymatgen layer size, which is the number of layers
            # we can safely remove at once while preserving terminations.

            if calculate_bonds:
                nn_method = sg_params.get("nn_method")
                weight = sg_params.get("weight")
                max_bl = max(Shaper.get_bonds(bulk_conv).values())
                bbs, area = Shaper.get_bonds_by_shift(
                    sg=sg,
                    bulk_conv=bulk_conv,
                    nn_method=nn_method,
                    tol=tol,
                    cutoff=max_bl,
                    edge_tol=99,
                )
                bvs = Shaper.get_bvs(bbs, weight=weight)
                for slab in slabs:
                    slab.energy = {
                        "broken_bonds": bbs[np.round(slab.shift, 4)],
                        "bvs_per_area": bvs[np.round(slab.shift, 4)] / area,
                        "area": area,
                    }

            if to_file:
                for index, slab in enumerate(slabs):
                    formula = slab.formula
                    hkl = "".join([str(i) for i in slab.miller_index])
                    area = np.round(slab.surface_area, 2)
                    slab.to(f"{formula}_{hkl}_{area}_{index}.vasp", "poscar")

            slabs_dict[m] = slabs
            sg_dict[m] = sg

        return slabs_dict, sg_dict

    @staticmethod
    def get_pmg_layer_size(
            bulk_conv: Structure, miller: tuple, sg: SlabGenerator, tol: float
    ) -> tuple[float, int]:
        """
        Calculates the size of a single layer in pymatgen's slab generation algorithm.

        :param bulk_conv: Conventional standard bulk structure from which to generate slabs from.
        :type bulk_conv: pymatgen.core.structure.Structure

        :param miller: Miller indices of the slab.
        :type miller: tuple

        :param sg: SlabGenerator object.
        :type sg: SlabGenerator

        :param tol: Tolerance parameters used in the identification of layers, given in units of Angstroms. Defaults
        to 0.1.
        :type tol: float

        :return: A tuple containing the distance between miller planes and the number of layers
            considered a single layer in pymatgen's slab generation algorithm.
        :rtype: tuple[float, int]
        """
        # since the terminations repeat every d_hkl distance in c direction,
        # the distance between miller planes, we need to figure out how many
        # layers this d_hkl portion corresponds to in order to preserve terminations
        d_hkl = bulk_conv.lattice.d_hkl(miller)
        try:
            ouc_layers = len(Shaper.get_layers(sg.oriented_unit_cell, tol))
        except ValueError:
            ouc_layers = 1
        ouc_height = Shaper.get_proj_height(sg.oriented_unit_cell)
        # we calculate how many layers pymatgen considers a single layer here
        pmg_layer_size = int(ouc_layers / round(ouc_height / d_hkl))
        return d_hkl, pmg_layer_size

    @staticmethod
    def get_constrained_ouc(slab: Slab) -> Structure:
        """
        Finds the constrained oriented unit cell of a Slab object.

        :param slab: Pymatgen Slab object.
        :type slab: Slab

        :return: Constrained oriented unit cell of the input Slab object.
        :rtype: Structure

        """
        constraints = {
            "a": slab.lattice.a,
            "b": slab.lattice.b,
            "gamma": slab.lattice.gamma,
        }
        ouc = slab.oriented_unit_cell.get_primitive_structure(
            constrain_latt=constraints
        )
        return ouc

    @staticmethod
    def get_matching_ouc(slab: Slab) -> Union[Structure, None]:
        """
        Given a slab, finds an oriented unit cell that matches the lateral lattice parameters
        and the gamma angle of the slab. Useful for constructing an oriented unit cell to be
        used as a reference structure for surface energy calculations.

        :param slab: Pymatgen Slab object whose oriented unit cell we want to constrain.
        :type slab: Slab

        :return: Constrained oriented unit cell of the input Slab object.
        :rtype: Structure
        """
        # applying LLL reduction on a structure sometimes changes the orders of the lattice
        # parameters and hence, the ordering of the lattice vectors. In order to have a
        # consistent sampling of Brillouin zone between the slab and the oriented unit cell
        # we rotate the oriented unit cell to have the same orientation as the slab.
        trans = {
            0: ((0, 0, 1), (0, 1, 0), (1, 0, 0)),
            1: ((1, 0, 0), (0, 0, 1), (0, 1, 0)),
        }
        ouc = slab.oriented_unit_cell
        # we first check if the preset OUC matches
        lattice_match = Shaper._check_lattice_match(slab.lattice, ouc.lattice)
        # angle_check = ouc.lattice.angles[3 - sum(indices)] == slab.lattice.gamma
        if not lattice_match:
            ouc = ouc.copy(sanitize=True)
            lattice_match = Shaper._check_lattice_match(
                slab.lattice, ouc.lattice
            )
            if not lattice_match:
                ouc = Shaper.get_constrained_ouc(slab)
                lattice_match = Shaper._check_lattice_match(
                    slab.lattice, ouc.lattice
                )
                if not lattice_match:
                    return None

        # since the whole reason we do this is to match the kpoint sampling of the slab
        # and the oriented unit cell in the plane parallel to the surface, we need to align
        # the matched lattice vectors, and that's why we perform this SupercellTransformation
        # to make sure we transform the OUC to have the same base vectors as the slab
        if lattice_match != 2:
            st = SupercellTransformation(trans[lattice_match])
            ouc = st.apply_transformation(ouc)
        return ouc

    @staticmethod
    def _check_lattice_match(
            lattice1: Lattice, lattice2: Lattice
    ) -> Union[int, None]:
        """
        Checks if two lattices have the same base vectors, ignoring orientations.

        :param lattice1: Pymatgen Lattice object that we want to use as a reference.
        :type lattice1: Lattice

        :param lattice2: Pymatgen Lattice object that we want to compare against the reference.
        :type lattice2: Lattice

        :return: If there is a match, returns the index of the angle between the matched base vectors.
            This is enough information to go further. If no match is found, returns None.
        :rtype: Union[int, None]

        """
        matches_ab = get_subset_indices(lattice1.abc[:2], lattice2.abc)
        if not matches_ab:
            return None
        else:
            for match_ab in matches_ab:
                angle_index = 3 - sum(match_ab)
                check = np.isclose(
                    lattice1.gamma, lattice2.angles[angle_index]
                )
                if check:
                    return angle_index
            return None
