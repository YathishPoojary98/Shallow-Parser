# This is a repository for CRF based Kannada Chunker.
## Install CRF++ from this link https://taku910.github.io/crfpp/
## How to run the code
## sh predict_chunk_tags_for_pos_annotated_files_and_convert_to_ssf.sh input_folder_path model_path format
### input_folder_path: contains Kannada files either in SSF (Shakti Standard Format) or CoNLL format
### chunk_model_path: Path of the Kannada chunk model
### format: Type the format either ssf or conll 
### Final Outputs will be saved in a folder appended with the format identifier either ssf or conll 
### Give absolute paths for all the paths (relative path may throw an error)
### SSF format Details (https://aclanthology.org/W14-5208.pdf) [avoid the backslash / at the end of the path]
