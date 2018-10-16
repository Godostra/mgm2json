#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 23:03:55 2017

@author: Jammyjamjamman
"""

import struct
import numpy as np


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
    with open('conflict.gbm', 'rb') as mg_map_file:
        my_mgmap = read_map(mg_map_file)
    
    # Uncomment this to plot the map data.

    """
    import matplotlib.pyplot as plt
    heightmap = np.reshape(my_mgmap["heightMap"],
                           (my_mgmap["height"], my_mgmap["width"]))
    plt.imshow(heightmap)
    plt.show()
    
    plt.figure(2)
    surfacemap = np.reshape(my_mgmap["surfaceMap"],
                            (my_mgmap["height"], my_mgmap["width"]))
    plt.imshow(surfacemap)
    plt.show()
    
    plt.figure(3)
    resourcemap = np.reshape(my_mgmap["resourceMap"],
                             (my_mgmap["height"], my_mgmap["width"]))
    plt.imshow(resourcemap)
    plt.show()
    """
    
    # Uncomment this to save map data as a JSON.
    """
    # Save atze's 6player map as a json file.
    import json
    with open(my_mgmap["title"]+".json", 'w') as json_file:
        json_file.write(json.dumps(my_mgmap))
    """
