import re
import pandas
import plotly.express as px
import sys

try:
	fname=sys.argv[1]
except:
	fname='data.txt'

'''
first, run the below bash script as the docker process runs:
while true; do docker stats --no-stream >> data.txt; done
then, run this script

specifying the data filename, as in:

python stats_to_plotly.py mydata.txt

default filename is 'data.txt'
'''

try:
	d=open(fname,"r")
	t=d.read()
	d.close()
except:
	print("bad filename: %s" %fname)

t=re.sub(" %","%",t)
t=re.sub(" / ","/",t)

blocks=[re.sub("  +","\t",i) for i in t.split("CONTAINER ")]

blocks=[i for i in blocks]
t=0

CPU=[]
MEM=[]
ts=[]
CONTAINER=[]


for block in blocks:

	lines=block.split('\n')
	headers=lines[0].split('\t')
	for line in lines[1:]:
		cols=line.split('\t')
		if len(cols)>1:
			entry={headers[i]:cols[i] for i in range(len(cols))}
			CONTAINER.append(entry["NAME"])
			CPU.append(float(re.sub("%","",entry["CPU%"])))
			MEM.append(float(re.sub("%","",entry["MEM%"])))
			ts.append(t)

	t+=1

data={"CPU":CPU,"MEM":MEM,"t":ts,"CONTAINER":CONTAINER}

df=pandas.DataFrame(data)

fig=px.line(df,x="t",y="CPU",color="CONTAINER")
fig.update_layout(title='DOCKER CPU USAGE',
                   xaxis_title='docker stats time step',
                   yaxis_title='% CPU USAGE')

fig.show()

fig=px.line(df,x="t",y="MEM",color="CONTAINER")
fig.update_layout(title='DOCKER MEM USAGE',
                   xaxis_title='docker stats time step',
                   yaxis_title='% MEM USAGE')

fig.show()