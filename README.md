# mgm2json

### Reading all the maps in a directory.

The script `read_map.py`, can be used to batch convert Glest binary maps (`.bgm`) or Megaglest binary maps (`.mgm`), to Godostra maps.

```bash
python3 mgm2json.py dir_to_mgm_maps dir_to_gs_maps
```

### Reading maps in python.

Maps can be read into a python dictionary, with the following code:

```py
from read_map import read_map

with open("mymap.mgm") as mg_map_file:
    my_map = read_map(mg_map_file)
```

the string `"mymap.mgm"`, should be replaced with the path to the map you want to load. To save a map as a `.json` file:

```py
from read_map import mgm2json

mgm2json("mymap.mgm")
```

This will save `mymap.mgm` as the json file `mymap.json`.


TODO:
* Add an installer script, so that it can be installed to python as a library.
* Add tests (maybe ;-) ).
