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
    strategy = "Community2D"
    #ELstrategy = "Pass Through"
    #Requires vtkboost
    #strategy = "CosmicTree"

    user_file      = "./data/M2/Flitter_Names.txt"
    friend_file    = "./data/M2/Links_Table.txt"
    community_file = "./data/M2/People_Cities.txt"
    colors = vtk.vtkNamedColors()

    graph     = vtk.vtkMutableDirectedGraph()
    username  = vtk.vtkStringArray()
    userid    = vtk.vtkIntArray()
    community = vtk.vtkStringArray()
    #community.SetComponentName("community")
    community.SetName("community")
    #userid.SetComponentName("uid")
    graph.GetVertexData().SetPedigreeIds(userid)

    ## Read user_file and friend_file with numpy
    names       = pd.read_csv( user_file, delimiter = '\t')
    friends     = pd.read_csv( friend_file, delimiter = '\t')
    communities = pd.read_csv( community_file, delimiter = '\t')

    ## Array to store verticies for adding edges
    v = []

    ## Create vertex from Flitter_names
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

    for i in range(0,len(communities)):
        community.InsertNextValue(communities.City[i])
    graph.GetVertexData().AddArray(community)

    return graph

    ### VTK pipeline stuff
    graphLayoutView = vtk.vtkGraphLayoutView()
    graphLayoutView.AddRepresentationFromInput(graph)
    #graphLayoutView.SetEdgeLayoutStrategy(ELstrategy)
    #graphLayoutView.SetLayoutStrategyToCommunity2D()


    strategery = vtk.vtkCommunity2DLayoutStrategy()
    strategery.SetGraph(graph)
    strategery.SetCommunityArrayName("community")
    graphLayoutView.SetLayoutStrategy(strategery)

    graphLayoutView.GetRenderWindow().SetSize(1024,1024)
    #theme = vtk.vtkViewTheme.CreateMellowTheme()
    #graphLayoutView.ApplyViewTheme(theme)

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
