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

headers = {
'okay':
{'color':'#808000','operation':'sum'}, 

'failed':

{'color':'#00FF00','operation':'sum'},

'trans rate':
{'color':'pink','operation':'sum'},

'concurrent':

{'color':'grey','operation':'sum'},

'resp time':

{'color':'orange','operation':'average'}

}

time_window=30

#This function rolls up a few 
v=0

time_anchors = []

output_dict = {header:{} for header in headers.keys()}

for vm in siegelogentries.keys():
	
	timestamps = list(siegelogentries[vm].keys())
	timestamps.sort()
	
	if v==0:
		time_anchors += timestamps

	else:	
		for timestamp in timestamps:
			closest_match=min(time_anchors, key=lambda x:abs(x-timestamp))
			if abs(timestamp-closest_match)>time_window:
				time_anchors.append(timestamp)
	
	time_anchors.sort()
	print(time_anchors)
	
	for header in headers.keys():
		output_dict[header] = {nominal_timestamp:[] for nominal_timestamp in time_anchors}
	v+=1


for vm in siegelogentries.keys():
	timestamps = list(siegelogentries[vm].keys())
	for header in headers.keys():	
		for timestamp in timestamps:
			value = siegelogentries[vm][timestamp][header]
			nominal_timestamp =min(time_anchors, key=lambda x:abs(x-timestamp))			
			output_dict[header][nominal_timestamp].append(value)




c = 0

y_vals = []

start_time = min(time_anchors)
x_vals = timestamps
adjusted_x_vals = [i-start_time for i in x_vals]
print("TIME VALS")
for i in range(0,len(adjusted_x_vals)-1):
	print(adjusted_x_vals[i],x_vals[i])


e=1
for header in output_dict.keys():
	x_vals = list(output_dict[header].keys())
	y_vals = []
	if header in ['trans rate','resp time']:
		print(header)
	for x in x_vals:
		ylist = output_dict[header][x]
		if headers[header]['operation']=='sum':
			y_val = sum(ylist)
		elif headers[header]['operation']=='average':
			y_val = mean(ylist)
		y_vals.append(y_val)
		if header in ['trans rate','resp time']:
			print(x,y_val)
	adjusted_x_vals = [i-start_time for i in x_vals]
	
		
			
	if e!=1:
		fig.add_trace(go.Scatter(x=adjusted_x_vals,y=y_vals,name=header,yaxis="y%d" %e,line=dict(color=headers[header]['color'])))
	else:
		fig.add_trace(go.Scatter(x=adjusted_x_vals,y=y_vals,name=header,yaxis="y" ,line=dict(color=headers[header]['color'])))
	e +=1



fig.update_layout(

yaxis=dict(title="okay"),

yaxis2=dict(title="failed",overlaying="y",side="right",anchor="free"),

yaxis3=dict(title="trans rate",overlaying="y",side="right",anchor="free"),

yaxis4=dict(title="concurrent",overlaying="y",side="right",anchor="free"),

yaxis5=dict(title="resp time",overlaying="y",side="right",anchor="free"),

yaxis6=dict(title="(d resp_time/d trans_rate)",overlaying="y",side="right",anchor="free")


)


plotly.offline.plot(fig,
	filename="siege_report_by_metric.html"
)
