setu=/home/yathish_poojary/Yathish/Dependency_Parser/Parser
path=$setu/morph/Morph-Tool
#echo $1
python $path/rootadd.py $1 
perl $path/fsgenerate.pl $1 $2 $path/rootsandsuff.txt
#rm rootsandsuff.txt
#rm intermediate
