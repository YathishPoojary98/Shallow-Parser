from wxconv import WXC
import sys
from charsreplace import *
from replaceback import *
from morph_hash import *
from suff_dict import *
import re
from langdetect import detect
from gender_number import *
from category_map import *
from template_root_dict import *
from template_suffix_dict import *
from suffix_morpheme_dict import *

with open("/home/yathish_poojary/Yathish/Dependency_Parser/Parser/morph/Morph-Tool/exceptions.txt","r") as f1:
    exceptions = f1.readlines()
    exceptions = [i.strip() for i in exceptions]
    exception_roots = [i.split(",")[0] for i in exceptions]

with open("/home/yathish_poojary/Yathish/Dependency_Parser/Parser/morph/Morph-Tool/exceptional_words.txt","r") as f2:
    exception_words = f2.readlines()
    exception_words = [i.strip() for i in exception_words]

utf2wx = WXC(order="utf2wx",lang="kan")
wx2utf = WXC(order="wx2utf",lang="kan")

dictionary_words = []
f = open("/home/yathish_poojary/Yathish/Dependency_Parser/Parser/morph/Morph-Tool/Splitter/Dictionaries/wx_dictionary2.txt", "r")
for line1 in f:
	dictionary_words.append(line1.strip())

def search_in_dict(word):
	if word in dictionary_words:
		return True
	else:
		return False


def first_alpha_index(string):
    match = re.search(r'[a-zA-Z]', string)
    if match:
        return match.start()
    else:
        return -1
    
def check_string_type(input_string):
    kannada_regex = re.compile(r'^[\u0C80-\u0CFF]+$')
    english_regex = re.compile(r'^[a-zA-Z]+$')
    number_regex = re.compile(r'^[0-9]+$')
    
    if kannada_regex.match(input_string):
        return "Kannada Word"
    elif english_regex.match(input_string):
        return "English Word"
    elif number_regex.match(input_string):
        return "Number String"
    else:
        return "Mixed"
    
    
def match(text, pattern):
    matching_length = 0
    for a, b in zip(text, pattern):
        if a != b:
            break
        matching_length += 1
    return matching_length

def length(string):
    return len(string)

def search_ika(word,suffix,to_replace):
    r = word.replace('ika',to_replace)
    #print(f"Word : {r}")
    if search_in_dict(r):
        if suffix==0:
            s = "ಇಕ"
        else:
            s = "ಇಕ+"+suffix
        return (r,s)
    return "NULL","NULL"


def handle_ika(wx_word,suffix):
    ika_dict = {'A':['A','a'],'E':['E','i','I','e'],'O':['O','u','U','o']}
    #print(f"handle_ika is called for word : {wx_word}")
    for k in ika_dict.keys():
        #print(f"k : {k}")
        if k in wx_word[:3]:
            #print("Yes")
            if type(ika_dict[k])==list:
                for v in ika_dict[k]:
                    w = wx_word[:3].replace(k,v) + wx_word[3:]
                    r,s = search_ika(w,suffix,'a')
                    #print(f"r : {r} , s : {s}")
                    if r!="NULL" and s!="NULL":
                        return (r,s)
                    c = ''
                    if k=='A':
                        c = w[-4]+"u"
                    if k=='E':
                        c = "i"
                    r,s = search_ika(w,suffix,f"{c}")
                    if r!="NULL" and s!="NULL":
                        return (r,s)
    return (wx_word,suffix)


def handle_Awmaka(wx_word,suffix):
    to_check = ['a','eV']
    for c in to_check:
        w = wx_word.replace("Awmaka",c)
        if search_in_dict(w):
            if suffix==0:
                s = 'ಆತ್ಮಕ'
            else:
                s = "ಆತ್ಮಕ+"+suffix
            return w,s
    return wx_word,suffix


def handle_aweV(wx_word,suffix):
    to_check = ['a','eV','i','isu']
    for c in to_check:
        w = wx_word.replace("aweV",c)
        if search_in_dict(w):
            if suffix==0:
                s = 'ಅತೆ'
            else:
                s = "ಅತೆ+"+suffix
            return w,s
    return wx_word,suffix


def find_root(word,cat,removed_suffs):
    w = utf2wx.convert(word)
    #print(f"Find root called with word : {w}")
    f = 0
    dictionaries = {'v':verb_root_dict,'n':noun_root_dict,'adv':adv_root_dict,'nst':nst_root_dict,'adj':adj_root_dict,'num':num_root_dict,'pn':pn_root_dict}
    if cat not in dictionaries.keys():
        return word,removed_suffs
    d = dictionaries[cat]
    suffixes = list(d.keys())
    suffixes = sorted(suffixes, key=length, reverse=True)
    global root_return
    global val
    for suff in suffixes:
            #print(suff)
            if w.endswith(suff):
                #print(f"Suff : {suff}")
                if suff.startswith("Md") and not w[:-len(suff)].endswith("goV"):
                    continue
                if w.endswith('goVlYlYu'):
                    continue
                #print("Here")
                removed_suffs.append(suff)
                i = len(w) - len(suff)
                #print(i)
                if (w[:i])[-2:] == 'lY' and (w[:i])[-4:-2] != 'lY' and (w[:i])[:-2].endswith("goV"):
                    to_add ='lY'+d[suff]
                    #print(f"to_add : {to_add}")
                else:
                    to_add = d[suff]
                pre = w[:i]+ to_add
                #print(f"Pre : {pre}, suff : {suff}")
                if pre=='':
                    return (word,removed_suffs)
                f = 1
                if search_in_dict(pre):
                    return (pre,removed_suffs)
                if char_replace(pre) in k.keys():
                    temp = char_replace(pre)
                    val = replaceback(k[temp])
                    if root_return == -1:
                        #print(f"Root return : {root_return} , val : {val} , pre : {pre}")
                        root_return = val
                    if val != pre and len(val)<len(pre):
                        #print(f"Find root called again with pre : {pre}")
                        return find_root(wx2utf.convert(pre),cat,removed_suffs)
                        #return (replaceback(k[temp]),removed_suffs)

                if root_return==-1:
                    return find_root(wx2utf.convert(pre),cat,removed_suffs)
                else:
                    #print(f"Root returned : {root_return}")
                    #print(f"Removed Suffixes : {removed_suffs}")
                    return (wx2utf.convert(root_return),removed_suffs)
    if f==0:
        #print(f"w : {w} , removed_suffs : {removed_suffs}")
        return (w,removed_suffs)


def find_gn(cat,removed_suffixes,gender,sg_pl):
    if (gender=="NULL" or sg_pl=="NULL") and len(removed_suffixes)!=0 :
        #reverse_removed_suffs = removed_suffixes[::-1]
        #print(f"Removed Suffixes : {removed_suffixes}")
        for i in removed_suffixes:
            #print(i)
            s = f"{cat},{i}"
            if s in gn.keys():
                g,sp = gn[s].split(",")
                #print(f"g : {g} , sp : {sp}")
                if gender == "NULL":
                    gender = g
                if (sg_pl == "NULL" or sg_pl=='sg') and sp!="NULL" :
                    sg_pl = sp
    return gender,sg_pl

def find_morpheme_string(word, root, cat, suff_list):
    #if len(root) > len(word):
        #return suff_list
    ind = match(word,root)
    rem = word[ind:]
    dictionaries = {'v': verb_suffix_dict, 'n': noun_suffix_dict, 'adv': adv_suffix_dict, 'nst': nst_suffix_dict, 'adj': adj_suffix_dict, 'num': num_suffix_dict, 'pn': pn_suffix_dict}
    if cat not in dictionaries.keys():
        return ("NULL","NULL")
    d = dictionaries[cat]
    suffixes = list(d.keys())
    suffixes = sorted(suffixes, key=len, reverse=True)
    #print(f"Rem : {rem}")
    match_found = 0
    for key in suffixes:
        #print(f"Key to match : {key}")
        if rem.endswith(key):
            if key.startswith("Md") and not word[:-len(key)].endswith("goV"):
                continue
            match_found = 1
            #print(f"Matched key : {key} , rem : {rem}")
            suff_list.append(key)
            if (word[:-len(key)])[-2:] == 'lY' and (word[:-len(key)])[-4:-2] != 'lY' and (word[:-len(key)])[:-2].endswith("goV"):
                word = word[:-len(key)] + 'lY' + d[key]
            else:
                if rem[:-len(key)]=='':
                    word = root
                else:
                    word = word[:-len(key)] + d[key]
            #print(word)
            return find_morpheme_string(word, root, cat, suff_list)
    if match_found == 0 and rem != '':
        return ("NULL","NULL")
    #print(f"Suff list : {suff_list}")
    to_del = ['uu']
    for del_key in to_del:
        if del_key in suff_list:
            suff_list.remove(del_key)
    suffix_kan = []
    suff_comps = []
    for ele in suff_list[::-1]:
        #print(f"ele : {ele}")
        if ele not in morpheme_dict.keys():
            res = generate_comps(ele,suffixes,[],d)
            #print(res)
            if len(res)==0:
                return ("NULL","NULL")
            suff_comps+=res
        else:
            #print(f"In else, ele : {ele}")
            suff_comps.append(ele)
    #print(f"Suffix comps : {suff_comps}")
    for ele in suff_comps:
        if ele not in morpheme_dict.keys():
            return ("NULL","NULL")
        val = morpheme_dict[ele]
        if (val.endswith("+ಅ") or val.endswith("+ಉ")) and suff_comps.index(ele) != len(suff_comps)-1:
            val = val[:-2]
        suffix_kan.append(val)
        #print(f"SUff kan : {suffix_kan}")
    return ("+".join(suffix_kan),suff_list)


def generate_comps(suffix,suffixes,comps,d):
    #print(f"Suffix now : {suffix}")
    s = suffix
    #print(f"Suffix then : {suffix}")
    #print(len(suffixes))
    for i in suffixes:
        if suffix.endswith(i) and len(s)>=len(i) and i in morpheme_dict.keys():
            #print(f"Testing suffix : {suffix}")
            comps.append(i)
            #print(f"Appending : {i}")
            suffix = suffix[:-len(i)]
            if suffix!= '':
                suffix += d[i]
            #print(f"Suff : {suffix}")
            return generate_comps(suffix,suffixes,comps,d)
    #print(f"Suffix : {suffix}")
    if suffix=='':
        #print(f"Comps : {comps[::-1]}")
        return comps[::-1]
    else:
        #print("Inside else")
        return [suffix]+comps[::-1] 


romans = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X',          'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX',          'XXI', 'XXII', 'XXIII', 'XXIV', 'XXV', 'XXVI', 'XXVII', 'XXVIII', 'XXIX', 'XXX',          'XXXI', 'XXXII', 'XXXIII', 'XXXIV', 'XXXV', 'XXXVI', 'XXXVII', 'XXXVIII', 'XXXIX', 'XL',          'XLI', 'XLII', 'XLIII', 'XLIV', 'XLV', 'XLVI', 'XLVII', 'XLVIII', 'XLIX', 'L']


lower_romans = [x.lower() for x in romans]






#print(f"Length : {len(k)}")
        
inputfile = sys.argv[1]
with open(inputfile,"r") as f:
    data = f.readlines()
    
data = [i for i in data if i!="\n"]

vf_flag = 0
vng_flag = 0

key_words = ["<Sentence","</Sentence","<document","<head>","</head>","</document"]
with open("/home/yathish_poojary/Yathish/Dependency_Parser/Parser/morph/Morph-Tool/rootsandsuff.txt","w") as f:
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
            if "((" in line or "))" in line:
                #f.write(f"{line}")
                continue
            #print(f"Line --> {line}")
            wf = 0
            #temp = line.split("\t")
            #print(temp)
            try_flag = False
            word = line.split("\t")[1]
            pos = (line.split("\t")[2]).strip()
            if "((" in next_line or "))" in next_line:
                next_pos = "NULL"
            elif next_line != "NULL":   
                next_pos = (next_line.split("\t")[2]).strip()
            else:
                next_pos = "NULL"

            gender = "NULL"
            sg_pl = "NULL"
            person = "NULL"
            root_return = -1
            val = ""
            l = "NULL"
            rs = []
            found_in_dict = False
            gn_found = False
            cat_found = False
            if pos in fs_dict_single.keys():
                    cat_found = True
                    cat = fs_dict_single[pos]
            if pos in fs_dict_double.keys():
                    cat_found = True
                    cat = fs_dict_double[pos]
            root = word
            suff = 0
            string_type = check_string_type(word[0])
            if string_type!='English Word':
                w = utf2wx.convert(word)
                w = w.replace("_","")
                w = w.replace(" ","")
                roman_word_w = char_replace(w)
                #print(f"Word : {word}")
                if (word not in romans) and (word not in lower_romans):
                    if roman_word_w[0].isalpha()==True:
                        if word in const_dict.keys():
                            #print("Here")
                            wf=1
                            #print(f"Word : {word}")
                            root = (const_dict[word])[0]
                            suff = (const_dict[word])[1]
                            #print(f"Length : {len(const_dict[word])}")
                            if len(const_dict[word])>=3:
                                gender = (const_dict[word])[2]
                                if len(const_dict[word])>3:
                                    sg_pl = (const_dict[word])[3]
                                gn_found=True
                            #suff += " const_dict"
                        #print(f"Root1 : {root}")
                        wx_word = utf2wx.convert(word)
                        wx_word = wx_word.replace("_","")
                        wx_word = wx_word.replace(" ","")
                        if search_in_dict(wx_word):
                        	found_in_dict = True
                        if found_in_dict == False:
                            roman_word = char_replace(wx_word)
                            if suff==0:
                                keys = ends_with.keys()
                                keys = sorted(keys, key=length, reverse=True)
                                for key in keys:
                                    if wx_word.endswith(key):
                                        res = ends_with[key]
                                        if type(res)==list:
                                            suff = res[0]
                                            gender = res[1]
                                            if len(res)>2:
                                                sg_pl = res[2]
                                            #gn_found=True
                                        else:
                                            suff = res
                                        #suff += " ends with"
                                        break

                            if roman_word in k.keys() and (word not in const_dict.keys()):
                                root = k[roman_word]
                                root = wx2utf.convert(replaceback(root))
                                suffixes_removed = []
                                z,rs = find_root(word,cat,suffixes_removed)
                                #print(f"Word : {word} , Suffixes removed : {rs}")
                            #if wx_word in dictWords:
                            else: 
                                #wf = 1
                                #print(f"wf : {wf}")
                                if wf!=1:
                                    #chopper_res = pratyaya_chopper(word,3)
                                    #root = (chopper_res[2].split("ಮೂಲ ಪದ : ")[1]).split("\n")[0]
                                    suffixes_removed = []
                                    r,rs = find_root(word,cat,suffixes_removed)
                                    #print(f"Word : {word} , Suffixes removed : {rs}")
                                    root = wx2utf.convert(r)
                                    #print(f"Root 2 : {root}")
                            #f.write(f"{line}")
                            #print(f"Root : {root}")
                            #print(f"Suff : {suff}")
                            root_for_suff = utf2wx.convert(root)
                            if root_for_suff==wx_word:
                                suff=0
                            else:
                                if suff==0:
                                    if root_for_suff in wx_word:
                                        temp = len(root_for_suff)
                                        temp1 = wx_word[temp:]
                                        #print(f"WX Word : {wx_word}, Temp : {temp}")
                                        #print(f"Temp1 : {temp1}")
                                        keys = rootrem.keys()
                                        keys = sorted(keys, key=length, reverse=True)
                                        for key in keys:
                                            if key==temp1:
                                                suff = 1
                                                res = rootrem[key]
                                                if type(res)==list:
                                                    suff = res[0]
                                                    gender = res[1]
                                                    if len(res)>2:
                                                        sg_pl = res[2]
                                                    #gn_found=True
                                                else:
                                                    suff = res
                                                #suff += " rootrem"

                                if suff==0:
                                    if root_for_suff[:-1] in wx_word:
                                        temp = len(root_for_suff)-1
                                        temp1 = wx_word[temp:]
                                        keys = root1.keys()
                                        keys = sorted(keys, key=length, reverse=True)
                                        for key in keys:
                                            if key==temp1:
                                                suff = 1
                                                res = root1[key]
                                                if type(res)==list:
                                                    suff = res[0]
                                                    gender = res[1]
                                                    if len(res)>2:
                                                        sg_pl = res[2]
                                                    #gn_found=True
                                                else:
                                                    suff = res
                                                #suff += " root1"

                                if suff==0:
                                    if root_for_suff[:-2] in wx_word:
                                        temp = len(root_for_suff)-2
                                        temp1 = wx_word[temp:]
                                        keys = root2.keys()
                                        keys = sorted(keys, key=length, reverse=True)
                                        for key in keys:
                                            if key==temp1:
                                                suff = 1
                                                res = root2[key]
                                                if type(res)==list:
                                                    suff = res[0]
                                                    gender = res[1]
                                                    if len(res)>2:
                                                        sg_pl = res[2]
                                                    #gn_found=True
                                                else:
                                                    suff = res
                                                #suff += " root2"
                        else:
                            if wf!=1:
                                root = word
                                suff = 0
                    else:
                        ind = first_alpha_index(roman_word_w)
                        found = 0
                        if ind!=-1:
                            root = roman_word_w[:ind]
                            #print(f"{root},{replaceback(roman_word_w[ind:])}")
                            for key in numbers_dict.keys():
                                if key==replaceback(roman_word_w[ind:]):
                                    found = 1
                                    res = numbers_dict[key]
                                    if type(res)==list:
                                        suff = res[0]
                                        if len(res)>1:
                                            sg_pl = res[1]
                                    else:
                                        suff = res
                            if found==0:
                                for j in ends_with.keys():
                                    if j==replaceback(roman_word_w[ind:]):
                                        #print(f"{j},{replaceback(roman_word_w[ind:])}")
                                        found=1
                                        res = ends_with[j]
                                        if type(res)==list:
                                            suff = res[0]
                                        else:
                                            suff = res
            
                                       
            if gn_found==False:
                try_flag = True
                w = utf2wx.convert(word)
                r = utf2wx.convert(root)
                match_index = match(w,r)
                s = w[match_index:]
                if s=='':
                	s='NULL'
                t = f"{cat},{s}"
                possible_cats = ['n','num','pn','v']
                if cat in possible_cats:
                    for exception in exceptions:
                        a = exception.split(",")[0]
                        b = exception.split(",")[-1]
                        if root==a and (s==b or b=='anysuffix' or s.startswith(b)):
                            gn_found=True
                            gn_res=exception.split(",")[2:4]
                            for i in range(len(gn_res)):
                                if gn_res[i]=='':
                                    gn_res[i]='NULL'
                            gender,sg_pl = gn_res
                            break

                    if gn_found==False:    
                        if t in gn.keys():
                            gn_res = gn[t]
                            gender,sg_pl = gn_res.split(",")
                            #print(f"Gender : {gender} , sg_pl : {sg_pl} , t : {t}")
                        else:
                            gender,sg_pl = find_gn(cat,rs,gender,sg_pl)
                            #print(f"Here for the root : {root}")
                            #print(f"Gender : {gender} , sg_pl : {sg_pl}")
                        if ((pos!='V__VM__VF' and pos!='V_VM_VF') and (pos!='V__VAUX' and pos!='V_VAUX')) and cat=='v':
                            #print(f"Here for the root : {root}")
                            gender='NULL'
                            sg_pl='NULL'

                        if (pos=='V__VM__VF' or pos=='V_VM_VF'):
                            vf_flag = 1

                        if (next_pos == 'V__VAUX' or next_pos == 'V_VAUX'):
                            #print(f"Here for the root : {root}")
                            gender = 'NULL'
                            sg_pl = 'NULL'

                        if (pos == 'V__VAUX' or pos == 'V_VAUX') and (next_pos != 'V__VAUX' and next_pos != 'V_VAUX'):
                            if vf_flag != 1:
                                #print(f"Here for the root : {root}")
                                gender = 'NULL'
                                sg_pl = 'NULL'

                        if (next_pos != 'V__VAUX' and next_pos != 'V_VAUX'):
                            vf_flag = 0


            cats_same_roots = ['avy','psp']
            if cat in cats_same_roots:
                root = word
                suff = 0
            if pos=='DM__DMD' or pos=='DM_DMD':
                #root = word
                #suff = 0
                sg_pl = 'sg'

            to_check_ending = {'a':'ಅ','u':'ಉ'}   
            ambiguous_suffs = {'ne_num':'ನೇ'}
            vibhakti_cats = ['n','pn','nst','num']
            word_wx = utf2wx.convert(word)
            root_wx = utf2wx.convert(root)
            ind = match(word_wx,root_wx)
            to_match = word_wx[ind:]
            if to_match in morpheme_dict.keys():
                suff = morpheme_dict[to_match]
                #print(f"to_match : {to_match} , Suff : {suff}")
            elif word_wx != root_wx:
                #print(find_morpheme_string(word_wx,root_wx,cat,[]))
                suff,l = find_morpheme_string(word_wx,root_wx,cat,[])
                #print(f"Suff : {suff} , l : {l}")
            else:
                suff = 0

                    
            if suff=="NULL":
                suff = 0
            if word[0].isdigit()==True and cat=='n':
                gender = 'NULL'
                sg_pl = 'NUM'

            if ((pos=='N_NNV' or pos=='N__NNV') or cat=='pn') and to_match=='vu':
                suff = "ವು+ಉ"
            elif root in exception_roots and to_match=='vu':
                suff = "ವು+ಉ"
            if cat=='pn' and to_match=='xu':
                suff = "ದ+ಉ"

            if (pos=='V__VM__VNG' or pos=='V_VM_VNG'):
                vng_flag = 1

            if (pos=='V__VAUX' or pos=='V_VAUX') and vng_flag==0:
                if str(suff).endswith("+ಅ"):
                    suff = suff.replace("+ಅ",'')
            
            if (pos=='V__VAUX' or pos=='V_VAUX') and vng_flag==1:
                for x,y in to_check_ending.items():

                    if word_wx.endswith(x) and (not str(suff).endswith((f"+ಅ",f"ಇಂದ"))):
                        if suff==0:
                            suff = y
                        else:
                            suff+=f"+{y}"

            
            if (pos=='V__VM__VNG' or pos=='V_VM_VNG'):
                
                for x,y in to_check_ending.items():

                    if word_wx.endswith(x) and (not str(suff).endswith("+ಅನ್ನು")) and not(wx_word.endswith("iMxa")):

                        if suff==0:
                            suff=y
                        else:
                            if (not suff.endswith("+ಅ")):
                                suff+=f"+{y}"




            #print(f"VNG Flag : {vng_flag}")
            nnv_adds = ["ಮೆ"]
            


            if cat in vibhakti_cats or pos=="QT__QTF" or pos=='QT_QTF':
                if word_wx.endswith('u'):
                    if suff==0:
                        suff='ಉ'
                    elif (not str(suff).endswith("+ಉ")) and (not str(suff).endswith("ಅನ್ನು")):
                        #print(f"Here for the word {word_wx}")
                        suff+='+ಉ'

            for x,y in ambiguous_suffs.items():
                a,b = x.split("_")
                if to_match==a and cat==b:
                    suff=y

            #print(f"Root : {root}")
            if root[0].isdigit()==True and "ಅರು" in str(suff):
                suff = suff.replace("ಅರು","ರ")

            if root_wx.endswith('isu') and to_match=='wa':
                suff='ಇತ'

            if pos.endswith("NNV") or cat=='adj':
                for i in nnv_adds:
                    if root.endswith(i):
                        root = root[:-2]
                        if suff==0:
                            suff=i
                        else:
                            suff = f"{i}+" + suff

            if pos.endswith("VF") and to_match=='varu':
                suff = "ವ+ಅರು"


            if root_wx.endswith("ika"):
                r,suff = handle_ika(root_wx,suff)
                root = wx2utf.convert(r)

            if (utf2wx.convert(root)).endswith('kAlika'):
                r = root_wx.replace("kAlika","kAla")
                root = wx2utf.convert(r)
                if suff==0:
                    suff = "ಇಕ"
                else:
                    suff = "ಇಕ+"+suff

            if root_wx.endswith("Awmaka"):
                r,suff = handle_Awmaka(root_wx,suff)
                root = wx2utf.convert(r)

            if root_wx.endswith("aweV"):
                #print(f"Root wx : {root_wx}")
                r,suff = handle_aweV(root_wx,suff)
                root = wx2utf.convert(r)

            root_wx = utf2wx.convert(root)  

            nnv_handle = {'iwa':['isu','ಇತ'],'vaNeV':['yisu','ವ+ಅಣೆ'],'aneV':['u','ಅನೆ'],'aNeV':['isu','ಅಣೆ'],'aNa':['isu','ಅಣ'],'ada':['u','ಅಡ'],'aka':['isu','ಅಕ']}
            adj_handle = {'iwa':['isu','ಇತ'],'vaNeV':['yisu','ವ+ಅಣೆ'],'aNeV':['isu','ಅಣೆ'],'aNa':['isu','ಅಣ'],'ada':['u','ಅಡ'],'aka':['isu','ಅಕ']}
            only_suffs = {'wana':'ತನ','weV':'ತೆ','kAra':'ಕಾರ','kAri':'ಕಾರಿ'}

            for a,b in nnv_handle.items():
                if root_wx.endswith(a) and (pos=="N_NNV" or pos=="N__NNV") and (root_wx not in exception_words):
                    if a=='iwa':
                        r = root_wx.replace("iwa","i")
                        if search_in_dict(r):
                            root_wx = r
                        else:
                            root_wx = root_wx.replace(a,b[0])
                    else:
                        root_wx = root_wx.replace(a,b[0])
                    root = wx2utf.convert(root_wx)
                    if suff==0:
                        suff=b[1]
                    else:
                        suff = f"{b[1]}+"+suff

            for a,b in adj_handle.items():
                if root_wx.endswith(a) and (pos=="JJ") and (root_wx not in exception_words):
                    if a=='iwa':
                        r = root_wx.replace("iwa","i")
                        if search_in_dict(r):
                            root_wx = r
                        else:
                            root_wx = root_wx.replace(a,b[0])
                    else:
                        root_wx = root_wx.replace(a,b[0])
                    root = wx2utf.convert(root_wx)
                    if suff==0:
                        suff=b[1]
                    else:
                        suff = f"{b[1]}+"+suff


            
        
            for a,b in only_suffs.items():
                if root_wx.endswith(a) and (search_in_dict(root_wx) == False):
                    r = root_wx[:-len(a)]
                    if search_in_dict(r):
                        if suff==0:
                            suff=b
                        else:
                            suff=f"{b}+"+suff
                        root = wx2utf.convert(r)
            

            if pos=='N__NNV' or pos=='N_NNV' or pos=='JJ':
                if root_wx.endswith("keV"):
                    r = root_wx[:-3]
                    if suff==0:
                        if r.endswith("i"):
                            s = "ಇಕೆ"
                        else:
                            s = "ಕೆ"
                    else:
                        if r.endswith("i"):
                            s = "ಇಕೆ+"+suff
                        else:
                            s = "ಕೆ+"+suff
                    if search_in_dict(r):
                        root = wx2utf.convert(r)
                        suff = s
                    else:
                        #r = r[:-1]+"a"
                        if search_in_dict(r):
                            root = wx2utf.convert(r)
                            suff = s
                        else:
                            r = r+"su"
                            if search_in_dict(r):
                                root = wx2utf.convert(r)
                                suff = s
                            else:
                                pass

            suff_replace = {'ಅಂ+ತ+ಎ':'ಅಂತೆ',"ಇ+ಕೆ":"ಇಕೆ",'ಇ+ದ':'ಇದ','ವ+ಅರ':'ಅವರು','ವಳಿ+ಕೆ':'ವಳಿಕೆ','ವ+ವ+ಅನು':'ವ+ಅವನು'}
            for a,b in suff_replace.items():
                if a.endswith(str(suff)) or (f"{a}+" in str(suff)):
                    suff = suff.replace(a,b)


            if str(suff).endswith("ತ+ಅ") and "iwa" in word_wx:
                suff = suff.replace("ತ+ಅ","ಇತ")
            elif str(suff).startswith("ತ+") and "iwa" in word_wx:
                suff = suff.replace("ತ+","ಇತ+")

            if to_match=='xeV' and root_wx=='illa':
                suff = "ಅದೆ"

            if cat=='v' and sg_pl=='sg':
                if gender=='any':
                    gender='NULL'

            if (pos=='N__NNP' or pos=='N_NNP') and word[0].isdigit():
                #print(f"Here for the word {word}")
                root = word
                suff = 0

            if pos=='JJ':
                if str(suff).endswith("+ಅ") or str(suff).endswith("+ಉ"):
                    suff = suff[:-2]

            #New code should be above this

            if "ಇಕೆ" in str(suff):
                gender="NULL"



            if suff == 0:
                d_o = 'd'
            else:
                d_o = 'o'



            if cat=='v' and (pos != 'V__VM__VNG' and pos != 'V_VM_VNG') and vng_flag==0:
                d_o = "NULL"

            if (next_pos != 'V__VAUX' and next_pos != 'V_VAUX'):
                            vng_flag = 0

            if (cat=='n' or cat=='pn') and (not root[0].isdigit()):
                person = '3'
                
            f.write(f"{root}\t{suff}\t{gender}\t{sg_pl}\t{person}\t{d_o}\t{word}\t{try_flag}\t{pos},{cat_found}\t{l}\n")
        
