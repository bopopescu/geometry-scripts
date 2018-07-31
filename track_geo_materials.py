"""
Script to print materials in the geometry at each x,y:z step
--> print out when material changes
"""

import Configuration
import maus_cpp.globals
import maus_cpp.material
import numpy as np

def initialise_maus():
    configuration = Configuration.Configuration().\
                                          getConfigJSON(command_line_args=True)
    maus_cpp.globals.birth(configuration)

def my_range(zmin, zmax, nz):
    ran = np.linspace(zmin, zmax, nz)
    return ran[np.nonzero(ran)]

def print_materials():
    # specify the list of x values you want to track through
    for x in [110]:
        material = None
        for z in my_range(13680.0, 13780.0, 4000):
            maus_cpp.material.set_position(x, 0., z)
            material_data = maus_cpp.material.get_material_data()
            new_material = material_data['name']
            # print every step regardless of material change -- 0.01 mm
            print x, z, material, new_material
            if new_material != material:
                material = new_material
                # print x, z, material if material has changed
                print str(x).ljust(10), str(z).ljust(10), material.ljust(20), material_data["name"]
        print

def main():
    initialise_maus()
    print_materials()

if __name__ == "__main__":
    main()
