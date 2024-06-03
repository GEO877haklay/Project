from geospatial import *
from poly_line_clip import *

def grid_segments(segment_list, gridbox_size):
    """
    Seperates segment data into grid-cells, using meters as
    gridbox size and squares as gridboxes.

    :attrib segment list:
        List of the segments to be separated into smaller
        "gridded" lists
    :attrib gridbox_size:
        Length and width of the square gridboxes in meters
    :returns:
        A list containing a list of segments for each gridbox
        and the clipping gridcells as a list of polygons
        (for visualization)
    """
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


    
