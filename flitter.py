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


### Check to see if table1 has a number of links to table2 and performs 
### a comparator operation op against the provided integer count
### all tables must be pandas dataframes and contain a userid column
### drops all members of table1 that do not meet the count/op criteria and
### returns table1
def check(table1, table2, friends, count, op):
    ## check middlemen
    for i in table1.userid.tolist():
        followtheleader = 0
        links = friends[friends.ID1 == i].ID2.tolist()
        links.extend(friends[friends.ID2 == i].ID1.tolist())
        for j in links:
            followtheleader = followtheleader + table2[table2.userid == j].userid.size
        if op == "lt":
            if followtheleader >= count: table1 = table1.drop(i)
        elif op == "le":
            if followtheleader > count: table1 = table1.drop(i)
        elif op == "eq":
            if followtheleader != count: table1 = table1.drop(i)
        elif op == "ne":
            if followtheleader == count: table1 = table1.drop(i)
        if op == "gt":
            if followtheleader <= count: table1 = table1.drop(i)
        elif op == "ge":
            if followtheleader < count: table1 = table1.drop(i)
    return table1

## Builds a graph from a list of vertices (table1) and a list of edges (friends)
## also takes a specification of clustering for the name of the array we will 
## be clustering by.
def makegraph(table1, friends, clustering):
    graph = vtk.vtkMutableDirectedGraph()
    username  = vtk.vtkStringArray()
    username.SetName("username")
    userid    = vtk.vtkIntArray()
    userid.SetName("uid")
    classifier = vtk.vtkStringArray()
    classifier.SetName(clustering)
    v = []

    ## Add vertices to graph
    for i in range(0, len(table1)):
        v.append(graph.AddVertex())
        username.InsertNextValue(table1.loc[i].username)
        userid.InsertNextValue(table1.loc[i].userid)
        if clustering == "city":
            classifier.InsertNextValue(table1.loc[i].city)
        else:
            classifier.InsertNextValue(table1.loc[i].criminal)
    graph.GetVertexData().AddArray(username)
    graph.GetVertexData().AddArray(userid)
    graph.GetVertexData().AddArray(classifier)
    table1['vertex'] = v

    ## Add edges to graph, check to make sure the edge belongs in this graph
    ## (check that both vertices are in table1)
    for i in range(0, len(table1)):
        vertex1 = v[i]
        for j in friends[friends.ID1 == table1.loc[i].userid].ID2.tolist():
            if table1[table1.userid == j].userid.size == 1:
                vertex2 = v[table1[table1.userid == j].vertex.tolist()[0]]
                graph.AddEdge(vertex1,vertex2)
    return graph

## Update out list of potential suspects
def update_suspects(potentials,handlers,employees,middlemen,leaders):
    employees.loc[:,'criminal']="employee"
    handlers.loc[:,'criminal']="handler"
    middlemen.loc[:,'criminal']="middlemen"
    leaders.loc[:,'criminal']="leader"
    potentials = handlers.append(middlemen)
    potentials = potentials.append(leaders)
    potentials = potentials.append(employees)
    potentials = potentials.reset_index()
    potentials = potentials.drop(columns="index")
    return potentials

def main():
    user_file      = "./data/M2/Flitter_Names.txt"
    friend_file    = "./data/M2/Links_Table.txt"
    community_file = "./data/M2/People_Cities.txt"

    ## Read user_file and friend_file with numpy
    names       = pd.read_csv( user_file, delimiter = '\t')
    friends     = pd.read_csv( friend_file, delimiter = '\t')
    communities = pd.read_csv( community_file, delimiter = '\t')

    ## Add the size of each users network to the pandas dataframe
    ## and the city of each user to the pandas dataframe
    size = []
    for i in range(0, len(names)):
        size.append(friends[friends.ID2 == i].ID2.size + friends[friends.ID1 == i].ID1.size)
    names.loc[:,'followers'] = size
    names.loc[:,'city'] = communities.City.tolist()

    #allgraph     = vtk.vtkMutableDirectedGraph()
    #allgraph = makegraph(names,friends,"city")

    ## First round of checks, do the sizes of their networks make sense?
    employees = names[(names['followers'] >= 37  ) & (names['followers'] <= 43)]
    handlers  = names[(names['followers'] >= 28  ) & (names['followers'] <= 42)]
    middlemen = names[(names['followers'] >= 4   ) & (names['followers'] <= 5 )]
    leaders   = names[(names['followers'] >= 125 )]

    #return names,friends,employees,handlers,middlemen,leaders

    middlemen = check(middlemen,leaders,friends,1,"ge")

    potentials = leaders
    potentials = update_suspects(potentials,handlers,employees,middlemen,leaders)

    allgraph = vtk.vtkMutableDirectedGraph()
    allgraph = makegraph(potentials,friends,"city")

    ## Second round of check, do they havethe appropriate links?
    handlers  = check(handlers, handlers, friends, 2, "le")
    employees = check(employees, handlers, friends, 3,"eq")
    middlemen = check(middlemen,handlers,friends,2,"ge")
    
    potentials     = update_suspects(potentials,handlers,employees,middlemen,leaders)
    potentialgraph = vtk.vtkMutableDirectedGraph()
    potentialgraph = makegraph(potentials,friends,"criminal")

    #return friends,names,potentials,employees,handlers,middlemen,leaders

    ### VTK pipeline stuff
    strategy = vtk.vtkAttributeClustering2DLayoutStrategy()
    strategy.SetVertexAttribute("city")
    strategy.SetGraph(allgraph)
    graphLayoutView = vtk.vtkGraphLayoutView()
    graphLayoutView.AddRepresentationFromInput(allgraph)
    graphLayoutView.GetRenderWindow().SetSize(1024,1024)
    graphLayoutView.SetLayoutStrategy(strategy)
    graphLayoutView.SetVertexLabelArrayName("city")
    graphLayoutView.SetVertexLabelVisibility(1)
    graphLayoutView.ResetCamera()


    ## Render Just potential employees, handlers, middlemen, and leaders
    strategy2 = vtk.vtkAttributeClustering2DLayoutStrategy()
    strategy2.SetVertexAttribute("criminal")
    strategy2.SetGraph(potentialgraph)
    graphLayoutView2 = vtk.vtkGraphLayoutView()
    graphLayoutView2.AddRepresentationFromInput(potentialgraph)
    graphLayoutView2.GetRenderWindow().SetSize(1024,1024)
    graphLayoutView2.SetLayoutStrategy(strategy2)
    graphLayoutView2.SetVertexLabelArrayName("username")
    graphLayoutView2.SetVertexLabelVisibility(1)
    graphLayoutView2.ResetCamera()

    ### implementing kayleigh's fancy linking code
    annotationlink = vtk.vtkAnnotationLink()
    graphLayoutView.GetRepresentation(0).SetAnnotationLink(annotationlink)
    graphLayoutView2.GetRepresentation(0).SetAnnotationLink(annotationlink)

    updater = vtk.vtkViewUpdater()
    updater.AddAnnotationLink(annotationlink)
    updater.AddView(graphLayoutView)
    updater.AddView(graphLayoutView2)

    graphLayoutView.Render()
    graphLayoutView.GetInteractor().Start()
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

