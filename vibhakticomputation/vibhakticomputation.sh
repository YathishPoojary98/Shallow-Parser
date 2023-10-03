setu=/home/yathish_poojary/Yathish/Dependency_Parser/Parser
perl $setu/printinput.pl $1 > vibhakticomputationinput
perl $setu/vibhakticomputation/vibhakticomputation.pl --path=$setu/vibhakticomputation --input=vibhakticomputationinput 
#--output=vibhakti-out.txt
