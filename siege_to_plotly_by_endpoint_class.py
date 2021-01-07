#!/bin/python3
import re
from datetime import date
import plotly
import plotly.graph_objs as go
import sys
import os
import siegelogparser
from statistics import mean

directory = sys.argv[1]

siegelogentries = siegelogparser.main(directory)
#print(siegelogentries)

fig = go.Figure()

#the below script will build a graph that tracks the response times for different types of endpoint/request.

xname='resp time'
yname='trans rate'


#available keys are
all_keys=['elap time', 'okay', 'failed', 'data trans', 'trans rate', 'concurrent', 'resp time', 'throughput', 'trans']
#add them to label_keys to make that metric appear as a label on hover over a node
label_keys=['concurrent']

for vm in siegelogentries:
	
	this_series_x=[]
	this_series_y=[]
	series_labels=[]
	
	for timestamp in siegelogentries[vm]:
		
		datapoint=siegelogentries[vm][timestamp]
		
		this_series_x.append(datapoint[xname])
		this_series_y.append(datapoint[yname])
		
		node_label=''
		for k in label_keys:
			s="%s: %s\n" %(str(k),datapoint[str(k)])
			node_label+=s
		series_labels.append(node_label)
		
	fig.add_trace(go.Scatter(x=this_series_x,y=this_series_y,text=series_labels,name=vm))
	
	print(vm)
	print(series_labels)
	print(this_series_x)
	print(this_series_y)

fig.update_layout(
xaxis=dict(title=xname),
yaxis=dict(title=yname)
)

plotly.offline.plot(fig,
	filename="siege_report_by_endpoint_class.html"
)
