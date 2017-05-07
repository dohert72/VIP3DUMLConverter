# VIP3DUMLConverter
Converts XML output descriptions of UML diagrams and converts them into a 3D printable format.


VIP3DUMLConverter:
===================
-BrailleText.py:
    Methods for converting plain text into Braille

-Classes2d.py:
    Creates 2D representations for the shapes described in UML XML file

-Classe3D.py:
    Translates the 2D shapes into the 3D shapes perscribed by the Solid Python library

-ConverterMain.py:
    Main script for executing conversion to .scad file

-OpenScad3DAssembly.py:
    Assembles the 3d shapes into one 3d diagram board in .scad format

-OpenScadShapes.py:
    Miscillaneous shapes such as triangles and arrows that are not a part of the 
    solid library but are useful in implementing the 3D UML

-XMLParser.py:
    Functions for parsing XML structure of VP output for UML designs

Installation, Configuration, and Running Program:
=================================================
Installation:
--------------
1- To download the source files for VIP3DUMLConverter, one can simply clone
   from the git (https://github.com/dohert72/VIP3DUMLConverter.git), run setup, or 
   download the files individually.
2- Dependency libraries that need to be installed can be retrieved by exexuting a
   pip install of the elements in requirements.txt that can be found in the git.

Other Configuration Notes:
--------------------------
* Part of the tool chain requires the use of the openSCAD application for 
  conversion of the .scad file into the stl format for the 3D printers. You will
  also likely find openSCAD as a useful tool for previewing the models generated by the 
  VIP3DUMLConverter. 
  1- Visit the openSCAD website at http://www.openscad.org in order to download
  2- Note that for ease of execution, the openscad converter is leveraged from command line/terminal
     this will require you to add the location of the downloaded program file to your PATH environment 
     variable

Running:
--------
By running the batch file ConvertToSTL and specifying the path of the xml file from visual paradigm, 
the conversion to .scad and then conversion to stl will be executed, producing the printable file.