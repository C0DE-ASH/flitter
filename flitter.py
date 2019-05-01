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
    allgraph     = vtk.vtkMutableDirectedGraph()
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
    size = []

    """
    ## Housecleaning
    uninteresting = friends.ID2.groupby(friends.ID2.tolist()).size()[friends.ID2.groupby(friends.ID2.tolist()).size() < 10].keys()
    for i in range(0, len(uninteresting)):
        friends = friends.drop(friends[friends.ID1 == uninteresting[i]].index.tolist())
        friends = friends.drop(friends[friends.ID2 == uninteresting[i]].index.tolist())
        names = names.drop(names[names.userid == uninteresting[i]].index.tolist())
        communities = communities.drop(communities[communities.ID == uninteresting[i]].index.tolist())

    names = names.reset_index()
    friends = friends.reset_index()
    communities = communities.reset_index()
    """

    ## Create vertex from Flitter_names
    for i in range(0, len(names)):
        v.append(allgraph.AddVertex())
        size.append(friends[friends.ID2 == i].ID2.size)
        username.InsertNextValue(names.username[i])
        userid.InsertNextValue(names.userid[i])
    allgraph.GetVertexData().AddArray(username)
    allgraph.GetVertexData().AddArray(userid)

    ## Put the vertex data in names for edge lookups
    names['vertex'] = v
    names['followers'] = size
    names['city'] = communities.City.tolist()

    employees = names[(names['followers'] >= 35 ) & (names['followers'] <= 45)]
    handlers = names[(names['followers'] => 30 ) &( names['followers'] <= 40)]
    middlemen = names[(names['followers'] >= 4 ) & (names['followers'] <= 5)]
    leaders = names[(names['followers'] >= 150 )]

    return friends,names

    ## Add Edges
    for i in range(0, len(friends)):
        allgraph.AddEdge(v[friends.ID1[i]],v[friends.ID2[i]])
        #vertex1 = v[names[names.userid == friends.ID1[i]].vertex.tolist()[0]]
        #vertex2 = v[names[names.userid == friends.ID2[i]].vertex.tolist()[0]]
        #allgraph.AddEdge(vertex1,vertex2)

    for i in range(0,len(communities)):
        community.InsertNextValue(communities.City[i])
    allgraph.GetVertexData().AddArray(community)


    ### VTK pipeline stuff

    ## Render All users
    strategy = vtk.vtkAttributeClustering2DLayoutStrategy()
    strategy.SetVertexAttribute("community")
    strategy.SetGraph(allgraph)
    graphLayoutView = vtk.vtkGraphLayoutView()
    graphLayoutView.AddRepresentationFromInput(allgraph)
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

get number of followers:
friends.ID2.groupby(friends.ID2.tolist()).size()
df = pd.DataFrame(friends.ID2.groupby(friends.ID2.tolist()).size())


friends.ID2.groupby(friends.ID2.tolist()).size()[friends.ID2.groupby(friends.ID2.tolist()).size() < 10].keys()

"""

if __name__ == '__main__':
    main()
