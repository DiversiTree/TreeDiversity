<img src="https://github.com/nofurtherinformation/TreeDiversity/blob/main/images/visual_abstract.jpg?raw=true" alt="Diversitree visual abstract" width="100%" />

# Diversi*Tree* Notebooks
### About
These Python notebooks are intended to help urban foresters, planners, greeners, and ecologists in quantifying tree ecosystem diversity in cities. Our recent study (citation) explored street tree diversity contrasted between the city center and outer areas, and we made these notebooks to compute tree diversity in these areas across two major dimensions:

1. **Diversity Indices:** Using two entropy indices, the Shannon Index and Simpson Index, we can measure how evenly diversity exists in your tree inventory.

2. **10/20/30 rule:** Urban foresters have long used the 10/20/30 benchmark to measure diversity. The rule suggests no more than 10% of an urban tree ecosystem should be made up of the same species, 20% of the same genus, and 30% of the same family.

These notebooks calculate these measures based on boths tree stem count (the raw number of trees) and the basal area of the tree, estimated from the diameter at breast height value. 

### How To Use These Notebooks
The two notebooks in this repository conduct a simple sensitivity analysis to check if the number of trees is sufficient to calculate these diversity indices, and then calculates the city center and outer area results. Simple plots along the way will be provided! 

To get started, gather the data as described below and open the first notebook. You'll need to add the file path to your data and input the column names needed in the notebook, and the rest of the notebook will run as you progress through the cells. 

### What You'll Need
Here's the data you'll need to use these notebooks:
1. **City Center geography:** To specify which trees are in the city center, you'll need a geospatial data file (geopackage, geojson, shapefile) with just the geometry of your city center. If multiple districts or geometries make up your city center area, we recommend dissolving these into a single feature.

2. **Tree data:** You'll need tree inventory data with the following data attached:
    * Geographic location
    * Diameter at breast height (DBH)
    * Scientific or species name
    * Genus name
    * Family name (Some ways to add this data to your tree inventory include [Open Tree of Life](https://opentreeoflife.github.io/) or [Encyclopedia of Life](https://eol.org/))

3. **Jupyter Notebook:** You'll need a Python 3 equipped [Jupyter Notebook](https://jupyter.org/install) to run these analyses! The dependency packages needed are listed in `requirements.txt` and listed below:
* pandas
* geopandas
* matplotlib
* descartes
* tqdm
* numpy

### Sample Data

Cleaned sample data for Paris, France is provided in this repository. 

### Publication

Galle, N., Halpern, D., Nitoslawski, S., Duarte, F., Ratti, C., & Pilla, F. (2021). [Mapping the diversity of street tree inventories across eight cities internationally using open data](https://senseable.mit.edu/papers/pdf/20210325_Galle-etal_MappingDiversity_UFUG.pdf). Urban Forestry and Urban Greening.

### Website

Want to learn more? Check out [DiversiTree's Website!](https://diversitree.netlify.app/)

_DiversiTree is a project of:_

<a href="https://www.ucd.ie/"><img src="https://raw.githubusercontent.com/nofurtherinformation/TreeDiversity/main/images/ucd.png" width="42px" height="60px" alt="University College Dublin Logo" /></a>&emsp;&emsp;&emsp;&emsp;<a href="http://senseable.mit.edu/"><img src="https://raw.githubusercontent.com/nofurtherinformation/TreeDiversity/main/images/mit_scl_logo_black.svg" alt="Senseable City Lab Logo" width="355px" height="60px"/></a>

___

<a href="https://connectingnature.eu/"><img src="https://github.com/nofurtherinformation/TreeDiversity/blob/main/images/connectingnature.png?raw=true" width="80px" height="80px" alt="Connecting Nature Logo" /></a>

This research received partial funding from the Connecting Nature project (Grant Agreement No. 730222) under the European Community’s Framework Program Horizon 2020.
