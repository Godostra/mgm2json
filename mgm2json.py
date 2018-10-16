#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 23:03:55 2017

@author: Jammyjamjamman
@adapted for Godostra: alketii
"""

import struct,sys,json,os
import numpy as np
from PIL import Image

TILE_SIZE = 16

img_1 = Image.open('tiles/1.png', 'r')
img_2 = Image.open('tiles/2.png', 'r')
img_3 = Image.open('tiles/3.png', 'r')

files = [f for f in os.listdir(sys.argv[1]) if os.path.isfile(os.path.join(sys.argv[1], f))]

total_files = len(files)

## Constants ##
header_fmt2 = "iiiiii128s128s128siii116s"
header2_len = 536
header2_keys = ("version",
                "maxFactions",
                "width",
                "height",
                "heightFactor",
                "waterLevel",
                "title",
                "author",
                "description",
                "magic",
                "cliffLevel",
                "cameraHeight")

map_dat_keys = ("startLocations",
                "heightMap",
                "surfaceMap",
                "resourceMap")

header_fmt1 = "iiiiii128s128s256s"
header1_len = 536
header1_keys = header2_keys[:9]
## Constants ##


def read_map(map_file):
    """
    Read a .bgm/ .mgm map into a dictionary.

    Args:
        map_file (file object): A file object pointing to a .bgm/.mgm file.

    Returns:
        Dict: A dictionary containing all the map data.

    TODO:
        Clean up script.
    """

    # Get the map version.
    map_bytes = map_file.read()
    map_version = struct.unpack('i', map_bytes[:4])
    mg_map = {}
    # Stores the start position of currently unread bytes.
    start_byte = 0
    if map_version[0] == 1:
        # Get header data.
        header_bytes = map_bytes[start_byte:start_byte+header1_len]
        map_header = list(struct.unpack(header_fmt1, header_bytes))
        # Remove blank data at the end.
        #del map_header[-1]
        # Store map header data.
        for i in range(len(map_header)):
            mg_map[header1_keys[i]] = map_header[i]
        # Convert text bytes to text.
        mg_map["title"] = mg_map["title"].decode('utf8').strip('\x00')
        mg_map["author"] = mg_map["author"].decode('utf8').strip('\x00')
        mg_map["description"] = mg_map["description"].decode('utf8').strip('\x00')
        start_byte += header1_len

    elif map_version[0] == 2:
        # Get header data.
        header_bytes = map_bytes[start_byte:start_byte+header2_len]
        map_header = list(struct.unpack(header_fmt2, header_bytes))
        # Remove blank data at the end.
        del map_header[-1]
        # Store map header data.
        for i in range(len(map_header)):
            mg_map[header2_keys[i]] = map_header[i]
        # Convert text bytes to text.
        mg_map["title"] = mg_map["title"].decode('utf8').strip('\x00')
        mg_map["author"] = mg_map["author"].decode('utf8').strip('\x00')
        mg_map["description"] = mg_map["description"].decode('utf8').strip('\x00')
        start_byte += header2_len

    else:
        raise TypeError("Map version " + map_version[0] + " not supported or understood.")

    # Map data.
    # Get player positions, *2 for x, y positions, *4 for 32bit int type.
    player_bytes = map_bytes[start_byte:start_byte + mg_map["maxFactions"]*2*4]
#    pos_array = np.frombuffer(player_bytes, dtype='int32')
    player_posns = []
    for i in range(mg_map["maxFactions"]):
        player_posns.append([int.from_bytes(player_bytes[i*2*4:i*2*4+4], byteorder="little"), int.from_bytes(player_bytes[i*2*4+4:i*2*4+8], byteorder="little")])
    start_byte += mg_map["maxFactions"]*2*4

    map_size = mg_map["width"]*mg_map["height"]

    # Get heightmap, map_size*4 number of bytes
    # because values are 32bit floats.
    height_bytes = map_bytes[start_byte:start_byte+map_size*4]
    height_map = [struct.unpack('f', height_bytes[i*4:i*4+4]) for i in range(map_size)]
    start_byte += map_size*4

    # Get surface map, map_size number of bytes
    # because values are 8bit integers.
    surface_bytes = map_bytes[start_byte:start_byte+map_size]
    surface_map = [int(surf_byte) for surf_byte in surface_bytes]
    start_byte += map_size

    # Get resource map, map_size number of bytes
    # because values are 8bit integers.
    resource_bytes = map_bytes[start_byte:start_byte+map_size]
    resource_map = [int(res_byte) for res_byte in resource_bytes]
    start_byte += map_size

    # Store map data.
    for key, map_dat in zip(map_dat_keys, (player_posns, height_map, surface_map, resource_map)):
        mg_map[key] = map_dat

    return mg_map


if __name__ == '__main__':
    # Load "mymap.mgm".
	file_i = 0
	for f in files:
		file_i += 1
		f_name = f.split(".")
		f_ext = f_name[1]
		f_name = f_name[0]
		out = sys.argv[2]+'/'+f_name
		os.mkdir(out)
		print("Converting:",f_name,file_i,"/",total_files)
		if f_ext in ["mgm","gbm"]:
			with open(sys.argv[1]+"/"+f, 'rb') as mg_map_file:
				jmap = read_map(mg_map_file)

				background = Image.new('RGB', (jmap['width']*TILE_SIZE, jmap['height']*TILE_SIZE), (0, 255, 0))	
				
				i = 0
				for y in range(jmap['height']):
					for x in range(jmap['width']):
						cell = jmap['surfaceMap'][i]
						if cell == 1:
							background.paste(img_1, (x*TILE_SIZE, y*TILE_SIZE), mask=img_1)
						elif cell == 2:
							background.paste(img_2, (x*TILE_SIZE, y*TILE_SIZE), mask=img_2)
						elif cell == 3:
							background.paste(img_3, (x*TILE_SIZE, y*TILE_SIZE), mask=img_3)
						
						i += 1
				
				background2 = background.rotate(180, expand=True)
				background2.save(out+'/splatmap.png')
	
	
				height = Image.open('tiles/height.png', 'r')
				background = Image.new('RGB', (jmap['width']*TILE_SIZE, jmap['height']*TILE_SIZE), (0, 0, 0))

				i = 0
				for y in range(jmap['height']):
					for x in range(jmap['width']):
						cell = int(jmap['heightMap'][i][0])
						for c in range(cell):
							background.paste(height, (x*TILE_SIZE, y*TILE_SIZE), mask=height)
						i += 1

				background2 = background.rotate(180, expand=True)
				background2.save(out+'/heightmap.png')
	
				with open(out+"/map.json", 'w') as json_file:
        				json_file.write(json.dumps(jmap))
	
			
	print("DONE!")