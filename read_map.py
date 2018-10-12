#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 23:03:55 2017

@author: Jammyjamjamman
"""

import struct
import numpy as np


## Constants ##
header_fmt1 = "iiiiii128s128s256s"
header1_len = 664

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
                "cameraHeight",
                "startLocations",
                "heightMap",
                "surfaceMap",
                "resourceMap")
## Constants ##


def read_map(map_file):
    """
    Read a .bgm/ .mgm map into a dictionary.
    
    Args:
        map_file (file object): A file object pointing to a .bgm/.mgm file.
        
    Returns:
        Dict: A dictionary containing all the map data.
        
    TODO:
        Add map version 1 support.
    """
    
    # Get the map version.
    map_bytes = map_file.read()
    map_version = struct.unpack('i', map_bytes[:4])
    mg_map = {}
    # Stores the start position of currently unread bytes.
    start_byte = 0
    if map_version[0] == 1:
        raise TypeError("Map version 1 not supported!")
    
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
        
        # Map data.
        # Get player positions, *2 for x, y positions, *4 for 32bit int type.
        player_bytes = map_bytes[start_byte:start_byte + mg_map["maxFactions"]*2*4]
        pos_array = np.frombuffer(player_bytes, dtype='int32')
        player_posns = []
        for i in range(mg_map["maxFactions"]):
            player_posns.append([int(pos_array[i*2]), int(pos_array[i*2+1])])
        start_byte += mg_map["maxFactions"]*2*4
        
        map_size = mg_map["width"]*mg_map["height"]
        
        # Get heightmap, map_size*4 number of bytes 
        # because values are 32bit floats.
        height_bytes = map_bytes[start_byte:start_byte+map_size*4]
        height_map = [float(i) for i in np.frombuffer(height_bytes, dtype="float32")]
        start_byte += map_size*4
        
        # Get surface map, map_size number of bytes
        # because values are 8bit integers.
        surface_bytes = map_bytes[start_byte:start_byte+map_size]
        surface_map = [int(i) for i in np.frombuffer(surface_bytes, dtype="int8")]
        start_byte += map_size
        
        # Get resource map, map_size number of bytes
        # because values are 8bit integers.
        resource_bytes = map_bytes[start_byte:start_byte+map_size]
        resource_map = [int(i) for i in np.frombuffer(resource_bytes, dtype="int8")]
        start_byte += map_size
        
        # Store map data.
        for i, map_data in enumerate((player_posns, height_map, surface_map, resource_map)):
            mg_map[header2_keys[i+len(map_header)]] = map_data
    
    else:
        raise TypeError("map version " + map_version[0] + " not supported or understood.")
    
    return mg_map


if __name__ == '__main__':
    # Load "mymap.mgm".
    with open('mymap.mgm', 'rb') as mg_map_file:
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
