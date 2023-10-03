setu=/home/yathish_poojary/Yathish/Dependency_Parser
#slang=$3
#tlang=$4
#stlang=$slang_$tlang

output_folder="Output"

#utf2wx	
#python $bin/sys/common/convertor-indic-1.5.2/convertor.py $1 $2
#Tokenizer
python $setu/Tokenizer/tokenizer_for_indian_languages_on_files.py --input $1 --output inter --lang kn

#Conll
python $setu/postagger/create_conll.py inter

#POSTagger
if [ ! -d "$output_folder" ]; then
  mkdir "$output_folder"
fi
python $setu/postagger/run_pos.py --input conll.txt --output ./Output/posout.ssf --model $setu/postagger/checkpoint

#Chunker
sh $setu/chunker/CRF-Based-Kannada-Chunker-main/predict_chunk_tags_for_pos_annotated_files_and_convert_to_ssf.sh Output $setu/chunker/CRF-Based-Kannada-Chunker-main/kannada-chunk-model.m ssf
perl $setu/chunker/crtpostag.pl posout-chunk-features.txt

#Morph
sh $setu/morph/Morph-Tool/morphtool.sh posout-chunk-features.txt morph-out.txt
python $setu/morph/Morph-Tool/autowxmorph.py morph-out.txt

#Headcomputation
sh $setu/headcomputation/headcomputation.sh morph-wxout.txt

#Vibhakti computation
sh $setu/vibhakticomputation/vibhakticomputation.sh head-out.txt

#Parser
#sh $bin/sl/simple_parser/kan/simple_parser_kan.sh vibhakti-out.txt
#sh $bin/sl/simple_parser/kan/parser.sh vibhakti-out.txt parser-out.txt

#remove
rm -r inter conll.txt Output-Chunk-Features Output-Corrected-Chunks Output-Predicted-Chunks Output posout-chunk-features.txt morph-out.txt morph-wxout.txt headcomputationinput head-out.txt vibhakticomputationinput headding-out.txt
#vibhakti-out.txt parserinput
