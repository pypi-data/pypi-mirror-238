from typing import Union

from pymatgen.core.interface import Interface
from pymatgen.core.structure import Structure
from pymatgen.core.surface import Slab
from pymatgen.io.vasp.sets import (
    MPScanRelaxSet,
    MPRelaxSet,
    MPScanStaticSet,
    MPStaticSet,
    MPMDSet,
)

from htflow_utils.external_forces import (
    ext_pressure_to_force_array,
    force_array_to_string,
)
from htflow_utils.kpoints import MeshFromDensity
from htflow_utils.misc_tools import load_defaults

defaults = load_defaults("surfflow")

scan_keywords = [
    "scan",
    "rscan",
    "r2scan",
    "Scan",
    "Rscan",
    "R2scan",
    "SCAN",
    "RSCAN",
    "R2SCAN",
]

vdw_keywords = [
    "dftd2",
    "dftd3",
    "dftd3-bj",
    "ts",
    "ts-hirshfeld",
    "mbd@rsc",
    "ddsc",
    "df",
    "optpbe",
    "optb88",
    "optb86b",
    "df2",
    "rvv10",
]


def get_emin_and_emax(potcar):
    """
    Return ENMIN and ENMAX energy cutoff for a given Potcar object.

    :param potcar: Potcar object
    :type potcar: pymatgen.io.vasp.inputs.Potcar

    :return: dict with ENMIN and ENMAX
    :rtype: dict
    """

    emin = []
    emax = []
    for pot in potcar:
        emin.append(pot.PSCTR.get("ENMIN"))
        emax.append(pot.PSCTR.get("ENMAX"))
    return {"ENMIN": max(emin), "ENMAX": max(emax)}


def get_custom_vasp_static_settings(
        structure: Structure,
        comp_parameters: dict,
        static_type: str,
        k_dens_default: float = 8.5,
        custom_uis: dict = None,
        custom_ups: dict = None,
) -> Union[MPStaticSet, MPScanStaticSet]:
    """Make custom vasp settings for static calculations.

    See get_custom_vasp_relax_settings for more details.
    """

    allowed_types = [
        "bulk_from_scratch",
        "bulk_follow_up",
        "bulk_nscf",
        "slab_from_scratch",
        "slab_follow_up",
        "slab_nscf",
        "bulk_epsilon_from_scratch",
        "bulk_epsilon_follow_up",
    ]

    if static_type not in allowed_types:
        raise SystemExit(
            "static type is not known. Please select from: {}".format(
                allowed_types
            )
        )

    # Set user incar settings:
    uis = {
        "NEDOS": 3001,
        "PREC": "Accurate",
        "GGA_COMPAT": ".FALSE.",
        "LASPH": ".TRUE.",
        "LORBIT": 11,
        "NELMIN": 4,
        "SIGMA": 0.05,
        "ISMEAR": -5,
        "EDIFF": 1.0e-6,
        "SYMPREC": 1e-04,
        "LMAXMIX": 6,
    }
    # include electrons with l-quantum number up to 6 into the mixer. Helps with convergence
    # maybe include functionality that sets LMAXMIX dependent on periodic table group
    # e.g.:
    # for element in structure.composition.elements:
    #     if element.group == 3:
    #         uis['LMAXMIX'] = 6
    #     elif element.group in [4,5,6,7,8,9,10,11,12]:
    #         uis['LMAXMIX'] = 4

    if static_type.startswith("bulk_"):
        uis["ALGO"] = "Fast"

    if static_type.endswith("from_scratch"):
        uis["ICHARG"] = 2
        uis["LAECHG"] = ".FALSE."

    if structure.num_sites < 20:
        uis["LREAL"] = ".FALSE."

    # Adjust mixing for slabs that have a very large c axis:
    if structure.lattice.c > 50.0:
        uis["AMIN"] = 0.05

    if comp_parameters.get("functional") in scan_keywords:
        uis["ISMEAR"] = 0
        uis["SIGMA"] = 0.1

    if static_type.startswith("slab_"):
        uis["NELMDL"] = -15
        uis["NELM"] = 200
        # set dipole corrections.
        try:
            polarity = structure.is_polar()
        except AttributeError:
            pass
        else:
            if polarity:
                uis["DIPOL"] = list(structure.center_of_mass)
                uis["IDIPOL"] = 3
                uis["LDIPOL"] = True
                uis["NELM"] = 300
                uis["MAXMIX"] = 150
    elif comp_parameters.get("functional") in scan_keywords:
        uis["NELMDL"] = -10
    else:
        uis["NELMDL"] = -6
        uis["NELM"] = 200

    if "encut" in comp_parameters:
        uis["ENCUT"] = comp_parameters["encut"]

    if "use_spin" in comp_parameters:
        if comp_parameters["use_spin"]:
            uis["ISPIN"] = 2
        else:
            uis["ISPIN"] = 1

    # set van der Waals functional. Note that as of now, 'functional' must be
    # specified for vdw to work!
    if {"use_vdw", "functional"} <= comp_parameters.keys():
        if comp_parameters["use_vdw"]:
            if comp_parameters.get("functional") in scan_keywords:
                vdw = "rVV10"
                uis["BPARAM"] = 11.95
            else:
                if comp_parameters["use_vdw"] in vdw_keywords:
                    vdw = comp_parameters["use_vdw"]
                else:
                    vdw = "optB86b"
        else:
            vdw = None
    else:
        vdw = None

    if comp_parameters.get("functional") in scan_keywords:
        uis["METAGGA"] = "R2SCAN"
        uis["ALGO"] = "All"
        uis["LELF"] = False  # otherwise KPAR >1 crashes

    if static_type.endswith("follow_up"):
        uis["ISTART"] = 1
        uis["LREAL"] = ".FALSE."
        uis["NELMDL"] = -1
    elif static_type.endswith("nsfc"):
        uis["ISTART"] = 1
        uis["LREAL"] = ".FALSE."
        uis["ICHARG"] = 11
        uis["NELMDL"] = -1

    if "kspacing" in comp_parameters:
        uis["KSPACING"] = comp_parameters["kspacing"]
        uis["KGAMMA"] = True
        kpoints = None
    elif "k_dens" in comp_parameters:
        if static_type.startswith("slab_") or static_type.startswith(
                "interface_"
        ):
            is_slab = True
        else:
            is_slab = False
        kpts = MeshFromDensity(
            structure,
            comp_parameters["k_dens"],
            is_slab=is_slab,
            force_gamma=True,
        )
        kpoints = kpts.get_kpoints()
    else:
        if static_type.startswith("slab_") or static_type.startswith(
                "interface_"
        ):
            is_slab = True
        else:
            is_slab = False
        kpts = MeshFromDensity(
            structure, k_dens_default, is_slab=is_slab, force_gamma=True
        )
        kpoints = kpts.get_kpoints()
    uks = kpoints

    if "LDA" in comp_parameters.get("functional"):
        upf = "LDA_54"
    else:
        upf = "PBE_54"

    if static_type.startswith("bulk_epsilon"):
        uis["LEPSILON"] = True
        uis["KPAR"] = 2
        uis["IBRION"] = 8
        if comp_parameters.get("is_metal", False):
            uis["LPEAD"] = False
        else:
            uis["LPEAD"] = True

    if custom_uis:
        try:
            uis.update(custom_uis)
        except ValueError:
            raise ValueError("custom_uis must be a valid dictionary.")

    if comp_parameters.get("functional") in scan_keywords:
        vis = MPScanStaticSet(
            structure,
            user_incar_settings=uis,
            vdw=vdw,
            user_kpoints_settings=uks,
            user_potcar_functional="PBE_54",
            user_potcar_settings=custom_ups,
        )
    else:
        vis = MPStaticSet(
            structure,
            user_incar_settings=uis,
            vdw=vdw,
            user_kpoints_settings=uks,
            user_potcar_functional=upf,
            user_potcar_settings=custom_ups,
        )

    return vis


def get_custom_vasp_relax_settings(
    structure: Union[Structure, Slab, Interface],
    comp_parameters: dict,
    relax_type: str,
    k_dens_default: float = 8.5,
    custom_uis: dict = None,
    custom_ups: dict = None,
    apply_pressure: Union[bool, float] = False,
    md_params=None,
) -> Union[MPRelaxSet, MPScanRelaxSet]:
    """
    Make custom vasp settings for relaxations.

    :param structure: Structure to be relaxed.
    :type structure: pymatgen.core.structure.Structure

    :param comp_parameters: Computational parameters dictionary which is usually created partly
        by the user and then filled automatically with defaults and after convergence tests.
    :type comp_parameters: dict

    :param relax_type: Specifies what is to be relaxed in what way. Check 'allowed_types'
        for a list of choices.
    :type relax_type: str

    :param k_dens_default: Specifies the default kpoint density if no k_dens or kspacing key
        is found in the comp_parameters dictionary. Defaults to 8.5.
    :type k_dens_default: float, optional

    :param custom_uis: Specify user potcar settings, e.g. which potcar to choose for which
        element. Defaults to there to fix an issue with tungsten, where
        MP uses W_pv, which is depreciated by VASP and replaced with W_sv. Defaults to None.
    :type custom_uis: dict, optional

    :param custom_ups: Specify user potcar settings, e.g. which potcar to choose for which
        element. Defaults to there to fix an issue with tungsten, where
        MP uses W_pv, which is depreciated by VASP and replaced with W_sv. Similar issue
        with Nb. Defaults to {"W": "W_sv", "Nb": "Nb_sv"}.
    :type custom_ups: dict, optional

    :param apply_pressure: If set to a float, the calculation will be run with an external
        pressure of the given value in GPa if the relax type starts with 'slab'
        or 'interface'. Defaults to False.

    :raises ValueError: If the relax_type is not in the allowed_types list.

    :return: VaspInputSet object for the given parameters.
    :rtype: pymatgen.io.vasp.sets.MPRelaxSet or pymatgen.io.vasp.sets.MPScanRelaxSet
    """

    if md_params is None:
        md_params = {}
    allowed_types = [
        "bulk_full_relax",
        "bulk_vol_relax",
        "bulk_pos_relax",
        "bulk_shape_relax",
        "bulk_pos_shape_relax",
        "slab_shape_relax",
        "slab_pos_relax",
        "interface_shape_relax",
        "interface_pos_relax",
        "interface_z_relax",
        "slab_MD",
    ]

    if relax_type not in allowed_types:
        raise SystemExit(
            "relax type is not known. Please select from: {}".format(
                allowed_types
            )
        )

    # Set user incar settings:
    uis = {
        "NEDOS": 3001,
        "PREC": "Accurate",
        "GGA_COMPAT": ".FALSE.",
        "LASPH": ".TRUE.",
        "LORBIT": 11,
        "MAXMIX": 100,
        "NELMIN": 5,
        "EDIFF": 0.5e-5,
        "LAECHG": ".FALSE.",
        "SYMPREC": 1e-04,
        "LMAXMIX": 6,
    }
    # include electrons with l-quantum number up to 6 into the mixer. Helps with convergence
    # maybe include functionality that sets LMAXMIX dependent on periodic table group
    # e.g.:
    # for element in structure.composition.elements:
    #     if element.group == 3:
    #         uis['LMAXMIX'] = 6
    #     elif element.group in [4,5,6,7,8,9,10,11,12]:
    #         uis['LMAXMIX'] = 4

    if structure.num_sites < 20:
        uis["LREAL"] = ".FALSE."

    # Adjust mixing for slabs that have a very large c axis:
    if structure.lattice.c > 50.0:
        uis["AMIN"] = 0.05

    if relax_type.startswith("slab_") or relax_type.startswith("interface_"):
        uis["NELMDL"] = -15
        uis["EDIFFG"] = -0.015
        uis["NELM"] = 200
        # Use a slightly slower but more stable algorithm for the electrons
        uis["ALGO"] = "Normal"
        # Turn on linear mixing
        # uis['AMIX'] = 0.2
        # uis['BMIX'] = 0.0001
        # uis['AMIX_MAG'] = 0.8
        # uis['BMIX_MAG'] = 0.0001
        # set dipole corrections. Only works for slabs, so has to be in a try/except block
        try:
            polarity = structure.is_polar()
        except AttributeError:
            pass
        else:
            if polarity and not relax_type.endswith("MD"):
                uis["DIPOL"] = list(structure.center_of_mass)
                uis["IDIPOL"] = 3
                uis["LDIPOL"] = ".TRUE."
                uis["NELM"] = 300
                uis["MAXMIX"] = 150
    else:
        uis["NELMDL"] = -6
        uis["EDIFFG"] = -0.01
        uis["NELM"] = 100
        uis["ALGO"] = "Fast"

    if relax_type.startswith("bulk_"):
        uis["IBRION"] = 1

    if relax_type.endswith("full_relax"):
        uis["ISIF"] = 3
    elif relax_type.endswith("pos_relax"):
        uis["ISIF"] = 2
    elif relax_type.endswith("z_relax"):
        uis["ISIF"] = 2
        # Set up selective dynamics array for the structures site property
        sd_array = []
        for i in range(len(structure.sites)):
            sd_array.append([False, False, True])
        structure.add_site_property("selective_dynamics", sd_array)
    elif relax_type.endswith("vol_relax"):
        uis["ISIF"] = 7
    elif relax_type.endswith("pos_shape_relax"):
        uis["ISIF"] = 4
    elif relax_type.endswith("shape_relax"):
        uis["ISIF"] = 5

    if "encut" in comp_parameters:
        uis["ENCUT"] = comp_parameters["encut"]

    if "use_spin" in comp_parameters:
        if comp_parameters["use_spin"]:
            uis["ISPIN"] = 2
        else:
            uis["ISPIN"] = 1

    if "is_metal" in comp_parameters:
        if comp_parameters["is_metal"]:
            uis["SIGMA"] = 0.2
            uis["ISMEAR"] = 1
        elif relax_type.startswith("bulk"):
            uis["SIGMA"] = 0.05
            uis["ISMEAR"] = -5
        else:
            uis["SIGMA"] = 0.1
            uis["ISMEAR"] = 0
    else:
        uis["SIGMA"] = 0.1
        uis["ISMEAR"] = 0

    # set van der Waals functional. Note that as of now, 'functional' must be
    # specified for vdw to work!

    if {"use_vdw", "functional"} <= comp_parameters.keys():
        if comp_parameters["use_vdw"]:
            if comp_parameters.get("functional") in scan_keywords:
                vdw = "rVV10"
            else:
                if comp_parameters["use_vdw"] in vdw_keywords:
                    vdw = comp_parameters["use_vdw"]
                else:
                    vdw = "optB86b"
        else:
            vdw = None
    else:
        vdw = None

    if "kspacing" in comp_parameters:
        uis["KSPACING"] = comp_parameters["kspacing"]
        uis["KGAMMA"] = True
        kpoints = None
    elif "k_dens" in comp_parameters:
        if relax_type.startswith("slab_") or relax_type.startswith(
                "interface_"
        ):
            is_slab = True
        else:
            is_slab = False
        kpts = MeshFromDensity(
            structure,
            comp_parameters["k_dens"],
            is_slab=is_slab,
            force_gamma=True,
        )
        kpoints = kpts.get_kpoints()
    else:
        if relax_type.startswith("slab_") or relax_type.startswith(
                "interface_"
        ):
            is_slab = True
        else:
            is_slab = False
        kpts = MeshFromDensity(
            structure, k_dens_default, is_slab=is_slab, force_gamma=True
        )
        kpoints = kpts.get_kpoints()
    uks = kpoints

    if "LDA" in comp_parameters.get("functional"):
        upf = "LDA_54"
    else:
        upf = "PBE_54"

    if apply_pressure and (
            relax_type.startswith("slab_") or relax_type.startswith("interface_")
    ):
        forces = ext_pressure_to_force_array(structure, apply_pressure)
        force_str = force_array_to_string(forces)
        uis["EFOR"] = force_str
    elif apply_pressure and relax_type.startswith("bulk_"):
        UserWarning("External pressure can not be applied to bulk systems.")

    if custom_uis:
        try:
            uis.update(custom_uis)
        except ValueError:
            print(
                f"Check custom_uis. It should be a dictionary of key-value pairs."
            )

    if "functional" in comp_parameters:
        if comp_parameters.get("functional") in scan_keywords:
            # Algo All does not play well with tetrahedron method
            if "is_metal" in comp_parameters:
                if not comp_parameters["is_metal"]:
                    uis["SIGMA"] = 0.1
                    uis["ISMEAR"] = 0
            uis["METAGGA"] = "R2SCAN"
            uis["ALGO"] = "All"
            uis["LELF"] = False  # otherwise KPAR >1 crashes
            vis = MPScanRelaxSet(
                structure,
                user_incar_settings=uis,
                vdw=vdw,
                user_kpoints_settings=uks,
                user_potcar_functional="PBE_54",
                user_potcar_settings=custom_ups,
            )
        else:
            vis = MPRelaxSet(
                structure,
                user_incar_settings=uis,
                vdw=vdw,
                user_kpoints_settings=uks,
                user_potcar_functional=upf,
                user_potcar_settings=custom_ups,
            )
    else:
        vis = MPRelaxSet(
            structure,
            user_incar_settings=uis,
            vdw=vdw,
            user_kpoints_settings=uks,
            user_potcar_functional=upf,
            user_potcar_settings=custom_ups,
        )

    if relax_type == "slab_MD":
        start_temp = md_params.get("start_temp", 500)
        end_temp = md_params.get("end_temp", 50)
        nsteps = md_params.get("nsteps", 10000)
        spin_polarized = comp_parameters.get("use_spin", False)
        uis["EDIFF"] = 1.0e-4
        uis["ALGO"] = "Fast"
        uis["LREAL"] = "Auto"
        uis["ISIF"] = 2
        uis["MAXMIX"] = -45
        uis.pop("EDIFFG", None)
        uis.pop("NELM", None)
        uis.pop("PREC", None)
        uis.pop("SYMPREC", None)
        uis.pop("NEDOS", None)
        uis.pop("LORBIT", None)
        vis = MPMDSet(
            structure,
            start_temp=start_temp,
            end_temp=end_temp,
            nsteps=nsteps,
            spin_polarized=spin_polarized,
            user_incar_settings=uis,
            vdw=vdw,
            user_kpoints_settings=uks,
            user_potcar_functional=upf,
            user_potcar_settings=custom_ups,
        )

    return vis


def get_vis(
        struct: Structure,
        comp_params: dict = None,
        calc_type: str = "static",
        custom_uis: dict = None,
        custom_ups: dict = None,
) -> Union[MPRelaxSet, MPStaticSet]:
    """
    Generates a VaspInputSet given the structure, computational parameters and calculation type.

    :param struct: Pymatgen object for the structure.
    :type struct: pymatgen.core.structure.Structure or pymatgen.core.surface.Slab

    :param comp_params: Computational parameters for the VASP calculations.
    :type comp_params: dict

    :param calc_type: Type of calculation, can be 'static' or 'relax'.
    :type calc_type: str

    :param custom_uis: Dictionary of custom user_incar_settings. Defaults to None.
    :type custom_uis: dict, optional

    :param custom_ups: Dictionary of custom user_potcar_settings. Defaults to None.
    :type custom_ups: dict, optional

    :raises ValueError: If calc_type is neither 'static' nor 'relax'.

    :return: VaspInputSet object for the given parameters.
    :rtype: pymatgen.io.vasp.sets.MPRelaxSet or pymatgen.io.vasp.sets.MPStaticSet
    """
    # check if calc_type is either 'static' or 'relax', otherwise raise error
    if calc_type not in ["static", "relax"]:
        raise ValueError(
            f"calc_type must be either 'static' or 'relax', not {calc_type}"
        )

    # if custom_uis and custom_ups are not given, load the default values
    custom_uis = (
        defaults.get("custom_uis") if custom_uis is None else custom_uis
    )
    custom_ups = (
        defaults.get("custom_ups") if custom_ups is None else custom_ups
    )

    # Simple function to generate a vasp input set from a structure, comp_params, and calc_type
    vis = (
        get_custom_vasp_relax_settings
        if calc_type == "relax"
        else get_custom_vasp_static_settings
    )
    struct_type = "slab" if hasattr(struct, "miller_index") else "bulk"
    calc_subtype = "pos_relax" if calc_type == "relax" else "from_scratch"
    return vis(
        struct,
        comp_params,
        f"{struct_type}_{calc_subtype}",
        custom_uis=custom_uis,
        custom_ups=custom_ups,
    )
