# additional functions for workflows that require atomate, and
# thus also FireWorks to function.


from copy import deepcopy
from typing import Union, Any

from htflow_utils.db_tools import VaspDB

try:
    from atomate.vasp.firetasks import RunVaspFake
    from atomate.vasp.fireworks import StaticFW, ScanOptimizeFW, OptimizeFW
    from atomate.vasp.powerups import add_modify_incar
    from fireworks import Workflow
except ImportError:
    print("******************************************************")
    print("atomate/FireWorks is not installed.")
    print("Please install htflow_utils with the workflow option:")
    print("pip install htflow_utils[workflow]")
    print("******************************************************")
    raise ImportError

from pymatgen.core.interface import Interface
from pymatgen.core.structure import Structure
from pymatgen.core.surface import Slab
from pymatgen.io.vasp.sets import (
    MPScanRelaxSet,
    MPRelaxSet,
    MPScanStaticSet,
    MPStaticSet,
    VaspInputSet,
)


def get_calc_wf(
        struct: Structure,
        vis: Union[MPStaticSet, MPRelaxSet],
        tag: str,
        add_static: bool = True,
        force_calc: bool = False,
        db_file: str = "auto",
) -> Union[Workflow, None]:
    """
    Generates a Workflow for the given parameters.

    :param struct: Pymatgen object for the structure.
    :type struct: pymatgen.core.structure.Structure or pymatgen.core.surface.Slab

    :param vis: VaspInputSet object for the given structure.
    :type vis: pymatgen.io.vasp.sets.MPRelaxSet or pymatgen.io.vasp.sets.MPStaticSet

    :param tag: Task label assigned to the calculation.
    :type tag: str

    :param add_static: Selects if a static follow-up calculation should be run at the relaxed
        structure. Defaults to True.
    :type add_static: bool, optional

    :param force_calc: If True, the calculation will be run even if a task with the given tag
        already exists. Defaults to False.
    :type force_calc: bool, optional

    :param db_file: Full path of the db.json file. Defaults to 'auto', in which case the path
        is checked from the environment variable FW_CONFIG_FILE.
    :type db_file: str, optional

    :return: Workflow object for a VASP calculation.
    :rtype: fireworks.core.firework.Workflow
    """
    # Simple function to make a Workflow from a structure, vis, and a tag
    print("Generating Workflow for", tag)
    nav_low = VaspDB(db_file=db_file, high_level=False)
    fltr_low = {"task_label": tag}
    result_low = nav_low.find_data("tasks", fltr_low)
    if result_low and not force_calc:
        print(f"Found existing task with tag {tag}. Skipping...")
        return None
    if vis.incar.get("NSW", 0) > 0:
        wf = dynamic_relax_swf([[struct, vis, tag]], add_static=add_static)
    else:
        fw = StaticFW(structure=struct, name=tag, vasp_input_set=vis)
        wf = Workflow.from_Firework(fw, name=tag)
        wf = add_modify_incar(wf)
    return wf


def dynamic_relax_swf(
        inputs_list: list,
        wf_name: str = "Dynamically generated Workflow",
        add_static: bool = False,
        prerelax_system: bool = True,
        prerelax_calculator: str = "m3gnet",
        prerelax_kwargs=None,
        db_file="auto",
) -> Any | None:
    """Generate a workflow with relaxations for PBE or SCAN functionals.

    A base workflow that uses an input list of lists with structures, vasp-
    input-sets and tags (to find the calculation again in the Fireworks
    database) to create a workflow. Many structures can be optimized at once.
    If the 'SCAN' (or '2rSCAN') is set as METAGGA value for any of the vasp-
    input-sets, two ScanOptimizeFW are run in succession for each structure,
    if not, a single OptimizeFW is run. An add_modify_incar powerup from
    atomate is applied to the final workflow. Static calculations can be
    added in the end if the 'add_static' flag is set to True. This will result
    in the input names pointing to the static follow-up run. Those static runs
    will start from the WAVECAR of the previous relaxation and provide more
    accurate total energies.

    :param inputs_list: List of lists of the type
        [[structure_n, vasp_input_set_n, name_n], ...]
    :type inputs_list: list of lists

    :param wf_name: Name for the created workflow.
        Defaults to 'Dynamically generated Workflow'
    :type wf_name: str, optional

    :param add_static: Selects if a static follow-up calculation should be run
        at the relaxed positions starting from the CHGCAR
        of the relaxation run. Defaults to False.
    :type add_static: bool, optional

    :param prerelax_system: Selects if the structure should be pre-relaxed
            using a simple potential before the main DFT relaxation.
            Defaults to True.
    :type prerelax_system: bool, optional

    :param prerelax_calculator: Selects the potential to be used for the pre-relaxation.
            Defaults to 'm3gnet'.
    :type prerelax_calculator: str, optional

    :param prerelax_kwargs: Keyword arguments for the pre-relaxation.
            Defaults to None.
    :type prerelax_kwargs: dict, optional

    :param db_file: Full path of the db.json file. Defaults to 'auto', in which case the path
        is checked from the environment variable FW_CONFIG_FILE.
    :type db_file: str, optional

    :return: A workflow intended to relax a structure or many structures.
    :rtype: fireworks.core.firework.Workflow
    """
    if prerelax_kwargs is None:
        prerelax_kwargs = {}
    fw_list = []
    for i in range(len(inputs_list)):
        struct = inputs_list[i][0]
        if prerelax_system:
            if "return_trajectory" in prerelax_kwargs:
                prerelax_kwargs.pop("return_trajectory")
            # make sure the pre-relaxation does not relax the cell
            # unless the user explicitly asks for it.
            relax_cell = prerelax_kwargs.pop("relax_cell", False)
            # unfortunately ASE does not support fixing sites in only
            # one direction, so we have no option to relax only
            # z-direction for now. If selective dynamics are not
            # [True, True, True] or [False, False, False], a
            # ValueError is raised.
            try:
                struct = struct.relax(
                    calculator=prerelax_calculator,
                    return_trajectory=False,
                    relax_cell=relax_cell,
                    **prerelax_kwargs,
                )
            except ValueError:
                pass
        vis = inputs_list[i][1]
        name = inputs_list[i][2]
        if add_static:
            if "scan" in vis.incar.get("METAGGA", "").lower():
                fws = scan_relax_with_static(struct, vis, name)
                fw_list.extend(fws)
            else:
                fws = pbe_relax_with_static(struct, vis, name)
                fw_list.extend(fws)
        else:
            if "scan" in vis.incar.get("METAGGA", "").lower():
                fws = scan_relax(struct, vis, name)
                fw_list.extend(fws)
            else:
                fws = pbe_relax(struct, vis, name)
                fw_list.extend(fws)

    db = VaspDB(db_file=db_file, high_level=False)
    task_labels = [fw.name.split('-', 1)[1] for fw in fw_list]
    completed_tasks = [
        task["task_label"]
        for task in db.find_many_data(
            "tasks", {"task_label": {"$in": task_labels}}, {"task_label": 1}
        )
    ]
    fw_list = [fw for fw in fw_list if fw.name.split('-', 1)[1] not in completed_tasks]
    processed_fws = set()

    # Use a while loop to iteratively process objects with parents
    while fw_list:
        current_object = fw_list.pop()
        processed_fws.add(current_object)

        # Check if the current object has parents
        if current_object.parents:
            for parent in current_object.parents:
                # Check if the parent has already been processed
                if parent not in processed_fws:
                    # Add the parent to the list for further processing
                    fw_list.append(parent)

    # convert the processed_fws set to a list
    fw_list = list(processed_fws)

    if fw_list:
        wf = Workflow(fireworks=fw_list, name=wf_name)
        return add_modify_incar(wf)
    else:
        return None


def scan_relax_with_static(
        struct: Union[Structure, Slab, Interface], vis: VaspInputSet, name: str
):
    """Relax a structure with SCAN and do a followup static calculation.

    Links a StaticFW to two ScanOptimizeFWs. The passed name is given to the
    static calculation, while the PBEsol pre-relaxation will have a
    "_PBEsolPreCalc" postfix, and the SCAN relaxation a "_SCAN_relax" postfix
    to the name.

    :param struct: Pymatgen object for the structure.
    :type struct: pymatgen.core.structure.Structure

    :param vis: A vasp input set
    :type vis: pymatgen.io.vasp.sets.VaspInputSet

    :param name: This will become the task_label in the FireWorks DB. Used to find the calculation later.
    :type name: str

    :return: List of fireworks and a dictionary of links between fireworks
    :rtype: list, dict
    """
    gga_vis = deepcopy(vis)
    static_vis = deepcopy(vis)
    gga_vis.user_incar_settings["ALGO"] = "Normal"
    if vis.user_incar_settings.get("LDIPOL", False):
        gga_vis.user_incar_settings["LDIPOL"] = False

    vis.user_incar_settings["LWAVE"] = True
    vis_params = {
        "user_incar_settings": vis.user_incar_settings,
        "user_kpoints_settings": vis.user_kpoints_settings,
        "user_potcar_functional": vis.potcar_functional,
        "vdw": vis.vdw,
    }
    fw_1 = ScanOptimizeFW(
        structure=struct,
        name=name + "_PBEsolPreCalc",
        vasp_input_set=gga_vis,
        vasp_input_set_params={"vdw": vis.vdw},
        spec={"_preserve_fworker": True},
    )
    fw_2 = ScanOptimizeFW(
        structure=struct,
        vasp_input_set_params=vis_params,
        parents=fw_1,
        prev_calc_loc=True,
        name=name + "_SCAN_relax",
        spec={"_preserve_fworker": True},
    )
    static_vis.user_incar_settings["EDIFF"] = 1e-07
    static_vis.user_incar_settings["ISMEAR"] = -5
    static_vis.user_incar_settings["ALGO"] = "Normal"
    static_vis.user_incar_settings["SIGMA"] = 0.05
    static_vis.user_incar_settings["ISTART"] = 1
    static_vis.user_incar_settings["ICHARG"] = 0
    static_vis.user_incar_settings["NELMDL"] = 0
    static_vis_params = {
        "user_incar_settings": static_vis.user_incar_settings,
        "user_kpoints_settings": static_vis.user_kpoints_settings,
        "user_potcar_functional": static_vis.potcar_functional,
        "user_potcar_settings": static_vis.user_potcar_settings,
        "vdw": static_vis.vdw,
    }
    fw_3 = StaticFW(
        structure=struct,
        vasp_input_set_params=static_vis_params,
        parents=fw_2,
        prev_calc_loc=True,
        additional_files_from_prev_calc=["WAVECAR"],
        name=name,
    )
    return [fw_1, fw_2, fw_3]


def pbe_relax_with_static(
        struct: Union[Structure, Slab, Interface],
        vis: Union[MPStaticSet, MPRelaxSet],
        name: str,
) -> list[Union[OptimizeFW, StaticFW]]:
    """Relax a structure with PBE and do a followup static calculation.

    Links a StaticFW to an OptimizeFW. The passed name is given to the static
    calculation, while the relaxation will have a "_PBE_relax" postfix to the
    name.

    :param struct: Pymatgen object for the structure.
    :type struct: pymatgen.core.structure.Structure | pymatgen.core.surface.Slab | pymatgen.core.surface.Interface

    :param vis: A vasp input set
    :type vis: pymatgen.io.vasp.sets.MPStaticSet | pymatgen.io.vasp.sets.MPRelaxSet

    :param name: This will become the task_label in the FireWorks DB. Used to find the calculation later.
    :type name: str

    :return: List of fireworks and a dictionary of links between fireworks.
    :rtype: list, dict
    """
    vis.user_incar_settings["LWAVE"] = True
    static_vis = deepcopy(vis)
    if vis.user_incar_settings.get("LDIPOL", False):
        pre_calc_vis = deepcopy(vis)
        pre_calc_vis.user_incar_settings["NSW"] = 0
        pre_calc_vis.user_incar_settings["LDIPOL"] = False
    else:
        pre_calc_vis = False

    static_vis.user_incar_settings["ISMEAR"] = -5
    static_vis.user_incar_settings["EDIFF"] = 1e-07
    static_vis.user_incar_settings["SIGMA"] = 0.05
    static_vis.user_incar_settings["ISTART"] = 1
    static_vis.user_incar_settings["ICHARG"] = 0
    static_vis.user_incar_settings["NELMDL"] = 0
    static_vis.user_incar_settings["LWAVE"] = False
    vis_params = {
        "user_incar_settings": static_vis.user_incar_settings,
        "user_kpoints_settings": vis.user_kpoints_settings,
        "user_potcar_functional": vis.potcar_functional,
        "user_potcar_settings": vis.user_potcar_settings,
        "vdw": vis.vdw,
    }

    if pre_calc_vis:
        fw_0 = StaticFW(
            structure=struct,
            name=name + "_NoLdipolPrecalc",
            vasp_input_set=pre_calc_vis,
            spec={"_preserve_fworker": True},
        )
        fw_1 = OptimizeFW(
            structure=struct,
            vasp_input_set=vis,
            parents=fw_0,
            prev_calc_loc=True,
            additional_files_from_prev_calc=["WAVECAR"],
            name=name + "_PBE_relax",
            spec={"_preserve_fworker": True},
        )
        fw_2 = StaticFW(
            structure=struct,
            vasp_input_set_params=vis_params,
            parents=fw_1,
            prev_calc_loc=True,
            additional_files_from_prev_calc=["WAVECAR"],
            name=name,
        )
        return [fw_0, fw_1, fw_2]
    else:
        fw_1 = OptimizeFW(
            structure=struct,
            name=name + "_PBE_relax",
            vasp_input_set=vis,
            spec={"_preserve_fworker": True},
        )
        fw_2 = StaticFW(
            structure=struct,
            vasp_input_set_params=vis_params,
            parents=fw_1,
            prev_calc_loc=True,
            additional_files_from_prev_calc=["WAVECAR"],
            name=name,
        )
        return [fw_1, fw_2]


def scan_relax(
        struct: Union[Structure, Slab, Interface],
        vis: Union[MPScanStaticSet, MPScanRelaxSet],
        name: str,
) -> list[ScanOptimizeFW]:
    """Relax a structure with SCAN.

    Links two ScanOptimizeFWs. The passed name is given to the second one,
    which is a SCAN relaxation, while the PBEsol pre-relaxation will have a
    "_PBEsolPreCalc" postfix.

    :param struct: Pymatgen object for the structure.
    :type struct: pymatgen.core.structure.Structure | pymatgen.core.surface.Slab | pymatgen.core.surface.Interface

    :param vis: A vasp input set
    :type vis: pymatgen.io.vasp.sets.MPScanStaticSet | pymatgen.io.vasp.sets.MPScanRelaxSet

    :param name: This will become the task_label in the FireWorks DB. Used to find the calculation later.
    :type name: str

    :return: List of fireworks and a dictionary of links between fireworks.
    :rtype: list, dict
    """
    gga_vis = deepcopy(vis)
    gga_vis.user_incar_settings["ALGO"] = "Normal"
    if vis.user_incar_settings.get("LDIPOL", False):
        gga_vis.user_incar_settings["LDIPOL"] = False
    vis_params = {
        "user_incar_settings": vis.user_incar_settings,
        "user_kpoints_settings": vis.user_kpoints_settings,
        "user_potcar_functional": vis.potcar_functional,
        "user_potcar_settings": vis.user_potcar_settings,
        "vdw": vis.vdw,
    }
    fw_1 = ScanOptimizeFW(
        structure=struct,
        name=name + "_PBEsolPreCalc",
        vasp_input_set=gga_vis,
        vasp_input_set_params={"vdw": vis.vdw},
        spec={"_preserve_fworker": True},
    )
    fw_2 = ScanOptimizeFW(
        structure=struct,
        vasp_input_set_params=vis_params,
        parents=fw_1,
        prev_calc_loc=True,
        name=name,
    )
    return [fw_1, fw_2]


def pbe_relax(
        struct: Union[Structure, Slab, Interface], vis: MPRelaxSet, name: str
) -> list[StaticFW | OptimizeFW] | list[OptimizeFW]:
    """Relax a structure with PBE.

    Use an OptimizeFW to relax a structure. The name will be assigned to the
    task_label of the calculation.

    :param struct: Pymatgen object for the structure.
    :type struct: pymatgen.core.structure.Structure | pymatgen.core.surface.Slab | pymatgen.core.surface.Interface

    :param vis: A vasp input set
    :type vis: pymatgen.io.vasp.sets.MPRelaxSet

    :param name: This will become the task_label in the FireWorks DB. Used to find the calculation later.
    :type name: str

    :return: List of fireworks and a dictionary of links between fireworks.
    :rtype: list, dict
    """
    if vis.user_incar_settings.get("LDIPOL", False):
        pre_calc_vis = deepcopy(vis)
        pre_calc_vis.user_incar_settings["NSW"] = 0
        pre_calc_vis.user_incar_settings["LDIPOL"] = False
    else:
        pre_calc_vis = False

    if pre_calc_vis:
        fw_0 = StaticFW(
            structure=struct,
            name=name + "_NoLdipolPrecalc",
            vasp_input_set=pre_calc_vis,
            spec={"_preserve_fworker": True},
        )
        fw_1 = OptimizeFW(
            structure=struct,
            vasp_input_set=vis,
            parents=fw_0,
            prev_calc_loc=True,
            additional_files_from_prev_calc=["WAVECAR"],
            name=name,
        )
        return [fw_0, fw_1]
    else:
        fw = OptimizeFW(structure=struct, name=name, vasp_input_set=vis)
        return [fw]


def use_fake_vasp(
        original_wf: Workflow,
        ref_dir: str,
        params_to_check: list = None,
        check_incar: bool = True,
        check_kpoints: bool = True,
        check_poscar: bool = True,
        check_potcar: bool = True,
        clear_inputs: bool = True,
) -> Workflow:
    """
    Replaces all tasks with "RunVasp" (e.g. RunVaspDirect) to be RunVaspFake.
    Thus, we do not actually run VASP but copy pre-determined inputs and
    outputs.

    :param original_wf: Original workflow to modify
    :type original_wf: Workflow

    :param ref_dir: Directory containing the reference files
    :type ref_dir: str

    :param params_to_check: List of parameters to check. If None. Defaults to
        ["ISPIN", "ENCUT", "ISMEAR", "SIGMA", "IBRION", "LORBIT", "NBANDS",
        "LMAXMIX"]
    :type params_to_check: list

    :param check_incar: Whether to check the INCAR file. Defaults to True.
    :type check_incar: bool

    :param check_kpoints: Whether to check the KPOINTS file. Defaults to True.
    :type check_kpoints: bool

    :param check_poscar: Whether to check the POSCAR file. Defaults to True.
    :type check_poscar: bool

    :param check_potcar: Whether to check the POTCAR file. Defaults to True.
    :type check_potcar: bool

    :param clear_inputs: Whether to clear the inputs of the RunVaspFake tasks,
        defaults to True.
    :type clear_inputs: bool

    :return: Workflow with RunVaspFake tasks
    :rtype: Workflow
    """
    if not params_to_check:
        params_to_check = [
            "ISPIN",
            "ENCUT",
            "ISMEAR",
            "SIGMA",
            "IBRION",
            "LORBIT",
            "NBANDS",
            "LMAXMIX",
        ]

    for idx_fw, fw in enumerate(original_wf.fws):
        for idx_t, t in enumerate(fw.tasks):
            t_str = str(t)
            t_job_type = t.get("job_type")
            if "RunVasp" in t_str:
                original_wf.fws[idx_fw].tasks[idx_t] = RunVaspFake(
                    ref_dir=ref_dir,
                    params_to_check=params_to_check,
                    check_incar=check_incar,
                    check_kpoints=check_kpoints,
                    check_poscar=check_poscar,
                    check_potcar=check_potcar,
                    clear_inputs=clear_inputs,
                )

    return original_wf
