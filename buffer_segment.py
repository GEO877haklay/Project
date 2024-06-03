from geospatial import *
import numpy as np

def calculate_normal_vector(start, end):
    """
    Calculates the normal vector parameters (i.e. coordinates the normal
    vector's end point would have when starting from the origin) for a 
    normal vector to a segment

    :attrib start:
        the starting point of the segment as
        point object from geospatial class
    :attrib seg2:
        the end point of the segment as
        point object from geospatial class
    :returns:
        the parameter values as a tuple
    """
    dx = end.x - start.x
    dy = end.y - start.y
    length = np.sqrt(dx**2 + dy**2)
    nx = -dy / length
    ny = dx / length
    return (nx, ny)

def buffer_segment(segment, buffer_distance, extension_distance = 0):
    """
    Generates a buffer polygon around a straight segment with a flat end.
    The end can be extended using the extension_distance.

    :attrib segment:
        segment to be buffered as segment object
        from geospatial class
    :attrib buffer_distance:
        the perpendicular distance to the segment
        by which the buffer should extend (in crs units)
    :attrib extension_distance:
        the distance, by which the flat end should extend
        from the ends of the segment (in crs units)
    :returns:
        the buffer as a Polygon object from geospatial class
    """
    # Calculate normal and parallel vector
    nx, ny = calculate_normal_vector(segment.start, segment.end)
    px, py = calculate_normal_vector(Point(0,0), Point(nx,ny))

    # Calculate buffer points
    buffer_ll = (segment.start.x + nx * buffer_distance, segment.start.y + ny * buffer_distance)
    buffer_ul = (segment.end.x + nx * buffer_distance, segment.end.y + ny * buffer_distance)
    buffer_ur = (segment.end.x - nx * buffer_distance, segment.end.y - ny * buffer_distance)
    buffer_lr = (segment.start.x - nx * buffer_distance, segment.start.y - ny * buffer_distance)
    
    # Extend the rectangle
    buffer_ll = (buffer_ll[0] + px * extension_distance, buffer_ll[1] + py * extension_distance)
    buffer_ul = (buffer_ul[0] - px * extension_distance, buffer_ul[1] - py * extension_distance)
    buffer_ur = (buffer_ur[0] - px * extension_distance, buffer_ur[1] - py * extension_distance)
    buffer_lr = (buffer_lr[0] + px * extension_distance, buffer_lr[1] + py * extension_distance)
    
    # Define clockwise ordered coordinates
    buffer_polygon = Polygon(data = [buffer_ll,buffer_lr,buffer_ur,buffer_ul, buffer_ll], xcol = 0, ycol = 1)
    
    return buffer_polygon