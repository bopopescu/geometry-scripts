"""
Script from Chris Rogers to visualize geometry in x-z, y-z sections

Supply the geometry ParentGeometryFile.dat as argument

Output is: materials.png materials.ps materials.root
"""

import Configuration
import maus_cpp.globals
import maus_cpp.material
import xboa.common
import ROOT
import time

VERBOSE = False

def initialise_maus():
    configuration = Configuration.Configuration().\
                                          getConfigJSON(command_line_args=True)
    maus_cpp.globals.birth(configuration)

MATERIAL_LIST = []
def material_to_colour(material):
    global MATERIAL_LIST
    if material[0:3] == "G4_":
        material = material[3:]
    if material not in MATERIAL_LIST:
        MATERIAL_LIST.append(material)
    if material in ("Galactic"):
        return None
    if material in ("Fe"): # "kill volumes"
        return 1
    if material in ("TUFNOL"):
        return 4
    if material in ("Zn", "Cu", "W", "TUNGSTEN", "BRASS", "STEEL", "IRON"):
        return 2
    if material in ("TAM1000"):
        return 9
    if material in ("Al", "ALUMINUM"):
        return 1
    if material in ("lH2", "MICE_LITHIUM_HYDRIDE", "LITHIUM_HYDRIDE"):
        return 6
    if material in ("AIR"):
        return 5
    if material in ("He", "Helium", "HELIUM"):
        return 7
    print "UNRECOGNISED MATERIAL", material
    return 1

def get_materials(radius, z_start, z_end, z_step):
    x = radius
    material = None
    material_start = []
    n_steps = int((z_end-z_start)/z_step)
    for i in range(n_steps):
        z = z_step*i+z_start
        maus_cpp.material.set_position(x, 0., z)
        material_data = maus_cpp.material.get_material_data()
        if VERBOSE == True:
            print x, z, material
        new_material = material_data['name']
        if new_material != material:
            material = new_material
            material_start.append({"x":x, "z":z, "material":material})
    return material_start

ROOT_GRAPHS = []
def plot_materials(r_start, r_end, r_step, z_start, z_end, z_step):
    global ROOT_GRAPHS
    ROOT.gROOT.SetBatch(1)
    canvas = xboa.common.make_root_canvas("materials")
    canvas.SetWindowSize(1900, 1000)
    n_steps = int((r_end-r_start)/r_step)
    hist = ROOT.TH2D("materials", ";z [mm]; x [mm]", 2000, z_start, z_end, 1000, r_start, r_end)
    hist.SetStats(False)
    #hist.GetYaxis().SetNdivisions(520)
    #hist.GetXaxis().SetNdivisions(520)
    #canvas.SetGridx()
    #canvas.SetGridy()
    hist.Draw()
    ROOT_GRAPHS.append(hist)
    for i in range(n_steps):
        r = r_step*i+r_start
        materials = get_materials(r, z_start,z_end, z_step)
        print "At radius", r, "found", len(materials), "materials using", len(ROOT_GRAPHS), "root objects"
        for i, material in enumerate(materials):
            #print material['material']
            colour = material_to_colour(material["material"])
            if colour == None:
                continue
            z_min = material["z"]
            radius = material["x"]
            if i+1 >= len(materials):
                z_max = z_end+1
            else:
                z_max = materials[i+1]["z"]
            if i == 0:
                z_min -= 1
            graph = ROOT.TGraph(2)
            graph.SetPoint(0, z_min, radius)
            graph.SetPoint(1, z_max, radius)
            graph.SetLineColor(colour)
            graph.SetMarkerColor(colour)
            graph.SetMarkerStyle(6)
            graph.SetLineWidth(2)
            graph.Draw("plsame")
            ROOT_GRAPHS.append(graph)
            if i % 10 == 0:
                canvas.Update()

    canvas.Update()
    for format in "png", "eps", "root":
        canvas.Print("materials."+format)

def main():
    initialise_maus()
    old_time = time.time()
    plot_materials(0.0, 200.0, 0.5, 13660., 13860., 0.01)
    print "Plotting took", time.time() - old_time, "seconds"
    print "Found the following materials", MATERIAL_LIST

if __name__ == "__main__":
    main()
    raw_input()
