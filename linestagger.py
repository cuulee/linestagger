import pandas as pd
import numpy as np
import simplejson as json
import math

# given a point1 x,y and a point2 x,y returns distance in miles
# points are given in long,lat geospatial cordinates
def distance(point1,point2):
	point1 = np.array(point1)
	point2 = np.array(point2)
	return np.linalg.norm(point1-point2)

# gets coords from a string representation of coords
def get_cords_json(coords):
	data = '{"a":%s}' % coords
	data = json.loads(data)	
	return data['a']

# gets a slope
def get_slope(pt1,pt2):
	x1,y1 = pt1
	x2,y2 = pt2

	if x1 == x2: 
		slope = 10000000.
	else:
		slope = (float(y2) - float(y1)) / (float(x2) - float(x1))

	return slope

# bullshit bearing 
def bullshit_bearing(pt1,pt2):
	return 90. - (180. / math.pi) * math.atan2(pt2[0]-pt1[0],pt2[1]-pt1[1])

# calculatating the stagger needed on each side
def perpendicular_slope(slope):
	if slope == 0:
		return 0.
	return - slope ** - 1 

# calculating the distance in feet which the stagger will be
def stagger(distancefeet):
	return (distancefeet / 5280.) / 69.2

# calculating the xy deltas for the stagger distance
# accepts coords to not recalculate shit forever
def calc_xydelta(pt1,pt2,staggerdistcoords):
	# getting slope
	slope = get_slope(pt1,pt2)

	# getting perpendicular slope
	perpslope = perpendicular_slope(slope)

	# getting the angle of the perpslope
	angleslope = math.atan(perpslope)


	# getting xdelta and y delta
	# these may later be abs()
	# thinking rule basedd quadrants fuck everything else
	xdelta,ydelta = staggerdistcoords * math.cos(angleslope),staggerdistcoords * math.sin(angleslope)

	# taking absolutes of xdelta and ydelta
	xdelta,ydelta = abs(xdelta),abs(ydelta)

	# getting bearing i know kind of redudant
	bearing = bullshit_bearing(pt1,pt2)
	if bearing < 0:
		bearing = 360 + bearing

	if bearing >= 0 and bearing <= 90:
		# im calling this quad 1 im not sure if it is
		xmult = 1.
		ymult = -1.
	elif bearing > 90 and bearing <= 180:
		# quad 2
		xmult = 1.
		ymult = 1.
	elif bearing > 180 and bearing <= 270:
		# quard 3
		xmult = -1.
		ymult = 1.
	elif bearing > 270 and bearing <= 360:
		# quard 3
		xmult = -1.
		ymult = -1.

	# therefore  
	# points in relation to lien progression
	rightsidept1,rightsidept2 = [pt1[0] + xdelta * xmult,pt1[1] + ydelta * ymult],[pt2[0] + xdelta * xmult,pt2[1] + ydelta * ymult]
	leftsidept1,leftsidept2 = [pt1[0] + xdelta * xmult * -1,pt1[1] + ydelta * ymult * -1],[pt2[0] + xdelta * xmult * -1,pt2[1] + ydelta * ymult * -1]

	return [leftsidept1,leftsidept2],[rightsidept1,rightsidept2]

# function for getting however not really useful for real line creation
def get_points(pts1,pts2,staggercoords):
	if pts1 == pts2:
		return []
	leftpts,rightpts = calc_xydelta(pts1,pts2,staggercoords)
	leftpts = [i + ['l'] for i in leftpts]
	rightpts = [i + ['r'] for i in rightpts]
	coords = [pts1,pts1,pts2]
	midpts = [i + ['m'] for i in coords]
	return midpts + leftpts+rightpts


# creates a string representation of both the left and right lines
def make_lr_line(coords,staggercoords):
	leftline,rightline = [],[]
	count = 0
	for pt in coords:
		if len(pt) == 2:
			if count == 0:
				count = 1
			else:
				leftpts,rightpts = calc_xydelta(oldpt,pt,staggercoords)
				leftline += leftpts
				rightline += rightpts
			oldpt = pt

	return [str(leftline),str(rightline)]

# from a given data frame and stagger distance
# creates stagger lines a given ft distance away the centerline
def make_stagger_lines(data,ftdistance):
	# getting stagger distance from the ft distance
	staggercoords = stagger(ftdistance)

	# going through each header to find the string repr 
	# of cooords
	for i in data.columns.values:
		if 'coord' in str(i).lower():
			coordheader = i


	# iterating through each normal string line
	llines,rlines = [],[]
	count = 0
	for i in data[coordheader].values.tolist():
		i = get_cords_json(i)
		lftline,rghtline = make_lr_line(i,staggercoords)
		llines.append(lftline)
		rlines.append(rghtline)
		count += 1

	data['left-line'] = llines
	data['right-line'] = rlines

	return data

# from created coord dataframe makes a make_map input dataframe table to visualize
def make_coords_output(data):
	data1 = data[['gid','coords']]
	data1['POS'] = 'm'

	data2 = data[['gid','left-line']]
	data2['POS'] = 'l'
	data2['coords'] = data['left-line']

	data3 = data[['gid','right-line']]
	data3['POS'] = 'r'
	data3['coords'] = data['right-line']

	data = pd.concat([data1[['gid','coords','POS']],data2[['gid','coords','POS']],data3[['gid','coords','POS']]])
	return data

