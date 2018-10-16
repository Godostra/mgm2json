# mgm2json

The script `read_map.py`, can be used to read Glest binary maps (`.bgm`) or Megaglest binary maps (`.mgm`), as a python dictionary.
Here is an example of reading a map:

```py
from read_map import read_map

with open('mymap.mgm', 'rb') as mg_map_file:
    my_mgmap = read_map(mg_map_file)
```

the string `"mymap.mgm"`, should be replaced with the path to the map you want to load. When the map is loaded as a python dictionary, the dictionary can be easily saved as a `.json` file:

```py
import json

with open(my_mgmap["title"]+".json", 'w') as json_file:
    json_file.write(json.dumps(my_mgmap))
```


TODO:
* Add an installer script, so that it can be installed to python as a library.
* Add tests (maybe ;-) ).
