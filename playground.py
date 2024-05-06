#%% imports
from geospatial import *
from poly_line_clip import *
from poly_poly_intersection import *
import matplotlib.pyplot as plt
import numpy as np



#%% create segments
seg_data = [(3,3,6,6),
            (3,6,6,3), 
            (3,1,7,7),
            (3,3,6,3), 
            (3,1,7,1),
            (3,3,6,6),
            (5,5,8,8),
            (1,10,10,10),
            (5,10,11,10),
            (4,4,10,10),
            (9,9,11,11),
            (4,4,4,8),
            (4,3,4,1)
            ]

segments = []
for a in range(0, len(seg_data)):
    seg = Segment(Point(seg_data[a][0],seg_data[a][1]),Point(seg_data[a][2],seg_data[a][3]))
    segments.append(seg)


#%% plot segements

for seg in segments:
    x = [seg.start.x, seg.end.x]
    y = [seg.start.y, seg.end.y]
    plt.plot(x,y)
plt.show()
# %% create polygon

poly_data = [(4,3),
             (6,3),
             (7,5),
             (5,7),
             (3,5),
             (4,3)]


polygon = Polygon(poly_data, xcol = 0, ycol = 1)

xs = [i.x for i in polygon]
ys = [i.y for i in polygon]

#%% plot lines & polygon
for seg in segments:
    x = [seg.start.x, seg.end.x]
    y = [seg.start.y, seg.end.y]
    plt.plot(x,y)

plt.plot(xs, ys, linestyle = 'dashed')
plt.show()


# %%
clipped_segments = []
for seg in segments:
    clipped_segments.append(poly_line_clip(poly1, seg))

for seg in clipped_segments:
    if seg is not None:
        x = [seg.start.x, seg.end.x]
        y = [seg.start.y, seg.end.y]
        plt.plot(x,y)

plt.plot(xs, ys, linestyle = 'dashed')
plt.show()

# %% test poly_poly_intersection
poly1_data = [(4,3),
              (6,3),
              (7,5),
              (5,7),
              (3,5),
              (4,3)]

poly2_data = [(5,3),
              (7,3),
              (8,5),
              (6,7),
              (4,5),
              (5,3)]

poly1 = Polygon(poly1_data, xcol = 0, ycol = 1)
poly2 = Polygon(poly2_data, xcol = 0, ycol = 1)

poly3 = poly_poly_intersection(poly1, poly2)
# %% plot poly_poly_intersection result

xs1 = [i.x for i in poly1]
ys1 = [i.y for i in poly1]

xs2 = [i.x for i in poly2]
ys2 = [i.y for i in poly2]

xs3 = [i.x for i in poly3]
ys3 = [i.y for i in poly3]

plt.plot(xs1, ys1, linestyle='dashed')
plt.plot(xs2, ys2, linestyle='dashed')
plt.plot(xs3, ys3, linestyle='dashed')
plt.show()

# %%
intersection_segments = []
for i in range(len(poly1.points)-1):
    #create segments for each edge of poly 1
    seg = Segment(poly1.points[i], poly1.points[i+1])
    seg_int = poly_line_clip(poly2, seg)
    if seg_int is not None:
            intersection_segments.append(seg_int)      

newpoly_vertices = []
for edge in intersection_segments:
    newpoly_vertices.append([edge.start.x, edge.start.y])
newpoly_vertices.append([intersection_segments[-1].end.x, intersection_segments[-1].end.y])

for i in range(len(poly2.points)-1):
        if poly1.containsPoint(poly2.points[i]):
            newpoly_vertices.append([poly2.points[i].x, poly2.points[i].y])

# %%
intersection_segments = []

for i in range(len(poly1.points)-1):
     segment = Segment(Point(poly1.points[i].x+0.1, poly1.points[i].y+0.1),
                       Point(poly1.points[i+1].x+0.1, poly1.points[i+1].y+0.1))
     int_seg = poly_line_clip(poly2, segment)
     if int_seg is not None:
          intersection_segments.append(int_seg)

for seg in intersection_segments:
    x = [seg.start.x, seg.end.x]
    y = [seg.start.y, seg.end.y]
    plt.plot(x,y)
plt.plot(xs2, ys2, linestyle='dashed')
plt.show()


# %%
intersection_segments = []
for i in range(len(poly1.points)-1):
    #create segments for each edge of poly 1
    seg = Segment(poly1.points[i], poly1.points[i+1])
    seg_int = poly_line_clip(poly2, seg)
    if seg_int is not None:
            intersection_segments.append(seg_int)

newpoly_vertices = []
for edge in intersection_segments:
    newpoly_vertices.append([edge.start.x, edge.start.y])
newpoly_vertices.append([intersection_segments[-1].end.x, intersection_segments[-1].end.y])


for i in range(len(poly2.points)-1):
        if poly1.containsPoint(poly2.points[i]):
            if [poly2.points[i].x, poly2.points[i].y] not in newpoly_vertices:
                newpoly_vertices.append([poly2.points[i].x, poly2.points[i].y])

newpoly_vertices.append([intersection_segments[0].start.x,intersection_segments[0].start.y])  
# %% another poly poly test
sample1 = [[0,10], [5,0], [10,10], [15,0], [20,10], [25, 0],
             [30, 20], [35, 15], [45, 0], [50, 50], [45, 40], 
             [40, 50], [30, 45], [25, 40], [20, 30], [15, 50],
             [10,35], [5, 50],[5,50], [0, 10]]

poly4 = Polygon(sample1, xcol=0, ycol=1)

poly5 = poly_poly_intersection(poly4, poly1)

xs4 = [i.x for i in poly4]
ys4 = [i.y for i in poly4]

xs5 = [i.x for i in poly5]
ys5 = [i.y for i in poly5]

plt.plot(xs1, ys1, linestyle='dashed')
plt.plot(xs4, ys4, linestyle='dashed')
plt.plot(xs5, ys5, linestyle='dashed')
plt.show()
# %%
