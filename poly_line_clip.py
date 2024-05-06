from geospatial import *
import numpy as np

def dot(p0, p1):
    """
    Dot product function for the poly_line_clip function.

    :attrib p0:
        point with xy-coordinates as list or tuple
    :attrib p1:
        point with xy-coordinates as list or tuple
    :returns:
        dot product of the two points
    """
    return p0[0] * p1[0] + p0[1] * p1[1]


def poly_line_clip(polygon, segment):
    """
    Clips a segment using a polygon overlay. Note, that since the
    algorithm is unable to deal with lines, that are parallel to edges
    of the polygon, the result is slightly inaccurate by introducing an
    artificial offset of 0.0001 crs units to one of the segment points.

    :attrib polygon:
        Polygon object with which the segment should be
        clipped, needs to be ordered anticlockwise (not checked,
        will return false result if not adhered to)
    :attrib segment:
        Segment object that is to be clipped
    :returns:
        the clipped segment as Segment object from geospatial
        class
    """
    n = len(polygon.points)
    P1_P0 = (segment.end.x + 0.0001 - segment.start.x, segment.end.y - segment.start.y)
    normal = [(polygon.points[i].y - polygon.points[(i+1) % n].y, polygon.points[(i+1) % n].x - polygon.points[i].x) for i in range(n)]
    P0_PEi = [(polygon.points[i].x - segment.start.x, polygon.points[i].y - segment.start.y) for i in range(n)]
    numerator = [dot(normal[i], P0_PEi[i]) for i in range(n)]
    denominator = [dot(normal[i], P1_P0) for i in range(n)]
    t = [numerator[i] / denominator[i] if denominator[i] != 0 else 0 for i in range(n)]
    tE = [t[i] for i in range(n) if denominator[i] > 0]
    tL = [t[i] for i in range(n) if denominator[i] < 0]
    tE.append(0)
    tL.append(1)
    temp = [np.max(tE), np.min(tL)]
    if temp[0] > temp[1]:
        return None
    newSegment = Segment(Point(segment.start.x + P1_P0[0] * temp[0], segment.start.y + P1_P0[1] * temp[0]), 
               Point(segment.start.x + P1_P0[0] * temp[1], segment.start.y + P1_P0[1] * temp[1]))
    return newSegment