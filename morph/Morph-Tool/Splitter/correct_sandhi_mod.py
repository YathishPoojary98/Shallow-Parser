#Author Akshatha Arodi 
#dtd 10/03/2015 as a part of my major project kannada spell checker with sandhi splitter 
#found_print[0] 0 if sandhi not found 1 if found
#found_print[1] gives what to be printed if sandhi is found
#found_print[1] has suggestions otherwise ( if in spell_ something
#initialised
#lookaika bug fixed
import itertools
#import init_sandhi_mod
from Splitter.init_sandhi_mod import *
#import word_roman_mod
from Splitter.word_roman_mod import *
#import spell_check_mod1
from Splitter.spell_check_mod1 import *
import sys
from Splitter.charsreplace import *
from Splitter.replaceback import *
from wxconv import WXC
global selected
global dict_dawg
global rev_dict_dawg
global prnt_res

#I need to return a flag saying if the thing is found or not, also if found what to print. 
#So, I am using an array called found_print
con = WXC(order="wx2utf",lang="kan")
vyanjana_prefixes = ['dur','nir','an']
def init_dawg():
	dictWords = []
	global dict_dawg
	global rev_dawg
	f = open("Splitter/Dictionaries/wx_dictionary2.txt", "r")
	for line1 in f:
		dictWords.append(line1.strip())
		
#read the store the reverse dictionary
	rev_f=open("Splitter/Dictionaries/reverse_wx_dictionary2.txt","r")
	for line in rev_f:
		rev_dictWords.append(line.strip())
				
#creating the reverse dawg
	rev_dict_dawg = rev_dictWords.copy()
	dict_dawg = dictWords.copy()
	#rev_dict_dawg=dawg.CompletionDAWG(rev_dictWords)
	#dict_dawg=dawg.CompletionDAWG(dictWords)
	
	
#spell checker with sandhi splitter module
def spell_sandhi_checker(given_word,prnt_res):
	global found_print
	found_print=[]
	found_print.append(0)
	found_print.append("")
	found_print.append("")
	found_print.append("")
	called_sandhi_maker=0
	i=2
	init_dawg()
	found=0
	found_print[0]=found
	given_word_len=len(given_word)
	global selected
	selected=''
	global spell_done
	spell_done=0
	while i<given_word_len:
		check_word=given_word[:i]
	
		#need to make lopa leave the word for a few combinations		
		#lopa_exclude=given_word[i]
	
		last=check_word[-1]
	
		#exclude this in lopa sandhi : skip the check
		#lopa_leave=last+lopa_exclude
	
		lastbone=check_word[-2]
		guessed_sandhi_place=lastbone+last
		#guessed_sandhi_place=check_word[-3:-1]
		if guessed_sandhi_place in sandhi_places:
			guessed_prefix=check_word[:-2]
			guessed_suffix=given_word[i:]
			
			#call a function to check the sandhi
			found_print=check_sandhi(guessed_prefix,guessed_suffix,guessed_sandhi_place,1,prnt_res,given_word)
		i=i+1
	i=2
	while i<given_word_len:
		check_word=given_word[:i]		
		last=check_word[-1]
		if found_print[0]==0 and last in kannada_sandhi_places:
			kannada_prefix=check_word[:-1]
			guessed_suffix=given_word[i:]
			found_print=spell_check_kannada_sandhi(kannada_prefix,guessed_suffix,last,prnt_res)
				
		i=i+1
	
	#checking and generation lopa sandhi places
	#This is generating a lot of unwanted suggestions
	#i=1
	#while i<given_word_len and found_print[0]!=1:
	#	lopa_len=given_word_len-i
	#	lopa_suffix=given_word[lopa_len:given_word_len]
	#	lopa_prefix=given_word[:lopa_len]
	#	found_print=spell_check_lopa_sandhi(lopa_prefix,lopa_suffix,prnt_res)
	#	i=i+1
	print("this is what sepll sandhi checker is returning")
	print(found_print[1])
	return found_print[1]
#removed stuff from here
	
#checking for valid sandhi with spell checker
def spell_valid_sandhi(guessed_prefix,guessed_suffix,sandhi_name,prefix_last,suffix_first1,suffix_first2,sandhi_place,prnt_res):
	found=0
	#found_print=[]
	#found_print.append(0)
	#found_print.append("")
	prefix=guessed_prefix+prefix_last
	sandhi=sandhi_name
	prefix_suggests=[]
	suffix_suggests=[]
	
	if prefix in dict_dawg:
		print("prefix in dict dawg")
	#prefix is already found in the word. So guess only sufffix
		prefix_suggests.append(guessed_prefix)
		suffix=suffix_first1+guessed_suffix
		
		#guess all the words which begin with the first suffix word
		suffix1_suggests=spell_check(suffix,'f',suffix_first1)
		print("before chop")
		print(suffix1_suggests)
		suffix_first1_len=len(suffix_first1)
		for word in suffix1_suggests:
			suffix_suggests.append(word[suffix_first1_len:])
		print("first time suffix suggests")
		print(suffix_suggests)
			
		suffix=suffix_first2+guessed_suffix
		suffix2_suggests=spell_check(suffix,'f',suffix_first2)
		suffix_first2_len=len(suffix_first2)
		for word in suffix2_suggests:
			suffix_suggests.append(word[suffix_first2_len:])
		print("secnd time suffix suggests")
		print(suffix_suggests)
		suffix_suggests=list(set(suffix_suggests))
		print("suf suggest")
		print(suffix_suggests)
		if len(suffix_suggests) > 0:
			found=1

	if suffix_first1+guessed_suffix in dict_dawg or suffix_first2+guessed_suffix in dict_dawg:		
		prefix_suggests1=spell_check(prefix[::-1],'r',prefix_last)
		suffix_suggests.append(guessed_suffix)
		print("suffix found")
		for word in prefix_suggests1:
			w=word[::-1]
			prefix_suggests.append(w[:-1])
		if len(prefix_suggests)>0:
			found=1
	print("saw for suf")	
	if found==1:
		print("insude founf=1")
		found_print[0]=found
		found_print[1]=spell_print_result(prefix_suggests,suffix_suggests,sandhi,sandhi_place,prnt_res)
	#found_print[0]=found
	print("printing found_print11")
	print(found_print)
	return found_print

#the combintions of all prefix and suffixes and sandhis to be printed

def spell_print_result(prefix_suggests,suffix_suggests,sandhi,sandhi_place,prnt_res):
	global selected
	given_suggests=[]
	for prefix in prefix_suggests:
		for suffix in suffix_suggests:
			word=prefix+sandhi_place+suffix
			given_suggests.append(word)
			
	ordered_suggests=order_suggests(given_suggests)
	return select_suggest(ordered_suggests,prnt_res)
	#print_suggestions(prnt_res)

#checking kannada sandhi will spell checker
def spell_check_kannada_sandhi(prefix,guessed_suffix,last,prnt_res):
	found=0
	found_print=[]
	found_print.append(0)
	found_print.append("")
	prefix_suggests=[]
	suffix_suggests=[]
	if last=='g':
		suffix='k'+guessed_suffix
		sandhi="AxeSa"
	elif last=='d':
		suffix='t'+guessed_suffix
		sandhi="AxeSa"
	elif last=='b':
		suffix='p'+guessed_suffix
		sandhi="AxeSa"
	elif last=='y':
		suffix=guessed_suffix
		sandhi="Agama"
	elif last=='v':
		suffix=guessed_suffix
		sandhi="Agama"
	if prefix in dict_dawg:
		prefix_suggests.append(prefix)			
		suffix_suggests1=spell_check(suffix,'f',suffix[0])
		for w in suffix_suggests1:
			word=w[1:]
			suffix_suggests.append(word)
		if len(suffix_suggests)>0:
			found=1
			
	elif suffix in dict_dawg:
		suffix_suggests.append(guessed_suffix)
		prefix_suggests=spell_check(prefix,'f','')
		if len(prefix_suggests)>0:
			found=1
	if found==1:
		found_print[1]=spell_print_result(prefix_suggests,suffix_suggests,sandhi,last,prnt_res)
	found_print[0]=found
	return found_print


#checking lopa sandhi with spelling 
def spell_check_lopa_sandhi(lopa_prefix,lopa_suffix,prnt_res):
	found=0
	found_print=[]
	found_print.append(0)
	found_print.append("")
	suffix_begin=lopa_suffix[0]
	possible_prefix=[]
	suffix_suggests=[]
	prefix_suggests=[]
	if lopa_suffix in dict_dawg:
		suffix_suggests.append(lopa_suffix)
		for vowel in lopa_places:
			prefix=lopa_prefix+vowel
			prefix_suggests+=spell_check(prefix,'f','')
	else:
		for vowel in lopa_places:
			prefix=lopa_prefix+vowel
			if prefix in dict_dawg:
				prefix_suggests.append(prefix)
				suffix_suggests+=spell_check(lopa_suffix,'f','')
	if len(prefix_suggests)>0 or len(suffix_suggests)>0:
		found=1
		
	

	if found==1:
		prefix1_suggests=[]
		for w in prefix_suggests:
			prefix1_suggests.append(w[:-1])
		found_print[1]=spell_print_result(prefix1_suggests,suffix_suggests,'lopa','',prnt_res)	
	found_print[0]=found
	return found_print

#main sandhi splitter module that tells if the word is split properly
#takes the word as input and a bool prnt_res  such as prnt : 0 no printing result prnt :1 prints result
def sandhi_splitter(given_word,prnt_res):
	#print("Splitter called")
	#print("Sandhi Splitter Called")
	given_word = char_replace(given_word)
	
	#print(f"Given word : {given_word}")
	found_print=[]
	found_print.append(0)
	found_print.append("")
	for prefix in vyanjana_prefixes:
		if given_word.startswith(prefix) and given_word[len(prefix):] in dictWords:
			return found_print
	given_word_len=len(given_word)
	
	i=2
	found=0
	found_print[0]=found
	check_word=''
	#refresh dawg after adding the words
	init_dawg()
	#this to show the word is swept for suggestions
	global done
	done=0
	while found_print[0]==0 and i<given_word_len:
		
		check_word=given_word[:i]
		
		#need to make lopa leave the word for a few combinations		
		#lopa_exclude=given_word[i]
		
		last=check_word[-1]
		
		#exclude this in lopa sandhi : skip the check
		#lopa_leave=last+lopa_exclude
		
	
		lastbone=check_word[-2]
		guessed_sandhi_place=lastbone+last
		#print(f"Guessed sandhi place : {guessed_sandhi_place}")
		
		#print(f"Sandhi places : {sandhi_places}")
		
		if guessed_sandhi_place in sandhi_places:
			guessed_prefix=check_word[:-2]
			guessed_suffix=given_word[i:]
			
			#call a function to check the sandhi
			#print(f"check sandhi called -> {guessed_sandhi_place}")
			found_print=check_sandhi(guessed_prefix,guessed_suffix,guessed_sandhi_place,0,prnt_res,given_word)
			#print("check_sandhi called")
		
		if found_print[0]!=1 and last in kannada_sandhi_places:
			kannada_prefix=check_word[:-1]
			guessed_suffix=given_word[i:]
			found_print=check_kannada_sandhi(kannada_prefix,guessed_suffix,last,prnt_res)
		i=i+1
		
		#checking lopa sandhi
	i=1
	while i<given_word_len and found_print[0]!=1:
		lopa_len=given_word_len-i
		lopa_suffix=given_word[lopa_len:given_word_len]
		lopa_prefix=given_word[:lopa_len]
		found_print=check_lopa_sandhi(lopa_prefix,lopa_suffix,prnt_res)
		i=i+1
	done=1
	#print(f"found_print = {found_print}")
	return found_print
	
#function to check the sandhi
#spell=0 indicates spell checker mode is off

def check_sandhi(guessed_prefix,guessed_suffix,guessed_sandhi_place,spell,prnt_res,given_word):
	#first see if the word itself has the splits	
	#see the possible cases
	found=0
	#print("Guessed Sandhi Place")
	#print(guessed_sandhi_place)
	
	# savarNaxIrGa aa= a+a/aa
	if guessed_sandhi_place=='aa':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"savarNaxIrGa",'a','a','aa',prnt_res)
			if found_print[0]==1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"savarNaxIrGa",'aa','a','aa',prnt_res)
			if found_print[0]==1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"lopa",'u','aa','a',prnt_res)
		else:
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"savarNaxIrGa",'a','a','aa','aa',prnt_res)
			if found_print[0]==1:
				return found_print
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"lopa",'u','a','aa','aa',prnt_res)
	# savarNaxIrGa ii= i+i/ii
	elif guessed_sandhi_place=='ii':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"savarNaxIrGa",'i','i','ii',prnt_res)
		else:
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"savarNaxIrGa",'i','i','ii','ii',prnt_res)
	
	# savarNaxIrGa uu= u+u/uu
	elif guessed_sandhi_place=='uu':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"savarNaxIrGa",'u','uu','u',prnt_res)
		else:
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"savarNaxIrGa",'u','u','uu','uu',prnt_res)	
	
	# savarNaxIrGa RR= R+R/RR
	elif guessed_sandhi_place=='RR':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"savarNaxIrGa",'R','R','RR',prnt_res)
		else:
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"savarNaxIrGa",'R','R','RR','RR',prnt_res)
		
	# guna sandhi oo=a+u/uu
	elif guessed_sandhi_place=='oo':

		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"guNa",'aa','u','uu',prnt_res)
			if found_print[0] == 1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"visarga",'aH','','a',prnt_res)
			if found_print[0] == 1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"visarga",'as','',' g',prnt_res)
			if found_print[0] == 1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"guNa",'a','u','uu',prnt_res)
			
			
		else:
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"guNa",'aa','u','uu','oo',prnt_res)	
			if found_print[0] == 1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"visarga",'as','',' g','oo',prnt_res)
			if found_print[0] == 1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"guNa",'a','u','uu','oo',prnt_res)
			
	# guna sandhi ee=a+i/ii
	elif guessed_sandhi_place=='ee':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"guNa",'aa','i','ii',prnt_res)
			if found_print[0] == 1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"guNa",'a','i','ii',prnt_res)
			
		else:
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"guNa",'a','i','ii','ee',prnt_res)
			if found_print[0] == 1:
				return found_print
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"guNa",'aa','i','ii','ee',prnt_res)
					
	# guna sandhi aR=a+R/RR
	elif guessed_sandhi_place=='aR':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"guNa",'a','R','RR',prnt_res)
		else:
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"guNa",'a','R','RR','aR',prnt_res)	
			
	# vqxXi sandhi a+ee/ai = ai
	elif guessed_sandhi_place=='ai':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"vqxXi",'aa','ee','ai',prnt_res)
			if found_print[0]==1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"vqxXi",'a','ee','ai',prnt_res)
		else:
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"vqxXi",'a','ee','ai','ai',prnt_res)
			#print("in vrudhi")
			#print("pre",guessed_prefix)
			#print("suf",guessed_suffix)	
				
	# vqxXi sandhi a+oo/au = au
	elif guessed_sandhi_place=='au':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"vqxXi",'aa','o','au',prnt_res)
			if found_print[0]==1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"vqxXi",'a','oo','o',prnt_res)
			if found_print[0]==1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"vqxXi",'aa','oo','o',prnt_res)
		else:
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"vqxXi",'a','o','au','au',prnt_res)
			if found_print[0]==1:
				return found_print
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"vqxXi",'a','oo','o','au',prnt_res)
			if found_print[0]==1:
				return found_print
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"vqxXi",'aa','oo','o','au',prnt_res)
		
	
	# yan ya=i+a/aa
	elif guessed_sandhi_place=='ya':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'i','a','aa',prnt_res)
			if found_print[0]==1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"Agama",'','a','aa',prnt_res)
		else:
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'i','a','aa','ya',prnt_res)
	
	# yan yu=i+u/uu
	elif guessed_sandhi_place=='yu':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'i','u','uu',prnt_res)
		else:
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'i','u','uu','yu',prnt_res)
	
	# yan yo=i+o/oo
	elif guessed_sandhi_place=='yo':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'i','o','oo',prnt_res)
		else:
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'i','o','oo','yo',prnt_res)
	
	# yan ye=i+e/ee
	elif guessed_sandhi_place=='ye':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'i','e','ee',prnt_res)
		else:
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'i','e','ee','ye',prnt_res)
		
	# yan va=v+a/aa
	elif guessed_sandhi_place=='va':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'u','a','aa',prnt_res)

		else:
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'u','a','aa','va',prnt_res)
	
	# yan vu=u+i/ii
	elif guessed_sandhi_place=='vu':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'u','i','ii',prnt_res)
		else:
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'u','i','ii','vu',prnt_res)
	
	# yan vo=u+o/oo
	elif guessed_sandhi_place=='vo':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'u','o','oo',prnt_res)
		else:
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'u','o','oo','vo',prnt_res)
	
	# yan ve=u+e/ee
	elif guessed_sandhi_place=='ve':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'u','e','ee',prnt_res)
			if found_print[0]==1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"lopa",'vu','e','el',prnt_res)
			if found_print[0]==1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'','be','',prnt_res)
		else:
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'u','e','ee','ve',prnt_res)
			if found_print[0] == 1:
				return found_print
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"lopa",'vu','e','el','ve',prnt_res)
			
	elif guessed_sandhi_place=='gi':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'k','i','ii',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'k','i','ii','gi',prnt_res)
	elif guessed_sandhi_place=='Dr':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'T','r','ra',prnt_res)
			if found_print[0] == 1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'T','r','ru',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'T','r','ra','Dr',prnt_res)
			if found_print[0] == 1:
				return found_print
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'T','r','ru','Dr',prnt_res)
			
	elif guessed_sandhi_place=='dr':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'t','r','',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'t','r','','dr',prnt_res)
			
			
	elif guessed_sandhi_place=='hc':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"Scuwva",'','c','ca',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"Scuwva",'','c','ca','hc',prnt_res)
			
	elif guessed_sandhi_place=='jj':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"Scuwva",'t','j','jy',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"Scuwva",'t','j','jy','jj',prnt_res)
			
	elif guessed_sandhi_place=='kR':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"Scuwva",'t','Ca','',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"Scuwva",'t','Ca','','kR',prnt_res)
			
			
	elif guessed_sandhi_place=='cc':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"Scuwva",'t','c','ci',prnt_res)
			if found_print[0]==1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"Cawva",'t','s','sh',prnt_res)
		else:
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"Scuwva",'t','c','ci','cc',prnt_res)
			if found_print[0]==1:
				return found_print
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"Cawva",'t','s','sh','cc',prnt_res)
			
	elif guessed_sandhi_place=='cC':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"Cawva",'t','s','sh',prnt_res)
			if found_print[0]==1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"Cawva",'c','sh','',prnt_res)
			if found_print[0]==1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"Cawva",'t','c','',prnt_res)
			if found_print[0]==1:
				return found_print
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"Cawva",'t','s','sh','cC',prnt_res)
			if found_print[0]==1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"Cawva",'c','sh','','cC',prnt_res)
			if found_print[0]==1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"Cawva",'t','c','','cC',prnt_res)
		
			
	elif guessed_sandhi_place=='sh':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"Scuwva",'s','','sh',prnt_res)
			
	elif guessed_sandhi_place=='Sh':
		if spell==0:
			#print(f"Guessed prefix : {guessed_prefix}")
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"Rtuwva",'s','T','Sh',prnt_res)
			if found_print[0]==1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"Rtuwva",'s','','',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"Rtuwva",'s','T','Sh','Sh',prnt_res)
			
	elif guessed_sandhi_place=='DD':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"Rtuwva",'t','D',' Da',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"Rtuwva",'t','D','Da','DD',prnt_res)
	elif guessed_sandhi_place=='TT':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"Rtuwva",'t','T','',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"Rtuwva",'t','T','','TT',prnt_res)	
				
	elif guessed_sandhi_place=='Nm':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"anunAsika",'T','m','mu',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"anunAsika",'T','m','mu','Nm',prnt_res)
	elif guessed_sandhi_place=='nn':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"anunAsika",'t','n','na',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"anunAsika",'t','n','na','nn',prnt_res)
			
	elif guessed_sandhi_place=='nG':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"anunAsika",'k','',' m',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"anunAsika",'k','',' m','nG',prnt_res)
			
	elif guessed_sandhi_place=='nm':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"anunAsika",'t','m','ma',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"anunAsika",'t','m','ma','nm',prnt_res)
			
	elif guessed_sandhi_place=='Hk':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"visarga",'r','k','ka',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"visarga",'r','k','ka','Hk',prnt_res)
			
	elif guessed_sandhi_place=='ir':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"visarga",'iH','','',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"visarga",'iH','','','ir',prnt_res)
			
	elif guessed_sandhi_place=='ur':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"visarga",'uH','','',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"visarga",'uH','','','ur',prnt_res)
			
	elif guessed_sandhi_place=='Hr':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"visarga",'r','r','ra',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"visarga",'r','r','ra','Hr',prnt_res)
			
	elif guessed_sandhi_place=='Hp':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"visarga",'r','p','pa',prnt_res)
			if found_print[0] == 1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"visarga",'s','p','ph',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"visarga",'r','p','pa','Hp',prnt_res)
			if found_print[0] == 1:
				return found_print
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"visarga",'s','p','ph','Hp',prnt_res)
			
	elif guessed_sandhi_place=='ga':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"lopa",'ge','a','al',prnt_res)
			if found_print[0] == 1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'k','a','aM',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"lopa",'ge','a','al','ga',prnt_res)
			if found_print[0] == 1:
				return found_print
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'k','a','aM','ga',prnt_res)
			
	elif guessed_sandhi_place=='ne':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"lopa",'nu','e','eM',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"lopa",'nu','e','eM','ne',prnt_res)
			
	elif guessed_sandhi_place=='iy':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"Agama",'i','',' a',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"Agama",'i','',' a','iy',prnt_res)
					
	elif guessed_sandhi_place=='av':
		if spell==0:
			found_print=check_kannada_sandhi(guessed_prefix+'a',guessed_suffix,'v',prnt_res)
			if found_print[0] == 1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'a','p','b',prnt_res)
			if found_print[0]==1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'a','b','ba',prnt_res)
		
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'a','p','pe','av',prnt_res)
			if found_print[0]==1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'a','b','ba','av',prnt_res)
			
			
	elif guessed_sandhi_place=='ev':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'e','p','b',prnt_res)
			if found_print[0]==1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'e','b','m',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'e','p','b','ev',prnt_res)
			if found_print[0]==1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'e','b','m','ev',prnt_res)
			
			
	elif guessed_sandhi_place=='Mc':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'n','s','sa',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'n','s','sa','Mc',prnt_res)
			
	elif guessed_sandhi_place=='Ca':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'','s','sa',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'','s','sa','Ca',prnt_res)
			
			
	elif guessed_sandhi_place=='Nc':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'N','s','sa',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'N','s','sa','Nc',prnt_res)
	elif guessed_sandhi_place=='ls':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'l','s','sa',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'l','s','sa','ls',prnt_res)
	elif guessed_sandhi_place=='lv':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'l','m','b',prnt_res)
			if found_print[0] == 1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'lku','m','',prnt_res)
			if found_print[0] == 1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'l','p','',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'l','m','b','lv',prnt_res)
			if found_print[0] == 1:
				return found_print
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'lku','m','','lv',prnt_res)
			if found_print[0] == 1:
				return found_print
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'l','p','','lv',prnt_res)
			
	elif guessed_sandhi_place=='Mj':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'n','s','',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'n','s','','Mj',prnt_res)
			
	elif guessed_sandhi_place=='Nj':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'N','s','',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'N','s','','Nj',prnt_res)
			
	elif guessed_sandhi_place=='iv':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'i','p','m',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'i','p','m','iv',prnt_res)
			
	elif guessed_sandhi_place=='ys':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'y','s','sa',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'y','s','sa','ys',prnt_res)
			
	elif guessed_sandhi_place=='Da':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'T','a','aa',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'T','a','aa','Da',prnt_res)
			
	elif guessed_sandhi_place=='da':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'t','a','aa',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'t','a','aa','da',prnt_res)
	elif guessed_sandhi_place=='dy':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'t','y','ya',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'t','y','ya','dy',prnt_res)
			
	elif guessed_sandhi_place=='kc':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'k','c','ca',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'k','c','ca','kc',prnt_res)
			
	elif guessed_sandhi_place=='kt':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'k','t','ta',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'k','t','ta','kw',prnt_res)
			
	elif guessed_sandhi_place=='bd':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'p','d','dh',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'p','d','dh','bd',prnt_res)
			
	elif guessed_sandhi_place=='gd':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'k','d','de',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'k','d','de','gd',prnt_res)
			
	elif guessed_sandhi_place=='ja':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'c','a','aM',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'c','a','aM','ja',prnt_res)
			
	elif guessed_sandhi_place=='du':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'t','u','ud',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'t','u','ud','du',prnt_res)
			
	elif guessed_sandhi_place=='db':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'t','b','bh',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'t','b','bh','db',prnt_res)
			
	elif guessed_sandhi_place=='bj':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'p','j','ja',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'p','j','ja','bj',prnt_res)
			
	elif guessed_sandhi_place=='ba':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'p','a','aM',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'p','a','aM','ba',prnt_res)
	elif guessed_sandhi_place=='gv':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'k','v','',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'k','v','','gv',prnt_res)
			
	elif guessed_sandhi_place=='tk':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'t','k','ka',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'t','k','ka','tk',prnt_res)
			
	elif guessed_sandhi_place=='ks':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'k','s','su',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'k','s','su','ks',prnt_res)
	elif guessed_sandhi_place=='kp':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'k','p','pa',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'k','p','pa','kp',prnt_res)
			
	elif guessed_sandhi_place=='aj':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"Scuwva",'at','j','jy',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"Scuwva",'at','j','jy','aj',prnt_res)
			
	elif guessed_sandhi_place=='mm':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"anunAsika",'p','m','ma',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"anunAsika",'p','m','ma','mm',prnt_res)
			
	elif guessed_sandhi_place=='Tm':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"anunAsika",'T','m','',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"anunAsika",'T','m','','Tm',prnt_res)
			
	elif guessed_sandhi_place=='dg':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'t','g','gu',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"jaSwva",'t','g','gu','dg',prnt_res)
	elif guessed_sandhi_place=='Rr':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'R','a','ar',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'R','a','ar','Rr',prnt_res)
	elif guessed_sandhi_place=='hv':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'hu','','a',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'hu','','a','hv',prnt_res)
	elif guessed_sandhi_place=='rv':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"AxeSa",'r','p','b',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"Axesa",'r','p','b','rv',prnt_res)
	elif guessed_sandhi_place=='nu':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"lopa",'na','u','uu',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"lopa",'na','u','uu','nu',prnt_res)
	elif guessed_sandhi_place=='ll':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"lakAra xviwva",'t','l','',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"lakAra xviwva",'t','l','','ll',prnt_res)
			
	elif guessed_sandhi_place=='ar':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"guNa",'aa','q','qR',prnt_res)
			if found_print[0] == 1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"guNa",'a','q','qR',prnt_res)
			if found_print[0] == 1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"visarga",'r','r','ra',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"guNa",'aa','q','qR','ar',prnt_res)
			if found_print[0] == 1:
				return found_print
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"guNa",'a','q','qR','ar',prnt_res)
			
	elif guessed_sandhi_place=='ra':
		if spell==0:
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'q','a','aa',prnt_res)
			if found_print[0] == 1:
				return found_print
			found_print=valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'q','','aM',prnt_res)
		else:
			
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'q','a','aa','ra',prnt_res)
			if found_print[0] == 1:
				return found_print
			found_print=spell_valid_sandhi(guessed_prefix,guessed_suffix,"yaN",'q','','aM','ra',prnt_res)
			

	
	return found_print

#putting the sandhi finding process in one function
def valid_sandhi(guessed_prefix,guessed_suffix,sandhi_name,prefix_last,suffix_first1,suffix_first2, prnt_res):
	found=0
	prefix=guessed_prefix+prefix_last
	prefix = replaceback(prefix)
	#print(f"Prefix : {prefix}")
	sandhi=sandhi_name
	#print(f"Sandhi name : {sandhi_name}")
	found_print=[]
	found_print.append(0)
	found_print.append("")
	if prefix in dict_dawg:
	#see ex a=a+a
		suffix=suffix_first1+guessed_suffix
		suffix = replaceback(suffix)
		#print(f"Suffix 1 : {suffix_first1}")
		#print(f"Suffix : {suffix}")
		if suffix in dict_dawg:		
				found=1
		else:
			suffix=suffix_first2+guessed_suffix
			#print(f"suffix_first2 : {suffix_first2}, guessed_suffix : {guessed_suffix}")
			suffix = replaceback(suffix)
			#print(f"Suffix 2 : {suffix_first2}")
			#print(f"Suffix :{suffix}")
			
			if suffix in dict_dawg:		
				found=1
			else:
				found=0
	if found==1 and prnt_res==1:
		#make found and 
		found_print[0]=found
		found_print[1]=print_result(prefix,suffix,sandhi)
	#customised for spell checker
	
	
	
	
	#need to fix this
	elif found==1 and prnt_res==2:
		found_print[0]=found
		to_print="\n"+sandhi+" sandhi"+" => "+prefix+" + "+suffix
		found_print[1]=to_print
	
	#prnt_res =4 means print a short form of the sandhi in kannada
	
	elif found==1 and prnt_res==4:
		found_print[0]=found
		sandhi=con.convert(sandhi)
		prefix=con.convert(prefix)
		suffix=con.convert(suffix)
		to_print="\n"+sandhi+" ಸಂಧಿ "+" => "+prefix+" + "+suffix
		found_print[1]=to_print
		
	#customised for kannada interface
	elif found==1 and prnt_res==3:
		to_print="\nಸಂಧಿ ಪದ ಛೇದ ಸಫಲವಾಗಿದೆ.\n"
		sandhi=to_uni(sandhi)
		prefix=to_uni(prefix)
		suffix=to_uni(suffix)
		
		to_print+="ಪೂರ್ವ ಪದ     :   "+prefix+"\n"
		to_print+="ಉತ್ತರ ಪದ       :   "+suffix+"\n"
		to_print+="ಸಂಧಿ                :   "+sandhi+"\n"
		found_print[1]=to_print
	found_print[0]=found
	
	return found_print


#checking kannada sandhis
def check_kannada_sandhi(prefix,guessed_suffix,last,prnt_res):
	found=0
	found_print=[]
	found_print.append(0)
	found_print.append("")
	suffix = ""
	#print(f"last : {last}")
	#prefix=replaceback(prefix)
	#print(f"Prefix : {prefix}")
	if prefix=='kaM':
		prefix='kaN'
		#prefix=replaceback(prefix)
	if prefix=='beM':
		prefix='ben'
		#prefix=replaceback(prefix)
	prefix = replaceback(prefix)
	#print(f"Prefix : {prefix}")
	if prefix in dict_dawg:
		if last=='g':
			suffix='k'+guessed_suffix
			sandhi="AxeSa"
		elif last=='d':
			suffix='t'+guessed_suffix
			sandhi="AxeSa"
		elif last=='b':
			suffix='p'+guessed_suffix
			sandhi="AxeSa"
		elif last=='y' and guessed_suffix[:2]!="aa":
			suffix=guessed_suffix
			sandhi="Agama"
		elif last=='v':
			print("Agama")
			suffix=guessed_suffix
			sandhi="Agama" 
		suffix=replaceback(suffix)
		#print(f"Suffix : {suffix}")
		if suffix in dict_dawg:
			if prnt_res==3:
				to_print="\nಸಂಧಿ ಪದ ಛೇದ ಸಫಲವಾಗಿದೆ.\n"
				sandhi=to_uni(sandhi)
				prefix=to_uni(prefix)
				suffix=to_uni(suffix)
		
				to_print+="ಪೂರ್ವ ಪದ     :   "+prefix+"\n"
				to_print+="ಉತ್ತರ ಪದ       :   "+suffix+"\n"
				to_print+="ಸಂಧಿ                :   "+sandhi+"\n"
				found_print[1]=to_print
			elif prnt_res==4:
				found_print[0]=found
				sandhi=con.convert(sandhi)
				prefix=con.convert(prefix)
				suffix=con.convert(suffix)
				found_print[1]="\n"+sandhi+" ಸಂಧಿ "+" => "+prefix+" + "+suffix
			elif prnt_res==2:
				found_print[0]=found
				to_print="\n"+sandhi+" sandhi"+" => "+prefix+" + "+suffix
				found_print[1]=to_print
			else:
				found_print[1]=print_result(prefix,suffix,sandhi)
			found=1
			
	found_print[0]=found
	return found_print

#find lopa 
def check_lopa_sandhi(lopa_prefix,lopa_suffix,prnt_res):
	found=0
	found_print=[]
	found_print.append(0)
	found_print.append("")
	found_print[0]=0
	suffix_begin=lopa_suffix[0]
	possible_prefix=[]
	#lopa_prefix=replaceback(lopa_prefix)
	lopa_suffix=replaceback(lopa_suffix)
	if lopa_suffix in dict_dawg:
		for vowel in lopa_places:
			if lopa_suffix[0]=='o':
				if lopa_prefix+'e' in dictWords:
					vowel = 'e'
				else:
					vowel = vowel
			if lopa_suffix[0]=='u':
				vowel='u'
			prefix=lopa_prefix+vowel
			#print(f"Prefix Lopa before replace : {prefix}")
			prefix=replaceback(prefix)
			#print(f"Prefix Lopa : {prefix}")
			if prefix in dict_dawg:
				if prnt_res==3:
					to_print="\nಸಂಧಿ ಪದ ಛೇದ ಸಫಲವಾಗಿದೆ.\n"
					sandhi='lopa'
					sandhi=to_uni(sandhi)
					prefix=to_uni(prefix)
					suffix=to_uni(lopa_suffix)
		
					to_print+="ಪೂರ್ವ ಪದ     :   "+prefix+"\n"
					to_print+="ಉತ್ತರ ಪದ       :   "+suffix+"\n"
					to_print+="ಸಂಧಿ                :   "+sandhi+"\n"
					found_print[1]=to_print
				elif prnt_res==4:
					found_print[0]=found
					sandhi='lopa'
					sandhi=con.convert(sandhi)
					prefix=con.convert(prefix)
					suffix=con.convert(lopa_suffix)
					found_print[1]="\n"+sandhi+" ಸಂಧಿ "+" => "+prefix+" + "+suffix
				elif prnt_res==2:
					found_print[0]=found
					to_print="\nlopa sandhi"+" => "+prefix+" + "+lopa_suffix
					found_print[1]=to_print
				else:
					found_print[1]=print_result(prefix,lopa_suffix,"lopa")
				found_print[0]=1
				return found_print
	return found_print
		

#defining printing result
def print_result(prefix,suffix,sandhi):
	to_print="\nSandhi is successfully split!\n\n"
	to_print+="Puurvapada  :   "+prefix+"\n"
	to_print+="Uttarapada   :   "+suffix+"\n"
	to_print+="Sandhi            :   "+sandhi+"\n"
	return to_print
	
	
#print("Calling Sandhi Splitter")
#print(f"Argument passed : {sys.argv[1]}")
'''
res = sandhi_splitter(sys.argv[1],4)
print(f"Result : {res}")

mode = 'w'
if res[0] == 1:
	filename = 'correctoutputs.txt'
else:
	filename = 'erroroutputs.txt'
with open(filename,'a',encoding='utf-8') as f:
	f.write(f"Given word : {con.convert(sys.argv[1])}\n{res}\n")
	
f.close()
'''

