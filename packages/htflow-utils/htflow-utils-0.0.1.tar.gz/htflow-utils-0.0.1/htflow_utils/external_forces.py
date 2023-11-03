from typing import Union

import numpy as np
from pymatgen.core.interface import Interface
from pymatgen.core.surface import Slab

from htflow_utils.shaper import Shaper


def ext_pressure_to_force_array(
        slab: Union[Slab, Interface],
        external_pressure: float,
        tol: float = 0.25,
) -> list:
    """
    This function takes a Slab or Interface object and a pressure and returns a force array.


    :param slab: Slab or Interface object
    :type slab: pymatgen.core.surface.Slab or pymatgen.core.interface.Interface

    :param external_pressure: The pressure to be applied to the structure in units of GPa.
    :type external_pressure: float

    :param tol: float, optional
        The tolerance used to determine the top and bottom layers of the slab. The
        default is 0.1.

    :return: The force array to be applied to the structure in units of eV/Angstrom.
    :rtype: list

    .. note::
        The force array is a list of floats, where each three consecutive floats
        represent the force on a site in the slab. The force array can be used to
        apply an external pressure to the slab in VASP.
        We have to make sure to do the right unit conversions. The pressure is
        given in GPa, and the force array is in eV/Angstrom. The force array is
        calculated as follows:
        - The area of the slab is calculated.
        - The force on the top and bottom layers is calculated using the area and
            the number of sites in the top and bottom layers.
        - The force array is created with all x and y components set to zero, and
            the z component set to the force on the top and bottom layers for the
            right sites, and zero for the rest.
    """

    try:
        area = slab.surface_area
    except AttributeError:
        area = slab.interface_properties["area"]

    # get a layer dictionary that has the layer fractional z-coordinates as
    # keys, and the layer sites as values:

    layers = Shaper.get_layers(slab, tol)

    # get the sites of the top and bottom layers:
    top_layer = layers[max(layers)]
    bot_layer = layers[min(layers)]

    # get the force on the top and bottom layers
    # We start with GPa (1e9Nm/m^3) and want to end up with eV/Angstrom:
    # Nm_to_eV = 6.241509074461e18
    # conversion_factor = Nm_to_eV * 1e9 / 1e30
    # avoid using large numbers and do this in one step:
    conversion_factor = 6.241509074461e-3
    external_pressure *= conversion_factor
    external_force = np.round(external_pressure * area, 4)
    force_top = -external_force / len(top_layer)
    force_bot = external_force / len(bot_layer)

    # create the force array, making sure that all x and y components are zero.
    # the z component is the force on the top and bottom layers for the right
    # sites, and zero for the rest:

    force_array = []
    for i, site in enumerate(slab.sites):
        if i in top_layer:
            force_array.extend([0.0, 0.0, force_top])
        elif i in bot_layer:
            force_array.extend([0.0, 0.0, force_bot])
        else:
            force_array.extend([0.0, 0.0, 0.0])

    return force_array


# function for changing the force_array to a string, which groups 0.0s
# together, and removes the brackets and commas. 0.0 values are grouped
# together to reduce the size of the force array string, which is more
# convenient for the user to read and can be understood by VASP.
def force_array_to_string(force_array: Union[list, np.array]) -> str:
    """
    This function takes a force array and returns a string readable by VASP.

    :param force_array: The force array to be converted to a string.
    :type force_array: list or numpy array

    :return: The force array as a string.
    :rtype: str
    """

    # first, slice the array in a way that blocks of 0.0 values are grouped
    # together and non-zero values are also grouped together:
    force_array = np.array(force_array)
    split_array = np.split(force_array, np.where(np.diff(force_array))[0] + 1)

    # now loop over the blocks, and if the whole block contains only 0.0s,
    # replace the block by "N*0", where N is the length of the block. If the
    # block contains non-zero values, replace the block by the values in the
    # block, separated by spaces:
    force_string = ""
    for block in split_array:
        if not np.any(block):
            force_string += str(len(block)) + "*0 "
        else:
            for value in block:
                force_string += str(value) + " "

    return force_string.strip()
