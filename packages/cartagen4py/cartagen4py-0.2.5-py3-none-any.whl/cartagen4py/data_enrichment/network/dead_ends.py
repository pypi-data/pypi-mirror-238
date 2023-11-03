import shapely
import geopandas as gpd
from cartagen4py.utils.partitioning import *
from cartagen4py.utils.network import *

def detect_dead_ends(roads):
    """
    This function detects dead ends inside a road network and returns their geometries.
    """

    crs = roads.crs

    network = []
    for road in roads.geometry:
        network.append(road)

    faces = calculate_network_faces(network)

    # Create a storage for the dead ends road index
    deadends = []
    # Storage for future enclosed faces
    enclosed = []

    # Create a tree for the network roads and for the network faces
    netree = shapely.STRtree(network)
    facetree = shapely.STRtree(faces)
    
    index = 0
    # Loop through network faces
    for face in faces:
        intersecting = []
        # Retrieve really intersecting roads
        for i in netree.query(face):
            if shapely.intersects(face, network[i]):
                # Append those index to the dead ends
                intersecting.append(i)

        # Creating a group for the dead ends
        group = []
        
        # Check if the face is totally enclosed by an other
        if is_inside(face, faces, facetree):
            # If so, append the face to the enclosed ones
            enclosed.append(face)

            




        if add:
            deadends.append({
                "did": index,
                "geometry": face
            })
        index += 1

    if len(deadends) > 0:
        return gpd.GeoDataFrame(deadends, crs=crs)
    else:
        return None

def find_holes(index, faces, tree):
    """
    Returns a list of faces indexes if those faces are completely contained inside the given face index.
    Returns an empty list if none are found.
    """
    intfaces = tree.query(face)

    for pid in tree.query(faces[index]):
        # Make sure the index is not the considered face
        if pid != index:
            # Query that face to see if the considered face is the only one intersecting
            count = 0
            for pid1 in tree.query(pid):
                if shapely.intersects(faces[pid], faces[pid1]):
                    pass


def is_inside(face, polygons, tree):
    """
    Returns true if the given face is completely inside one and only one of the other polygons.
    """
    count = 0
    for pid in tree.query(face):
        if polygons[pid] != face:
            count += 1
    
    if count == 1:
        return True
    else:
        return False