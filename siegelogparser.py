
import re
import datetime
import os
import sys

directory = sys.argv[1]

def main(directory = directory):
	entries = {}
	headers = ['date & time','trans','elap time','data trans','resp time','trans rate','throughput','concurrent','okay','failed']

	flist = [f for f in os.listdir(directory) if f.endswith('.log')]

	for fname in flist:
		d = open(os.path.join(directory,fname),'r')
		t = d.read()
		t = re.sub(' +',' ',t)
		d.close()
		vm_id = re.search('.*(?=\.log)',fname).group(0)
		#print(vm_id)
		lines = [l for l in t.split('\n')[1:] if l != '']
		#print(lines)
		entries[vm_id] = {}

		for line in lines:
			linelist = line.split(', ')
			#print(linelist)
			date,time = linelist[0].split(' ')
			year,month,day = date.split('-')
			hour,minute,second = time.split(':')
			dt = datetime.datetime(int(year),int(month),int(day),int(hour),int(minute),int(second))
			#print(dt)
			timestamp = dt.timestamp()
			entries[vm_id][timestamp] = {}
			c=0
			for entry in linelist:
				#print(headers[c],entry)
				try:
					e = float(entry)
				except:
					e = entry
				entries[vm_id][timestamp][headers[c]] = e
			
				c+=1
	print(entries)
	return entries

if __name__ == '__main__':
	main()
