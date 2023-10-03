# this shell script takes 3 arguments
# input folder: Input folder path containing SSF POS Annotated text or conll files in the format token\tpos
# chunk_model_path: Path of CRF trained chunker model
# format: Format of the data; ssf or conll
# this code works at folder level
repo="/home/yathish_poojary/Yathish/Dependency_Parser/Parser/chunker/CRF-Based-Kannada-Chunker-main"
input_folder=$1
chunk_model_path=$2
format=$3
pred_chunks_folder=$input_folder"-Predicted-Chunks"
corrected_chunks_folder=$input_folder"-Corrected-Chunks"
# this creates Chunk Features folder for SSF annotated data
if [ $format = "ssf" ];then
	chunk_features_folder=$input_folder"-Chunk-Features"
	if [ ! -d $chunk_features_folder ];then
		mkdir $chunk_features_folder
	fi
fi
if [ ! -d $pred_chunks_folder ];then
	mkdir $pred_chunks_folder
fi
if [ ! -d $corrected_chunks_folder ];then
	mkdir $corrected_chunks_folder
fi
if [ $format = "ssf" ];then
	python3 $repo/extract_features_for_chunk_from_pos_annotated_ssf_files.py --input "$input_folder" --output "$chunk_features_folder"
else
	chunk_features_folder=$input_folder
fi
for fl in $(ls $chunk_features_folder);do
	file_path="$chunk_features_folder"/"$fl"
	pred_chunk_path="$pred_chunks_folder"/"$fl"
	crf_test -m $chunk_model_path $file_path > $pred_chunk_path
done
python3 $repo/correct_incorrect_chunks.py --input "$pred_chunks_folder" --output "$corrected_chunks_folder"
output_folder=./
if [ $format = "ssf" ];then
	if [ ! -d $output_folder ];then
		mkdir $output_folder
	fi
	python3 $repo/read_feature_files_and_convert_into_ssf.py --input "$corrected_chunks_folder" --output "$output_folder" --opr 1
else
	mv $corrected_chunks_folder $output_folder
fi
