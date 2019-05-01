### Flitter project

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






[solutions]: https://www.cs.umd.edu/hcil/varepository/VAST%20Challenge%202009/challenges/MC2%20-%20Social%20Network%20and%20Geospatial/
[alldata]: https://raw.githubusercontent.com/mkijowski/flitter/master/images/alldata.png
[communities]: https://raw.githubusercontent.com/mkijowski/flitter/master/images/communities.png
[reduced]:https://raw.githubusercontent.com/mkijowski/flitter/master/images/reduced-communities.png
