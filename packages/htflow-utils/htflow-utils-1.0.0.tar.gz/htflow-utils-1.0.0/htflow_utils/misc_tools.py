import itertools
import json
import os
import warnings
from typing import Union, Type

import numpy as np
from pymatgen.core.interface import Interface
from pymatgen.core.structure import Structure
from pymatgen.core.surface import Slab

from htflow_utils.caching import dict_to_hash


def get_by_path(root: dict, items: list):
    """
    Get a value from a dictionary by a list of keys.

    :param root: Dictionary to search in.
    :type root: dict

    :param items: A list of keys to search for.
    :type items: list

    :return: value
    :rtype: object
    """
    import operator
    from functools import reduce

    return reduce(operator.getitem, items, root)


def make_calculation_hash(
        structure: Union[Slab, Structure], **additional_params
):
    frac_coords = np.round(structure.frac_coords, 6)
    frac_coords[frac_coords == 1.0] = 0.0
    species = [site.species_string for site in structure.sites]
    sites = sorted(
        [(species[i], tuple(frac_coords[i])) for i in range(len(species))],
        key=lambda x: x[1][2],
    )
    return dict_to_hash({"sites": sites, **additional_params})


def attr_to_dict(obj, attrs: list):
    """
    Converts the attributes of an object to a dictionary.

    :param obj: Object to convert.
    :type obj: object

    :param attrs: A list of attributes to convert.
    :type attrs: list

    :return: Dictionary of converted attributes.
    :rtype: dict
    """
    attr_dict = {attr: getattr(obj, attr, None) for attr in attrs}
    return attr_dict


def get_subset_indices(list1: tuple, list2: tuple) -> list:
    """
    Returns the indices of list1 that are also in list2.

    :param list1: List of values.
    :type list1: tuple

    :param list2: List of values.
    :type list2: tuple

    :return: List of indices of elements in list1 that are also in list2.
    :rtype: list
    """
    couples = list(itertools.permutations(list2, len(list1)))
    indices = list(itertools.permutations(range(len(list2)), len(list1)))
    matches = [
        indices[i] for i, x in enumerate(couples) if np.allclose(x, list1)
    ]
    return matches


def generate_input_dict(
        struct: Union[Structure, Slab, Interface], calc_type: str, tag: str
) -> dict:
    """
    Simple function to generate a dictionary that stores the structure
    and the type of calculation to be performed on it.

    :param struct: Pymatgen object for the structure.
    :type struct: Structure, Slab, Interface

    :param calc_type: Type of calculation to be performed on the structure.
    :type calc_type: str

    :param tag: Short description of the structure in relation to what
        is being calculated. For example, can be 'slab', 'ouc',
        'sto_slab' and so on.
    :type tag: str

    :raises ValueError: If calc_type is not 'static' or 'relax'.

    :return: Simple dictionary describing the calculation.
    :rtype: dict
    """
    # check if calc_type is either 'static' or 'relax', otherwise raise error
    if calc_type not in ["static", "relax"]:
        raise ValueError(
            f"calc_type must be either 'static' or 'relax', not {calc_type}"
        )
    # struct_type = 'slab' if hasattr(struct, 'miller_index') else 'bulk'
    input_dict = {
        "struct": struct,
        # 'struct_type': struct_type,
        "calc_type": calc_type,
        "calc_tag": tag,
    }
    return input_dict


def get_pmg_sg_params(bulk_conv: Structure, miller: tuple, sg_params: dict):
    """
    Generates a dictionary of parameters that can be used to generate a slab
    using the SlabGenerator class from pymatgen.

    :param bulk_conv: Pymatgen structure of the bulk.
    :type bulk_conv: Structure

    :param miller: Miller index of the surface.
    :type miller: tuple

    :param sg_params: Parameters used in slab generation.
    :type sg_params: dict

    :return:  Dictionary of parameters to be used in pymatgen's SlabGenerator.
    :rtype: dict
    """
    pmg_sg_params = {
        "initial_structure": bulk_conv,
        "min_slab_size": sg_params["slab_thick"],
        "min_vacuum_size": sg_params["vac_thick"],
        "lll_reduce": sg_params["lll_reduce"],
        "center_slab": sg_params["center_slab"],
        "in_unit_planes": True,
        "primitive": sg_params["primitive"],
        "reorient_lattice": True,
    }
    # the actual max_normal_search used in SlabGenerator is defined using
    # the corresponding max_normal_search in sg_params. We use two options,
    # either "max" or None. Then the pmg_sg_params is updated with these
    mns = sg_params.get("max_normal_search")
    max_normal_search = max([abs(i) for i in miller]) if mns == "max" else mns
    pmg_sg_params.update(
        {"max_normal_search": max_normal_search, "miller_index": miller}
    )
    return pmg_sg_params


def parse_miller(miller: str) -> tuple:
    """
    Parse a miller index from a string to a tuple.

    :param miller: Miller index in string format.
    :type miller: str

    :return: Miller index in tuple format.
    :rtype: tuple
    """
    emp = []
    flag = False
    for i, m in enumerate(miller):
        try:
            tmp = (1 - 2 * int(flag)) * int(m)
            emp.append(tmp)
        except ValueError:
            flag = True
        else:
            flag = False
    return tuple(emp)


def load_defaults(module_name):
    """
    Loads the defaults from a module's defaults.json file and updates them

    :param module_name: name of the module
    :type module_name: str

    :return: defaults
    :rtype: dict
    """
    config_file = os.environ.get("FW_CONFIG_FILE")
    config_dir = os.path.dirname(config_file) if config_file else None
    try:
        with open(os.path.join(config_dir, "user_defaults.json")) as f:
            user_defaults = json.load(f)
    except (FileNotFoundError, TypeError):
        user_defaults = {}

    # import the module and get the path
    module = __import__(module_name)
    module_path = os.path.dirname(module.__file__)
    json_path = os.path.join(module_path, "defaults.json")
    with open(json_path, "r") as f:
        defaults_dict = json.load(f)
    defaults_dict.update(user_defaults)
    return defaults_dict


def transfer_average_magmoms(magnetic_struct: Type[Structure],
                             struct_without_magmoms: Type[Structure]) -> Type[Structure]:
    """Set magmom for a structure based on the average value of each species of a reference structure.

    For unit cells of the same structure, it is not always trivial to transfer
    the site properties. This function attempts to transfer at least the magmom
    site property between two structures with the same species, but not
    necessarily the same number of sites. For each species the average value
    of the magentic moments in the magnetic input structure is computed and
    set as a site property for all atoms of the same species in the output
    structure. NOTE THAT THIS WILL GIVE GENERALLY WRONG RESULTS FOR ALL BUT
    SIMPLE FERROMAGNETIC STRUCTURES!

    Parameters
    ----------
    magnetic_struct : pymatgen.core.structure.Structure
        Input structure with "magmom" site property.
    struct_without_magmoms : pymatgen.core.structure.Structure
        Input structure with no "magmom" site property but the same species.

    Returns
    -------
    new_struct : pymatgen.core.structure.Structure
        copy of struct_without_magmoms with added "magmom" site property.

    """

    mag_struct = magnetic_struct.copy()
    new_struct = struct_without_magmoms.copy()

    if not mag_struct.site_properties.get("magmom"):
        print("No magnetic moments to transfer. Doing nothing...")
        return new_struct

    if not sorted(mag_struct.types_of_species) == sorted(
            new_struct.types_of_species
    ):
        warnings.warn(
            "\n##################################################\n"
            "You are trying to transfer magnetic moments between\n"
            "two structures which contain different species and\n"
            "                 THIS CANNOT WORK!\n"
            "The code will continue to run, without transferring\n"
            "any magnetic moments. Convergence might be slow..."
            "\n##################################################\n"
        )
        return new_struct

    magmom_dict = {}
    for s in mag_struct.types_of_species:
        magmom_dict[s] = []
        for i, el in enumerate(mag_struct.species):
            if s == el:
                magmom_dict[s].append(
                    mag_struct.site_properties.get("magmom")[i]
                )
        magmom_dict[s] = np.mean(magmom_dict[s])

    new_magmoms = []
    for s in new_struct.species:
        new_magmoms.append(magmom_dict[s])
    new_struct.add_site_property("magmom", new_magmoms)

    return new_struct
