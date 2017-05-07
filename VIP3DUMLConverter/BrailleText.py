"""  Contains functions for converting text to Braille
"""


from __future__ import division
import os, sys, re

from solid import *
from solid.utils import *
from math import *

dotHeight = 0.5
dotRadius = 1
charWidth = 7
resolution = 10
lineHeight = 12
#totalHeight = len(testText)*lineHeight
#slabX = 50
slabX = 150
#slabY = totalHeight
charKeys = ["a", "A", "b", "B", "c", "C", "d", "D", "e", "E", "f", "F", "g",
            "G", "h", "H", "i", "I", "j", "J", "k", "K", "l", "L", "m", "M",
            "n", "N", "o", "O", "p", "P", "q", "Q", "r", "R", "s", "S", "t",
            "T", "u", "U", "v", "V", "w", "W", "x", "X", "y", "Y", "z", "Z",
            ",", ";", ":", ".", "!", "(", ")", "?", "\"", "*", "'", "-"]

charValues = [[1], [1], [1, 2], [1, 2],
              [1, 4], [1, 4], [1, 4, 5], [1, 4, 5],
              [1, 5], [1, 5], [1, 2, 4], [1, 2, 4],
              [1, 2, 4, 5], [1, 2, 4, 5], [1, 2, 5],
              [1, 2, 5], [2, 4], [2, 4], [2, 4, 5],
              [2, 4, 5], [1, 3], [1, 3], [1, 2, 3],
              [1, 2, 3], [1, 3, 4], [1, 3, 4], [1, 3, 4, 5],
              [1, 3, 4, 5], [1, 3, 5], [1, 3, 5], [1, 2, 3, 4],
              [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 5],
              [1, 2, 3, 5], [2, 3, 4], [2, 3, 4], [2, 3, 4, 5], [2, 3, 4, 5],
              [1, 3, 6], [1, 3, 6], [1, 2, 3, 6], [1, 2, 3, 6], [2, 4, 5, 6],
              [2, 4, 5, 6], [1, 3, 4, 6], [1, 3, 4, 6], [1, 3, 4, 5, 6], [1, 3, 4, 5, 6],
              [1, 3, 5, 6], [1, 3, 5, 6], [2], [2, 3], [2, 5], [2, 5, 6], [2, 3, 5], [2, 3, 5, 6],
              [2, 3, 5, 6], [2, 3, 6], [2, 3, 6], [3, 5], [3], [3, 6]]

def drawDot(location, dotHeight, dotRadius):
    dot = translate(location)(difference()(cylinder(h=dotHeight, r=dotRadius)))
    return dot

def drawCharacter(charMap, dotHeight, dotRadius): 
    character = []
    for i in range(len(charMap)-1):
        dot = drawDot([math.floor((charMap[i]-1)/3)*(.33*dotHeight)*3*dotRadius*2,
                                     -(charMap[i]-1)%3*(0.33*dotHeight)*3*dotRadius*2, 0], dotHeight,
                                    dotRadius)
        character.append(dot)
    return character 

def drawText(text, dotHeight, dotRadius, charWidth ):
    line_list = []

    for i in range(len(text)-1):

        for j in range(len(charKeys)):

            if charKeys[j] == text[i]:
                line = drawCharacter(charValues[j], dotHeight, dotRadius)

                for character in line:
                    line_list.append (translate([charWidth*i, 0, 0])(character))

                 

    return line_list

def create_text_board(testText, dotHeight, dotRadius, charWidth, lineHeight, totalHeight, slabX):
    final_chars = []
    for i in range(len(testText)):
        text_elem = drawText(testText[i], dotHeight, dotRadius, charWidth)

        for elem in text_elem:
            item = translate([-len(testText[i])*charWidth/2,
                            totalHeight/2-lineHeight*i, 3])(elem)
            final_chars.append(item)

    return final_chars

def text_box(testText, card_width):

    dotHeight = 3
    dotRadius = 1
    charWidth = 7
    resolution = 10
    lineHeight = 12
    totalHeight = len(testText)*lineHeight
    #slabX = 50
    slabX = card_width
    slabY = totalHeight


    slat = translate([0, lineHeight, 0])(cube([slabX, slabY, 1], True))
    text_board = union()(slat, create_text_board(testText,
                                                 dotHeight, dotRadius,
                                                 charWidth, lineHeight,
                                                 totalHeight, slabX))
    print(testText)
    return text_board