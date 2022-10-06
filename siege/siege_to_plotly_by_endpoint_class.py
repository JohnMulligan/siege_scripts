#!/bin/python3
import re
from datetime import date
import datetime

import plotly
import plotly.graph_objs as go
import os
from statistics import mean,median
from plotly.subplots import make_subplots
directory = sys.argv[1]

'''
input log filenames should
1. be in the logs folder
2. have the structure enpointclass_vmidnumber.log
3. you know, like, legacy_queries_88.log or static_assets_new_523.log
'''

def lineval_processor(val):
	try:
		output=float(val)
	except:
		output= datetime.datetime.strptime(val,'%Y-%m-%d %H:%M:%S')
	return(output)

def siegelogparser(directory = directory):
	entries = {}
	flist = [f for f in os.listdir(directory) if f.endswith('.log')]
	endpoint_labels=[]
	for fname in flist:
		d = open(os.path.join(directory,fname),'r')
		t = d.read()
		t = re.sub('^\s+','',t)
		t = re.sub('\s+$','',t)
		t = re.sub(',\s+','\t',t)
		d.close()
		endpoint_label=fname
		endpoint_labels.append(endpoint_label)
		lines = [l for l in t.split('\n') if l != '']
		entries[endpoint_label]=[]
		for line in lines:
			linelist=line.split('\t')
			if lines.index(line)==0:
				headers=linelist
			elif "siege aborted" not in line:
				linedict={headers[c]:lineval_processor(linelist[c]) for c in range(len(headers))}
				entries[endpoint_label].append(linedict)
		
	#print(entries)
	endpoint_labels=list(set(endpoint_labels))
	return entries,headers,endpoint_labels

siegelogentries,headers,endpoint_labels = siegelogparser(directory)
#print(siegelogentries)

#the below script will build a graph that tracks the response times for different types of endpoint/request.

bar_y_name='Resp Time'
scatter_y_name='Trans Rate'

sort_by='Concurrent'
show_labels=['Concurrent']


for endpoint_label in endpoint_labels:

	# Create figure with secondary y-axis
	fig = make_subplots(specs=[[{"secondary_y": True}]])
	
	response_times={}
	transaction_rates={}
	c_keys=[]
	
	this_series=sorted(siegelogentries[endpoint_label], key=lambda i: i[sort_by],reverse=True)
	n=0
	
	x_vals=[int(datapoint[sort_by]) for datapoint in this_series]
	
	series={x_val:{bar_y_name:[],scatter_y_name:[]} for x_val in x_vals}
	
	for datapoint in this_series:
		x=int(datapoint[sort_by])
		bar_y=datapoint[bar_y_name]
		scatter_y=datapoint[scatter_y_name]
		
		series[x][bar_y_name].append(bar_y)
		series[x][scatter_y_name].append(scatter_y)
	
	x_series=sorted(list(set(x_vals)))
	
	scatter_y_series=[sum(series[x_val][scatter_y_name])/len(series[x_val][scatter_y_name]) for x_val in x_series]
	
	bar_y_series=[sum(series[x_val][bar_y_name])/len(series[x_val][bar_y_name]) for x_val in x_series]
	
	
	fig.add_trace(go.Bar(x=x_series,y=bar_y_series,name=bar_y_name))
	fig.add_trace(go.Scatter(x=x_series,y=scatter_y_series,mode='markers+lines',name=scatter_y_name),secondary_y=True)
	
	fig.update_layout(
    	title_text=endpoint_label
	)
	
	fig.update_xaxes(title_text="Concurrent Users")
	
	fig.update_yaxes(title_text="Response Time (seconds)",secondary_y=False)
	fig.update_yaxes(title_text="Transaction Rate (transactions/second)",secondary_y=True)
	
	
	plotly.offline.plot(fig,
		filename="siege_report_%s.html" %endpoint_label
	)
