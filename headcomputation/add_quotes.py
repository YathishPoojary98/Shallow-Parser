import sys


with open(sys.argv[1],"r") as infile:
	lines = infile.readlines()

for line in lines:
	if "head" in line:
		dummy = line.split("head=")
		heads = dummy[1]
		if "'" not in heads and '"' not in heads:
			head_name = heads.split(">")[0]
			final_head = f'"{head_name}">'
			dummy[1] = final_head
		line = "head=".join(dummy)
		print(line)
	elif "name" in line:
		dummy = line.split("name=")
		heads = dummy[1]
		if "'" not in heads and '"' not in heads:
			head_name = heads.split(">")[0]
			final_head = f'"{head_name}">'
			dummy[1] = final_head
		line = "name=".join(dummy)
		print(line)
	else:
		print(line)
