""" Contains main function required to convert the xml document into
    an .scad file.  Once the .scad file is made the file can then be
    converted to stl via OpenSCAD
"""

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from Classes2D import *
from Classes3D import *
from openSCAD3DAssembly import *
from XMLParser import *
from solid.solidpython import scad_render_to_file
import argparse

PARSER = argparse.ArgumentParser()
PARSER.add_argument("--file_path", type=str, default="./", help="file_path")
PARSER.add_argument("--file_name", type=str, default="./", help="file_name")
ARGS = PARSER.parse_args()

#Path for the VP XML output to be parsed
#TODO: Maybe figure out a more efficient method for 
# accessing file
FILEPATH = ARGS.file_path

#Parse the XML from VP
TREE = ET.ElementTree(file=FILEPATH)

# Retrieve root node from TREE and store it
ROOT = TREE.getroot()

#Find  model and diagram children and store them
DIAGRAMS = ROOT.find('Diagrams')
MODELS = ROOT.find('Models')

#Declare a list to store all the diagrams

# TODO: Might be a good idea to get rid of this feature
#       only 1 diagram processed at a time
DIAGRAMLIST = []

# Loop through each diagram and pass it to class ParsedDiagram
for diagram in DIAGRAMS:
    d = ParsedDiagram(diagram, MODELS)
    #Append list of diagrams with instance of a ParsedDiagram
    DIAGRAMLIST.append(d)

for diagram in DIAGRAMLIST:
    #Dictionary for diagram attributes
    d = {}
    #Dictionary for storing aggregation
    #and composition information and message info


    agg_dict = diagram.get_agg_relationship_info()

    msg_dict = diagram.get_msg_relationship_info()

    #Create lists of 2d shape and line instances
    diagram_2d_shapes = []
    diagram_2d_lines = []

    #Establish contents of diagram attrib dictionary
    for key in diagram.keys():
        d[key] = diagram.get(key)

    #Instantiate an instance of a 2d diagram
    diagram_layout = Diagram2D(d, diagram.tag)

    #Instantiate instances of 2d shapes and add them to list
    # of 2d shapes
    for shape in diagram.shapes:
        s = {}
        for key in shape.keys():
            s[key] = shape.get(key)
        shape_instance = Shape2D(s, shape.tag)
        diagram_2d_shapes.append(shape_instance)

    #Instantiate instances of 2d connectors and add them to list
    # of 2d lines
    for connector in diagram.connectors:
        c = {}
        for key in connector.keys():
            c[key] = connector.get(key)
        connector_instance = Connector2D(c, connector.tag)
        diagram_2d_lines.append(connector_instance)

    #Establish 3d print area (typically 215mm)
    new_diagram_width = 1510

    #Scale dim of new diagram to that of xml spec
    # create normalizing ratios for old diagram to
    # new diagram conversion
    orig_height = diagram_layout.get_diagram_height()
    orig_width = diagram_layout.get_diagram_width()
    print(orig_height, orig_width)

    new_diagram_height = (orig_height/orig_width)*new_diagram_width

    width_norm = float(new_diagram_width)/float(orig_width)

    height_norm = float(new_diagram_height)/float(orig_height)

    #Create list to store 3d shapes and connectors
    shapes_3d = []

    lines_3d = []



    #Loop through 2d shapes and create 3D instances of
    # all shapes and add them to 3d shapes list
    for shape in diagram_2d_shapes:
        s = Builder.build_shape(shape.shape_type,
                                shape.get_attribs(),
                                width_norm, height_norm)
        shapes_3d.append(s)

    #Create dictionary to store shape ID as key and
    # coord of shape as tuple for value
    id_coord = {}
    for shape in shapes_3d:
        id_coord[shape.shape_get_id()] = shape.shape_3d_location()

    #Loop through 2d lines and create 3d instances of lines making
    #use of id_coord dict to establish to and from points.
   #  Add these objects to the 3d lines list.
    for line in diagram_2d_lines:
        l = Builder.build_connector(line.get_connector_type(),
                                    line.get_connector_2d_info(),
                                    id_coord[line.get_from()], id_coord[line.get_to()],
                                    msg_dict, agg_dict, id_coord)
        lines_3d.append(l)
    #Now call the respective functions for the 3d shapes and
    # lines list to create 3d cards and lines and store in lists
    scad_lines = []
    scad_shapes = []

    for shape in shapes_3d:
        scad_shapes.append(Builder.make_3d_shape(shape))

    for line in lines_3d:
        scad_lines.append(Builder.make_3d_connector(line))

    #Use assembly function to put the pieces together
        final_product = assembly(scad_lines, scad_shapes)

    SEGMENTS = 48
    #file_name = input('File Name: ')
    file_name = ARGS.file_name
    #Create an openSCAD file from finished_product
    #TODO: this is a klunky way to make file and needs fixed 

scad_render_to_file(final_product, file_header='$fn = %s;'%SEGMENTS, include_orig_code=True)

