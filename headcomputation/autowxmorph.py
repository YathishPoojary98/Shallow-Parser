#Latest autowxmorph

import sys
from wxconv import WXC
con = WXC(order="utf2wx",lang="kan")
ord_chars = {3202:'M'}
with open(sys.argv[1],"r",encoding="utf-8") as f:
	lines = f.readlines()
outfilename = sys.argv[1]
with open(outfilename,"w",encoding="utf-8") as f:
	for line in lines:
		if len(line.split("\t"))>=4 and "<fs" in line:
			splits = line.split("\t")
			word = splits[1]
			pos = splits[2]
			comps = splits[3].split("=")
			second = comps[1].split(",")
			root = second[0]
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
			if word!="":
				word = con.convert(word)
				word = word.replace("_",'')
				word = word.replace(" ",'')
			root = con.convert(root)
			root = root.replace("_",'')
			root = root.replace(" ",'')
			second[0] = root
			second[-2] = second[-1]
			second = ",".join(second)
			comps[1] = second+"'>\n"
			splits[3] = "=".join(comps)
			pos = pos.split("__")[-1]
			splits[2] = pos
			splits[1] = word
			res = "\t".join(splits)
			#print(res)
			f.write(res)
		else:
			f.write(line)
