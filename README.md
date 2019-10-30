# RASP-plots
This repo has become a bunch of functions to plot weather information coming from the [RASP forecast](http://raspuri.mooo.com/RASP/index.php) for the central region of Spain in a GIS kind of way.

## Scripts
**data.py**: script to crawl and retrieve latest calculations from [Oriol's RASP forescat](http://raspuri.mooo.com/RASP/index.php)

The data structre is:
```bash
RASP/DATA/
└── w2
    ├── SC2
    │   └── %year
    │       ├── %month
    │       │   ├── %day
    │       │   │   ├── %Hour%Minute_%property.data
```
**davinci.py**: general script to run through all the dates, times and properties to be plotted.  
**plots.py**: collection of function to plot each property individually tuned.  
**colormaps.py**: definition of custom colormaps.  
**cool_plot.py**: obsolete functions to plot on top of a google maps screenshot.


## Data files
{sc}_lats.npy & {sc}_lons.npy are the real grid used in the RASP calculations used by the WRF code. {sc} stands for the possible grids used, namely sc2, sc2+1, sc4+2, sc4+3.  
lats.npy, lons.npy, hagl.npy are the grid of latitudes, longitudes and **h**eight **a**bove **s**ea **l**evel used to plot the terrain. (These files are likely to be modified in the near future)


## Terrain data
The used terrain data is extracted from the [SkyBean terrain data repository](https://vps.skybean.eu/agl/), converted into a grid of terrain height with customizable density.
In order to plot the terrain we use matplotlib's hillshade function.
Lakes and rivers have been taken from the [Ministerio de Agricultura, Alimentación y medio ambiente](https://servicio.mapama.gob.es/sia/visualizacion/descargas/mapas.jsp)

## Release notes
v0.2.0
Ditched standard plots for layered base so the web allows a GIS-like manipulation (using javascript)
v0.1.0
Added script that tracks latest run and plots only the new information
v0.0.3
The terrain files have been checked for every grid.
The web generator has been included in the code, thought it will be heavily modified or even moved to its own repo in the near future.
Performance is now ~50s to download the data and ~25min for the plots
Logging for data.py is needed
