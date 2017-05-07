from __future__ import division
import os, sys, re

from solid import *
from solid.utils import *

def assembly (new_lines, new_cards):
    '''
        Assembles the transformed cards and lines into one diagram.

        Args: list new_lines and new_cards transformed cards and connectors from xml]
        now 3d

        Return: The finished diagram as solid python code
    '''
    final_diagram =(union()(new_lines, new_cards, forward(10)(right(100)(down(3)((cube([500,300,1], False)))))))
    return final_diagram

 #right(150)(cube([500,300,1], False))