import re
import datetime
import os
import sys

directory = sys.argv[1]

def lineval_processor(val):
	try:
		output=float(val)
	except:
		output= datetime.datetime.strptime(val,'%Y-%m-%d %H:%M:%S')
	return(output)

def main(directory = directory):
	entries = {}
	flist = [f for f in os.listdir(directory) if f.endswith('.log')]

	for fname in flist:
		d = open(os.path.join(directory,fname),'r')
		t = d.read()
		t = re.sub('^\s+','',t)
		t = re.sub('\s+$','',t)
		t = re.sub(',\s+','\t',t)
		d.close()
		vm_id = re.search('.*(?=\.log)',fname).group(0)
		#print(vm_id)
		lines = [l for l in t.split('\n') if l != '']
		#print(lines)
		entries[vm_id] = []
		
		for line in lines:
			linelist=line.split('\t')
			if lines.index(line)==0:
				headers=linelist
			elif "siege aborted" not in line:
				linedict={headers[c]:lineval_processor(linelist[c]) for c in range(len(headers))}
				entries[vm_id].append(linedict)
		
	#print(entries)
	return entries,headers

if __name__ == '__main__':
	main()
