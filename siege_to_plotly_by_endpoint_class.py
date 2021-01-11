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

siegelogentries,headers = siegelogparser.main(directory)
#print(siegelogentries)

fig = go.Figure()

#the below script will build a graph that tracks the response times for different types of endpoint/request.

xname='Resp Time'
yname='Trans Rate'

sort_by='Concurrent'
show_labels=['Concurrent']



for vm in siegelogentries:
	
	this_series_x=[]
	this_series_y=[]
	series_labels=[]
		
	this_series=sorted(siegelogentries[vm], key=lambda i: i[sort_by],reverse=True)
	#print(vm)
	for datapoint in this_series:
		
		#print(datapoint[sort_by],datapoint[xname],datapoint[yname])
		
		this_series_x.append(datapoint[xname])
		this_series_y.append(datapoint[yname])
		
		node_label=''
		for k in show_labels:
			s="%s: %s\n" %(str(k),datapoint[str(k)])
			node_label+=s
		series_labels.append(node_label)
		
	fig.add_trace(go.Scatter(x=this_series_x,y=this_series_y,text=series_labels,name=vm))
	
	#print(vm)
	#print(series_labels)
	#print(this_series_x)
	#print(this_series_y)

fig.update_layout(
xaxis=dict(title=xname),
yaxis=dict(title=yname)
)

plotly.offline.plot(fig,
	filename="siege_report_by_endpoint_class.html"
)
