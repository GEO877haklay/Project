#%% imports
from geospatial import *
from poly_line_clip import *
from rect_rect_clip import *
from buffer_segment import *
import matplotlib.pyplot as plt
import numpy as np
import json



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
# %% for presentation
def load_segments_from_geojson(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    segments = []
    for feature in data['features']:
        coords = feature['geometry']['coordinates']
        if isinstance(coords[0], list):
            if isinstance(coords[0][0], list):
                for subcoords in coords:
                    for i in range(len(subcoords) - 1):
                        p1 = Point(subcoords[i][0], subcoords[i][1])
                        p2 = Point(subcoords[i + 1][0], subcoords[i + 1][1])
                        segments.append(Segment(p1, p2))
            else:
                for i in range(len(coords) - 1):
                    p1 = Point(coords[i][0], coords[i][1])
                    p2 = Point(coords[i + 1][0], coords[i + 1][1])
                    segments.append(Segment(p1, p2))
        else:
            p1 = Point(coords[0], coords[1])
            p2 = Point(coords[2], coords[3])
            segments.append(Segment(p1, p2))
    return segments

motorways_osm = load_segments_from_geojson(r'S:\course\geo877\student\haklay\data\geojson\zurich\osm'+'/motorway_zh_osm.geojson')
motorways_top = load_segments_from_geojson(r'S:\course\geo877\student\haklay\data\geojson\zurich\swisstopo'+'/motorway_zh_swisstopo.geojson')
aoi = Polygon([[2.677*1e6,1.243*1e6],[2.679*1e6,1.243*1e6],[2.679*1e6,1.245*1e6],[2.677*1e6,1.245*1e6],[2.677*1e6,1.243*1e6]], xcol=0,ycol=1)
motorways_osm_clipped = []
motorways_top_clipped = []
for motorway in motorways_osm:
    clipped_segment = poly_line_clip(aoi,motorway)
    if clipped_segment is not None:
        motorways_osm_clipped.append(clipped_segment)
for motorway in motorways_top:
    clipped_segment = poly_line_clip(aoi,motorway)
    if clipped_segment is not None:
        motorways_top_clipped.append(clipped_segment)

#%% plotting motorways
fig = plt.figure(figsize=(20,20))
for seg in motorways_osm_clipped:
    x = [seg.start.x, seg.end.x]
    y = [seg.start.y, seg.end.y]
    plt.plot(x,y, color='Green')
for seg in motorways_top_clipped:
    x = [seg.start.x, seg.end.x]
    y = [seg.start.y, seg.end.y]
    plt.plot(x,y, color='Red')
plt.show()

# %% buffered motorways
def buffer_segments(segments, buffer_distance):
    buffered_segments = []
    for seg in segments:
        buffered_seg = buffer_segment(seg, buffer_distance)
        buffered_segments.append(buffered_seg)
    return buffered_segments

motorways_osm_clipped_buffer = buffer_segments(motorways_osm_clipped,10)
motorways_top_clipped_buffer = buffer_segments(motorways_top_clipped,10)

#%% plot buffered motorways
fig = plt.figure(figsize=(20,20))
for seg in motorways_osm_clipped:
    x = [seg.start.x, seg.end.x]
    y = [seg.start.y, seg.end.y]
    plt.plot(x,y, color='Green')
for seg in motorways_top_clipped:
    x = [seg.start.x, seg.end.x]
    y = [seg.start.y, seg.end.y]
    plt.plot(x,y, color='Red')

for poly in motorways_osm_clipped_buffer:
    xs = [i.x for i in poly]
    ys = [i.y for i in poly]
    plt.plot(xs,ys, color = 'Green')

for poly in motorways_top_clipped_buffer:
    xs = [i.x for i in poly]
    ys = [i.y for i in poly]
    plt.plot(xs,ys, color = 'Red')


plt.show()

#%% Intersection Polygons
intersecting_buffers = []
for buffer_osm in motorways_osm_clipped_buffer:
    for buffer_top in motorways_top_clipped_buffer:
        intersection = rect_rect_clip(buffer_osm,buffer_top)
        if intersection is not None:
            intersecting_buffers.append(intersection)

# %% plot buffered motorways with intersecting buffers
fig = plt.figure(figsize=(20,20))


for poly in motorways_osm_clipped_buffer:
    xs = [i.x for i in poly]
    ys = [i.y for i in poly]
    plt.plot(xs,ys, color = 'Green')

for poly in motorways_top_clipped_buffer:
    xs = [i.x for i in poly]
    ys = [i.y for i in poly]
    plt.plot(xs,ys, color = 'Red')

for poly in intersecting_buffers:
    xs = [i.x for i in poly]
    ys = [i.y for i in poly]
    plt.plot(xs,ys, color = 'Purple')

plt.show()

# %% intersect overlapping buffer intersections
overlaping_buffer_intersections = []
for i in range(len(intersecting_buffers)):
    for j in range(len(intersecting_buffers)):
        if i != j:
            intersection = rect_rect_clip(intersecting_buffers[i],intersecting_buffers[j])
            if intersection is not None:
                overlaping_buffer_intersections.append(intersection)

#%% test poly contains point
poly = Polygon([[0,0],[5,5],[3,7],[-2,2],[0,0]],xcol=0,ycol=1)
point = Point(-2,2)

poly.containsPoint(point)

# %% test gridding
def grid_segments(segment_list, gridbox_size):
    #initialize new segment list and grid polygons
    gridded_segments = []
    grid_polygons = []
    #get extent of data
    for i,segment in enumerate(segment_list):
        box = Bbox(segment)
        if i == 0:
            xmin,ymin,xmax,ymax = (box.ll.x,box.ll.y,box.ur.x,box.ur.y)
        else:
            if box.ll.x < xmin:
                xmin = box.ll.x
            if box.ll.y < ymin:
                ymin = box.ll.y
            if box.ur.x > xmax:
                xmax = box.ur.x
            if box.ur.y > ymax:
                ymax = box.ur.y
    x_extent = xmax-xmin
    y_extent = ymax-ymin
    #get gridcellcount in x&y dimension and set up polygons
    x_cellcount = int((x_extent // gridbox_size) +1)
    y_cellcount = int((y_extent // gridbox_size) +1)
    for i in range(y_cellcount):
        for j in range(x_cellcount):
            poly = Polygon([[(j*gridbox_size)+xmin,(i*gridbox_size)+ymin],
                            [((j+1)*gridbox_size)+xmin,(i*gridbox_size)+ymin],
                            [((j+1)*gridbox_size)+xmin,((i+1)*gridbox_size)+ymin],
                            [(j*gridbox_size)+xmin,((i+1)*gridbox_size)+ymin],
                            [(j*gridbox_size)+xmin,(i*gridbox_size)+ymin]
                            ],xcol=0,ycol=1)
            grid_polygons.append(poly)
    #cut segments with gridcells using cyrus-beck & add one segment-list per gridcell
    for cell in grid_polygons:
        grid_segments = []
        for segment in segment_list:
            if Bbox(segment).intersects(cell.bbox):
                clipped_segment = poly_line_clip(cell,segment)
                if clipped_segment is not None:
                    grid_segments.append(clipped_segment)
        gridded_segments.append(grid_segments)
    
    return gridded_segments, grid_polygons


motorways_osm_gridded, grid_polygons = grid_segments(motorways_osm,5000)

#%% plot gridded segments
colors = ['red','green', 'blue']
for i, cell in enumerate(motorways_osm_gridded):
    xs = [j.x for j in grid_polygons[i]]
    ys = [j.y for j in grid_polygons[i]]
    plt.plot(xs,ys, color = colors[i%3])
    for seg in cell:
        x = [seg.start.x, seg.end.x]
        y = [seg.start.y, seg.end.y]
        plt.plot(x,y, color=colors[i%3])


# %%
