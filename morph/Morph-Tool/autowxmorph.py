#Latest autowxmorph

import sys
from wxconv import WXC
con = WXC(order="utf2wx",lang="kan")
ord_chars = {3202:'M'}
with open(sys.argv[1],"r",encoding="utf-8") as f:
	lines = f.readlines()
outfilename = sys.argv[1].replace("out","wxout")
with open(outfilename,"w",encoding="utf-8") as f:
	for line in lines:
		if len(line.split("\t"))>=4 and "<fs" in line:
			comps = line.split("=")
			second = comps[1].split(",")
			utf = second[-2]
			ords = [ord(char) for char in utf]
			if utf==0:
				second[-1]=0
			elif utf=='':
				second[-1]=''
			else:
				ord_keys = list(ord_chars.keys())
				for key in ord_keys:
					if chr(key) in utf:
						utf = utf.replace(chr(key),ord_chars[key])
				second[-1]=con.convert(utf)
				second[-1]=second[-1].replace("_",'')
				second[-1]=second[-1].replace(" ",'')
				
			second = ",".join(second)
			comps[1] = second+"'>\n"
			res = "=".join(comps)
			#print(res)
			f.write(res)
		elif "<Sentence id" in line:
			line = line.replace("'",'"')
			f.write(line)
		else:
			f.write(line)
