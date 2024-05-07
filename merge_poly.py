from geospatial import *
import numpy as np
import matplotlib.pyplot as plt




#Ignore this file, it is just for testing purposes



def merge_poly(poly1,poly2):
    """
    Merges two polygons into one Polygon object. The polygons are assumed to overlap.
    The overlapped area will therefore only be counted once in the result.
    So the function should take all the points in the polygons and create the convex hull of the points.
    The convex hull is then the merged polygon. 
    The points will need to be ordered in a clockwise manner and unnecessary points should be removed.

    :attrib poly1:
        the first polygon as Polygon object from geospatial class
    :attrib poly2:
        the second polygon as Polygon object from geospatial class
    :returns:
        the merged polygon as Polygon object from geospatial class  
    
    """

    # Get the points from the polygons
    points1 = poly1.get_points()
    points2 = poly2.get_points()
    
    # Combine the points
    points = points1 + points2

    # Create the convex hull
    merged_polygon = Polygon(data = points, xcol = 0, ycol = 1)

    return merged_polygon
    

# Run the function with two simple polygons
poly1 = Polygon(data = [[0,0],[0,1],[1,1],[1,0]], xcol = 0, ycol = 1)
poly2 = Polygon(data = [[0.5,0.5],[0.5,1.5],[1.5,1.5],[1.5,0.5]], xcol = 0, ycol = 1)

test = poly1.merge_poly(poly2)
print(test.get_points())
