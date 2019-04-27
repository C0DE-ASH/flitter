#!/usr/bin/python
"""
CEG 7560
Visual & Image Process
Assignment 3 - Flitter Data

Matthew Kijowski
matthewkijowski@gmail.com
w114mek
"""

import vtk
import pandas as pd
import numpy as np
import sys

def main():
    user_file   = "./data/M2/Flitter_Names.txt"
    friend_file = "./data/M2/Links_Table.txt"
    colors = vtk.vtkNamedColors()

    graph = vtk.vtkMutableDirectedGraph()

    users = vtk.vtkStringArray()
    names = pd.read_csv( user_file, delimiter = '   ')
    friends = pd.read_csv( friend_file, delimiter = '   ')
    for i in range(0, len(names)):
        graph.addVertex()
        username.InsertNextValue(names.username[i])
        userid.InsertNextValue(names.userid[i])
    graph.GetVertexData().AddArray(username)
    graph.GetVertexData().AddArray(userid)

