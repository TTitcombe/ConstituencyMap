# ConstituencyMap
This project contains code to generate maps of the United Kingdom divided by constituency lines. One can supply constituency-level data, 
such as number of voters, to see the constituency break down of the data.

Formally known as choropleth maps, the plots are generated using geopandas and matplotlib.

This repo also implements hex maps, in which each constituency is represented by an equally sized hexagon.

## How to use
Clone the repo and run `python -m examples.hexmap` in the root directory to see an example hexmap, using 
data taken from the Revoke Article 50 petition.
This example file will show you how to use the **HexMap** class the create a choropleth map of the United Kingdom.


*"Real" maps coming soon*

The plots use the generalised parliamentary boundaries as of December 2015 by default (error downloading more recent data - update on the way). To use different geographic divisions,
download the [*shapefile*](https://www.gislounge.com/what-is-a-shapefile/) you want and replace the dataset loaded in the example.

You can download official UK boundaries [here](https://geoportal.statistics.gov.uk/search?q=Parliamentary%20Generalized%20Clipped%20Boundaries).

_Note: Make sure you copy_ **all** _of the files, not just the shp file._

### What are constituencies?
The United Kingdom of Great Britain and Northern Ireland operates elections under a first-past-the-post (fptp) system.
The nation is split into hundreds of **constituencies** of roughly the same number of citizens. 

In General Elections, the politician with the most votes in each constituency is elected as that constituency's representative to the House of Commons,
as one of 650 Members of Parliament (MP).
