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


### Check to see if table1 has a number of links to table2 equal to count
### all tables must be pandas dataframes and contain a userid column
### drops all members of table1 that do not meet the count criteria and
### returns table1
def check(table1, table2, friends, count):
    ## check middlemen
    for i in table1.userid.tolist():
        followtheleader = 0
        links = friends[friends.ID1 == i].ID2.tolist()
        links.extend(friends[friends.ID2 == i].ID1.tolist())
        for j in links:
            followtheleader = followtheleader + table2[table2.userid == j].userid.size
        if followtheleader != count:
            table1 = table1.drop(i)
    return table1

def main():
    user_file      = "./data/M2/Flitter_Names.txt"
    friend_file    = "./data/M2/Links_Table.txt"
    community_file = "./data/M2/People_Cities.txt"

    potentialgraph     = vtk.vtkMutableDirectedGraph()
    allgraph     = vtk.vtkMutableDirectedGraph()
    username  = vtk.vtkStringArray()
    username.SetName("username")
    userid    = vtk.vtkIntArray()
    userid.SetName("uid")

    community = vtk.vtkStringArray()
    community.SetName("community")

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
        size.append(friends[friends.ID2 == i].ID2.size + friends[friends.ID1 == i].ID1.size)
        username.InsertNextValue(names.username[i])
        userid.InsertNextValue(names.userid[i])
    allgraph.GetVertexData().AddArray(username)
    allgraph.GetVertexData().AddArray(userid)

    ## Put the vertex data in names for edge lookups
    names.loc[:,'vertex'] = v
    names.loc[:,'followers'] = size
    names.loc[:,'city'] = communities.City.tolist()


    ## First round of checks, do the sizes of their networks make sense?
    employees = names[(names['followers'] >= 35  ) & (names['followers'] <= 45)]
    handlers  = names[(names['followers'] >= 30  ) & (names['followers'] <= 40)]
    middlemen = names[(names['followers'] >= 4   ) & (names['followers'] <= 5 )]
    leaders   = names[(names['followers'] >= 150 )]

    vpot = []
    potusername  = vtk.vtkStringArray()
    potusername.SetName("username")
    potuserid    = vtk.vtkIntArray()
    potuserid.SetName("uid")
    classifier = vtk.vtkStringArray()
    classifier.SetName("classifier")
    handlers.loc[:,'classifier']="employee_or_handler"
    middlemen.loc[:,'classifier']="middlemen"
    leaders.loc[:,'classifier']="leaders"
    potentials = handlers.append(middlemen)
    potentials = potentials.append(leaders)
    potentials = potentials.drop(columns="vertex")
    potentials = potentials.reset_index()
    potentials = potentials.drop(columns="index")


    for i in potentials.userid.tolist():
        vpot.append(potentialgraph.AddVertex())
        potusername.InsertNextValue(potentials[potentials.userid == i].username.tolist()[0])
        potuserid.InsertNextValue(i)
        classifier.InsertNextValue(potentials[potentials.userid == i].classifier.tolist()[0])
    potentialgraph.GetVertexData().AddArray(potusername)
    potentialgraph.GetVertexData().AddArray(classifier)
    potentialgraph.GetVertexData().AddArray(userid)
    potentials['vertex'] = vpot


    #return names, friends, potentials, potentialgraph,vpot
    for i in range(0, len(potentials)):
        vertex1 = vpot[i]
        for j in friends[friends.ID1 == potentials.loc[i].userid].ID2.tolist():
            if potentials[potentials.userid == j].userid.size == 1:
                vertex2 = vpot[potentials[potentials.userid == j].vertex.tolist()[0]]
                potentialgraph.AddEdge(vertex1,vertex2)

    ## Second round of check, do they havethe appropriate links?
    #employees = check(employees, handlers, friends, 3)
    #handlers  = check(handlers, handlers, friends, 0) 

    #return friends,names

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

    ## Render Just potential employees, handlers, middlemen, and leaders
    strategy2 = vtk.vtkAttributeClustering2DLayoutStrategy()
    strategy2.SetVertexAttribute("classifier")
    strategy2.SetGraph(potentialgraph)
    graphLayoutView2 = vtk.vtkGraphLayoutView()
    graphLayoutView2.AddRepresentationFromInput(potentialgraph)
    graphLayoutView2.GetRenderWindow().SetSize(1024,1024)
    graphLayoutView2.SetLayoutStrategy(strategy2)
    graphLayoutView2.ResetCamera()
    graphLayoutView2.Render()
    graphLayoutView2.GetInteractor().Start()

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
