### Flitter project

The most recent commit can be viewed by cloning this repository and running the
following (in my container or somewhere you have vtk, numpy, and pandas):
```
python ./flitter.py
```

#### The Scenario
We believe an employee communicated with his/her handler(s) (a contact from the
criminal network) through Flitter, however we do not know the Flitter name of 
the handler nor of the espionage organization. We believe that the associated 
network may take one of two forms of social structures:

1. The employee has about 40 Flitter contacts. Three of these contacts are his 
   handlers, people in the criminal organization assigned to obtain his 
   cooperation. Each of the handlers probably has between 30 to 40 Flitter 
   contacts and share a common middle man in the organization, who we have 
   code-named *Boris*. Boris maintains contact with the handlers, but does not 
   allow them to communicate among themselves using Flitter. Boris communicates 
   with one or two others in the organization and no one else. One of these 
   contacts is his likely boss, who we've code­named *Fearless Leader*. Fearless 
   Leader probably has a broad Flitter network (well over 100 links), including 
   international contacts.

2. The employee has about 40 Flitter contacts. Three of these contacts are his 
   handlers, people in the organization assigned to obtain his cooperation. Each 
   of the handlers likely has between 30 to 40 Flitter contacts, and each probably 
   has his or her own middle man in the organization, who we've code-named *Boris*, 
   *Morris* and *Horace*. It is probable the middle men will not allow the handlers
   to communicate among themselves using Flitter. 

   Each of the middle men probably communicate with one or two others in the 
   organization, and no one else. One of the contacts for all of the middle men 
   is the head of the organization, Fearless Leader. Fearless Leader has a 
   broad Flitter network (well over 100 links) including international contacts.

In addition to the above, the two social structures have geospatial 
implications. While a target and handler may be in a large city, a middleman
might be in nearby smaller locations. A leadership role, such as the one of 
Fearless Leader, would likely require a presence in a larger city.

#### The Data
The data for this project is included in this repository [./data](../master/data/)

The data has been modified slightly from it's original form in the following
ways:
1. All data has only one row at the top for names of column data
   * if the data had more than one extras were removed
   * if the data had 0 then column identifiers were added
2. All data now has a null user with uid = 0 added so that indexes match uid for
   convenience.
3. Data was added to `./data/M2/Flitter_Names.txt` for each city and country to
   fix some out of bounds errors (also having state actors on a social platfrom
   like flitter is probably more relevant)

#### Starting point
Visualizing all of the data was trivial but also useless.  My first results
looked like this:
![All data, no clustering][alldata]

Since this was clearly not very useful I then tried implementing some better
graphing layout strategies like clustering, specifically
`vtk.vtkAttributeClustering2DLayoutStrategy()` using the data about what city
each flitter user was in.  This worked but there was still too much data to
view usefully:
![People-cities.txt based clustering][communities]

Next I tried reducing the data set byt removing users with few links (< 10).
![Only showing users with more than 10 followers][reduced]

This approach has 3 problems:
1. Still too much data (although it reduced the number of edges from 29,000 to
   about 9,000)
2. Removes users AND links that user created, which affects other users total
   followers making the rest of the problem difficult to classify
3. This also removes middlemen since they typically have between 3 and 5
   followers.

Because of this reducing the data in this was was discarded.

#### Reducing dataset based on problem descripton
When all else fails, look at the instructions...

Assumptions based on the instructions:
1. Twitter links are very much one directional, meaning you can "follow" someone
   without them needing to "follow" you back.  For the purposes of my solution I
   am assuming a network size to be equal to the number of people you are
   following plus the number of people following you

According to the instructions, employees have about 40 contacts, and handlers
have between 30 and 40.  This makes it difficult to identify one from the other
so my first attempt lumps them together.  There are between 100 and 150
users who fit in this category depending on how large a net cast (eg. users with
between 30 and 43 contacts).

Leaders are simple, they have well over 100 contacts.  For this attempt I
assumed a leader would have a network size of over 150.

Middlemen on the otherhand only have 4 or 5 contacts, but one of those contacts
must be a leader.  There are nearly 2,000 users with a network size of 4 or 5
but only about 700 have a network with a potential leader in it.

Lets take a look at what we see now:
![Potential networks with leaders][potentials2]

This is getting better but lets look at some networks that meet the specific
scenarios above.

#### Solution
In scenario 1 we make the following assumptions:
1. Handlers have between 28 and 42 contacts in their network
2. Handlers can talk to no more than 2 other handlers (even though they are not
   allowed by their middlemen)
3. Middlemen have between 4 and 5 contacts in their network
4. Middlemen must be in contact with a potential fearless leader
5. Middlemen must be in contact with 2 or more handlers
6. Fearless leaders must have networks of over 125 contacts
7. Employees must have between 37 and 43 people in their network
8. Employees must be in contact with 3 handlers

In addition to this I have established a link between two graphs to visualize
clusters grouped by city and by criminal type (employes, handlers, leaders, or
middlemen).
![Scenario 1 network with leaders highlighted][scenario1]

This scenario was solved with [this `flitter.py`
commit.](https://raw.githubusercontent.com/mkijowski/flitter/52779b33d14c42805c6bb52899751646d5aa5214/flitter.py)

When highlighting the leaders and zooming in on the graph clustered by city we
can tell that the leaders are predominantly in larger cities.  For this scenario
I only obtained 3 potential criminal employees:

1. @corbett
2. @bailey
3. @marrevee

The next steps are to render only the networks associated with
these three emplyees, meaning I would remove all handlers that are not responsible
for them and try to identify the remaining handler's middleman Boris.

I would also eliminate any leaders that would not make up one of the two
networks, and I would probably sanity check myself that the remaining leaders were in
large cities.

Doing so produces the following:
![Solution with leaders highlighted][solution]

You can clearly see the makeup of this criminal network.  On the left you have
the potential networks that fulfill our scenarios clustered by criminal class
(employee at the bottom, which are connected to handlers, and then to middlemen, 
and finally to leaders).  On the right you have a view of all potential criminal
candidates clusterd by city.

1. My sanity check proves correct and all but one of the potential fearless 
   leaders are in large cities.
2. On the left, the only links shown are internally relevent, employees to handlers, handlers to
   middlemen, and middelmen to leaders (although leaders do have links to one
   another...)
3. On the right we have many more vertices and edges to display a proportionally
   larger potential criminal network that might show some other mischief.  This
   graph is clustered by the city each user is in

Additional work needed:
* properly color and size the final network
* as make sure all labels are a useful size
* panning function for render windows
* selecting users should possibly highlight their network (could be recursive
  all the way up to the leader)
* remove internal links from leaders



[alldata]: https://raw.githubusercontent.com/mkijowski/flitter/master/images/alldata.png
[communities]: https://raw.githubusercontent.com/mkijowski/flitter/master/images/communities.png
[reduced]:https://raw.githubusercontent.com/mkijowski/flitter/master/images/reduced-communities.png
[potentials1]: https://raw.githubusercontent.com/mkijowski/flitter/master/images/potentials1.png
[potentials2]: https://raw.githubusercontent.com/mkijowski/flitter/master/images/potentials2.png
[scenario1]: https://raw.githubusercontent.com/mkijowski/flitter/master/images/scenario1.png
[solution]: https://raw.githubusercontent.com/mkijowski/flitter/master/images/solution.png 
