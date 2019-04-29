#!/usr/bin/python
"""
CEG 7560
Visual & Image Process
Assignment 3 - Flitter Data

Matthew Kijowski
matthewkijowski@gmail.com
w114mek
"""

import pandas as pd
import vtk
import numpy as np

def main():
    user_file      = "./data/M2/Flitter_Names.txt"
    friend_file    = "./data/M2/Links_Table.txt"
    community_file = "./data/M2/People_Cities.txt"

    graph     = vtk.vtkMutableDirectedGraph()
    username  = vtk.vtkStringArray()
    username.SetName("username")

    userid    = vtk.vtkIntArray()
    userid.SetName("uid")

    community = vtk.vtkStringArray()
    community.SetName("community")
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

    #return graph

    ### VTK pipeline stuff

    ## Strategy attempt 2
    strategy = vtk.vtkAttributeClustering2DLayoutStrategy()
    strategy.SetVertexAttribute("community")

    ## Strategy Attempt 1, failed due to not finding community array...
    #strategy = vtk.vtkCommunity2DLayoutStrategy()
    #strategy.SetCommunityArrayName("community")


    strategy.SetGraph(graph)
    graphLayoutView = vtk.vtkGraphLayoutView()
    graphLayoutView.AddRepresentationFromInput(graph)
    graphLayoutView.GetRenderWindow().SetSize(1024,1024)
    graphLayoutView.SetLayoutStrategy(strategy)
    graphLayoutView.ResetCamera()
    graphLayoutView.Render()
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
