# ConstituencyMap
This project contains code to generate maps of the United Kingdom divided by constituency lines. One can supply constituency-level data, 
such as number of voters, to see the constituency break down of the data. The maps represent
constituencies as equally-sized hexagons. This can be invaluable for visualising maps in a way
not biased by landmass.

Static plots are generated using geopandas and matplotlib, and interactive maps
are generated with altair.

## Maps
The mapper classes are implemented in `map/`. Currently, only hex maps have been implemented. These maps are created using the fantastic tool by 
[ODILeeds](https://odileeds.org/projects/hexmaps/constituencies/). There is a script in `utils/hex_to_csv` 
which converts the "hexjson" files created by ODILeeds into csv files.

This repo uses data from the [Revoke Article 50 petition](https://petition.parliament.uk/petitions/241584) in the 
example files to demonstrate how to create choropleth maps.

## How to use
Run the [`examples/`][examples], either by cloning the repo or using [binder][binder]

in the root directory to see an example hexmap, using 
data taken from the Revoke Article 50 petition.
This example file will show you how to use the **HexMap** class the create a choropleth map of the United Kingdom.

### What are constituencies?
The United Kingdom of Great Britain and Northern Ireland operates elections under a first-past-the-post (fptp) system.
The nation is split into hundreds of **constituencies** of roughly the same number of citizens. 

In General Elections, the politician with the most votes in each constituency is elected as that constituency's representative to the House of Commons,
as one of 650 Members of Parliament (MP).

[examples]: examples/
[binder]: examples/