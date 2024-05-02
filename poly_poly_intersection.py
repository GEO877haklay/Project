from geospatial import *
from poly_line_clip import *


def poly_poly_intersection(poly1, poly2):
    #check for bounding box overlap:
    if poly1.bbox.intersects(poly2.bbox) == False:
        return None
    
    #check if poly1 totally within poly2
    if poly2.containsPoint(poly1.points[0]):
        if all([poly2.containsPoint(point) for point in poly1.points]):
            return poly1
    
    #check if poly2 totally within poly1
    if poly1.containsPoint(poly2.points[0]):
        if all([poly1.containsPoint(point) for point in poly2.points]):
            return poly2

    #otherwise, start iterating over segments of poly1 to find intersection segments
    intersection_segments = []
    for i in range(len(poly1.points)-1):
        #create segments for each edge of poly 1
        seg = Segment(poly1.points[i], poly1.points[i+1])
        seg_int = poly_line_clip(poly2, seg)
        if seg_int is not None:
                intersection_segments.append(seg_int)      

    #extract vertices of intersection segments
    newpoly_vertices = []
    for edge in intersection_segments:
        newpoly_vertices.append([edge.start.x, edge.start.y])
    if len(intersection_segments) != 0:
        newpoly_vertices.append([intersection_segments[-1].end.x, intersection_segments[-1].end.y])
    
    # get all vertices of poly2 within poly1 (i.e. not on an intersection segment but
    # still part of the intersection polygon
    for i in range(len(poly2.points)-1):
         if poly1.containsPoint(poly2.points[i]):
              if [poly2.points[i].x, poly2.points[i].y] not in newpoly_vertices:
                newpoly_vertices.append([poly2.points[i].x, poly2.points[i].y])

    # append first point again to close polygon
    if len(intersection_segments) != 0:
        newpoly_vertices.append([intersection_segments[0].start.x,intersection_segments[0].start.y])
    
    #return none if intersection points is empty (bboxes overlap, but no intersections)
    if not newpoly_vertices:
        return None
    else:
        return Polygon(newpoly_vertices, xcol = 0, ycol = 1)
    

    
