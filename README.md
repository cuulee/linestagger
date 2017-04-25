# linestagger
See pictures and example roadway visualization tool.

Helps visualize two-way roadways represented by a oneway line. Pretty simple usage, either input a nlgeojson dataframe or convert to one from a geodataframe using nlgeojson. ( i.e. nl.geodf_tonldf(geodataframe), done)

From there your simply using a dataframe file typed how I usually do spatial analysis, nothing crazy. Input that dataframe, into make_stagger_lines() to get a dataframe with two fields added representing the left and right roads respectively which correspond to the proper side of the road driving wise. (in NA at least) 

Another function exist called make_coords_output() which takes that dataframe and makes it into an easily stylable dataframe that can be easily put into a map to see the output.

# Example
```
import linestagger
import pandas as pd
import mapkit as mk

# reading a csv
data = pd.read_csv('example.csv')

# creating the left and right stagger fields 20 feet from the center line
data = linestagger.make_stagger_lines(data,20)

# creating an easily stylable dataframe from output
data = linestagger.make_coords_output(data)

# adding colorkey field
# styling based on the POS field of the line
# i.e. middle,left or right
data = mk.make_colorkey(data,'POS')

# creating mapout
mk.make_map([data,'lines'])

```

