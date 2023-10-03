import sys

inputfile = sys.argv[1]
with open(inputfile,"r") as f:
    data = f.readlines()
    
data = [i for i in data if i!="\n"]


key_words = ["<document","<head>","</head>","</document"]
with open("conll.txt","w") as outf:
    for i in range(len(data)):
        line = data[i] 
        #print(f"Line --> {line}")
        if i<len(data)-1:
            next_line = data[i+1]
        else:
            next_line = "NULL"

        flag = 0
        for key in key_words:
            if key in line:
                flag = 1
                #f.write(f"{line}")
                break
        if flag==0:
            if "((" in line or "))" in line or "<Sentence" in line:
                #f.write(f"{line}")
                continue
            #print(f"Line --> {line}")
            if "</Sentence" in line:
                outf.write("\n")
            else:
                word = line.split("\t")[1]
                outf.write(f"{word}\n")
        
