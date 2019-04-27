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
    strategy = "Circular"
    ELstrategy = "Pass Through"
    #Requires vtkboost
    #strategy = "CosmicTree"

    user_file   = "./data/M2/Flitter_Names.txt"
    friend_file = "./data/M2/Links_Table.txt"
    colors = vtk.vtkNamedColors()

    graph = vtk.vtkMutableDirectedGraph()
    username = vtk.vtkStringArray()
    userid   = vtk.vtkIntArray()
    graph.GetVertexData().SetPedigreeIds(userid)

    ## Read user_file and friend_file with numpy
    names = pd.read_csv( user_file, delimiter = '\t')
    friends = pd.read_csv( friend_file, delimiter = '\t')

    v = []
    for i in range(0, len(names)):
        v.append(graph.AddVertex())
        username.InsertNextValue(names.username[i])
        userid.InsertNextValue(names.userid[i])
    graph.GetVertexData().AddArray(username)
    graph.GetVertexData().AddArray(userid)

    ### Ignore the last 12 lines becuase they are just city&country data
    ### And I don't have vertexes for them yet
    for i in range(0, len(friends)-12):
        graph.AddEdge(v[friends.ID1[i]-1],v[friends.ID2[i]-1])

    #return graph

    graphLayoutView = vtk.vtkGraphLayoutView()
    graphLayoutView.AddRepresentationFromInput(graph)
    graphLayoutView.SetLayoutStrategy(strategy)
    graphLayoutView.SetEdgeLayoutStrategy(ELstrategy)
    graphLayoutView.ResetCamera()
    graphLayoutView.Render()

    #graphLayoutView.GetLayoutStrategy().SetRandomSeed(0)

    graphLayoutView.GetInteractor().Start()

"""
## Some useful pandas examples:
## Return number of people UID 6000 is following
len(friends[friends.ID1 == 6000 ])
## Return the users UID 6000 is following
friends[friends.ID1 == 6000 ]
"""

if __name__ == '__main__':
    main()
