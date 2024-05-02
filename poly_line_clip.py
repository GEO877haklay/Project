from geospatial import *
import numpy as np

#implement the cyrus_beck line clipping algorithm

#define a dot product function
def dot(p0, p1):
    return p0[0] * p1[0] + p0[1] * p1[1]

# implement cyrus beck (NEEDS POLYGON WITH ANTICLOCKWISE ORDERED VERTICES!)
# should be working now with parallel lines of an edge of the poly that are outside
# but had to add the 0.0001 so the solution is not 100% accurate
# --> todo: implement check for left turns of polygon edges, and reordering of
# vertices if clockwise polygon inserted
def poly_line_clip(polygon, segment):
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