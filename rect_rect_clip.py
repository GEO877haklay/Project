from geospatial import *
import numpy as np


def segment_intersection(seg1, seg2):
    """
    Determines, if two segments intersect, and if so , returns the intersection Point.

    :attrib seg1:
        segment object from geospatial class
    :attrib seg2:
        segment object from geospatial class
    :returns:
        the intersection as point object from geospatial class
        or None, if no intersection exists
    """
    #test for bbox overlap
    if not Bbox(seg1).intersects(Bbox(seg2)):
        return None
    
    denominator = (((seg2.end.y - seg2.start.y) * (seg1.end.x - seg1.start.x)) - 
                   ((seg2.end.x - seg2.start.x) * (seg1.end.y - seg1.start.y)))
    
    # Check if lines are parallel
    if denominator == 0:
        return None
    
    ua = (((seg2.end.x - seg2.start.x) * (seg1.start.y - seg2.start.y)) -
          ((seg2.end.y - seg2.start.y) * (seg1.start.x - seg2.start.x))) / denominator
    ub = (((seg1.end.x - seg1.start.x) * (seg1.start.y - seg2.start.y)) -
          ((seg1.end.y - seg1.start.y) * (seg1.start.x - seg2.start.x))) / denominator
    

    # Check for intersection
    if ((ua < 0) or (ua > 1) or (ub < 0) or (ub > 1)):
        return None
    
    # Calculate x and y coordinates of intersection
    x = seg1.start.x + ua * (seg1.end.x - seg1.start.x)
    y = seg1.start.y + ua * (seg1.end.y - seg1.start.y)

    return Point(x,y)

def rect_rect_intersection(poly1, poly2):
    """
    Returns all intersection points of two rectangular Polygons.

    :attrib poly1:
        rectangular Polygon object from geospatial class
    :attrib seg2:
        rectangular Polygon object from geospatial class
    :returns:
        list of intersection Points, or empty list if
        there are no intersection points
    """
    #check for bbox overlap
    if not poly1.bbox.intersects(poly2.bbox):
        return []

    intersectionPoints = []

    # loop over all edges of each polygon
    for i in range(4):
        seg_poly1 = Segment(poly1[i],poly1[i+1])
        for j in range(4):
            seg_poly2 = Segment(poly2[j],poly2[j+1])
            intersection_point = segment_intersection(seg_poly1,seg_poly2)
            if intersection_point is not None:
                intersectionPoints.append(intersection_point)
    
    return intersectionPoints

def rect_rect_clip(poly1, poly2):
    """
    Clips two rectangular Polygons and returns the clipped area as Polygon

    :attrib poly1:
        rectangular Polygon object from geospatial class
    :attrib seg2:
        rectangular Polygon object from geospatial class
    :returns:
        clipped area shared between the two input Polygons
        as a Polygon object from geospatial class
    """
    #check for bbox overlap
    if not poly1.bbox.intersects(poly2.bbox):
        return None

    all_points = []
    #loop over each vertice of each polygon
    for i in range(4):
        vertice = poly1[i]
        if poly2.containsPoint(vertice):
            all_points.append(vertice)
    
    for i in range(4):
        vertice = poly2[i]
        if poly1.containsPoint(vertice):
            all_points.append(vertice)
    
    # add intersection points to list
    all_points = all_points + rect_rect_intersection(poly1, poly2)

    # calculate center of points
    cx = all_points[0].x
    cy = all_points[0].y
    for i in range(1,len(all_points)):
        cx = cx + ((all_points[i].x - cx) / (i+1))
        cy = cy + ((all_points[i].y - cy) / (i+1))
    
    # calculate angle of all points from center of points
    points_with_angles = []
    for point in all_points:
        points_with_angles.append([[point.x,point.y], np.arctan2(cy - point.y, cx - point.x)])
    
    # sort points clockwise through angle value
    points_with_angles = sorted(points_with_angles, key = lambda x: x[1])

    sorted_points = [points_with_angles[i][0] for i in range(len(points_with_angles))]
    sorted_points.append(sorted_points[0])

    return Polygon(sorted_points, xcol = 0, ycol = 1)



