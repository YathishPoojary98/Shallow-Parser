setu=/home/yathish_poojary/Yathish/Dependency_Parser/Parser
perl $setu/printinput.pl $1 > headcomputationinput
#python $setu/bin/sl/headcomputation/autowxmorph.py headcomputationinput 
perl $setu/headcomputation/headcomputation.pl --path=$setu/headcomputation --input=headcomputationinput --output=headding-out.txt
python $setu/headcomputation/add_quotes.py headding-out.txt > head-out.txt
