"""Correct incorrect predicted chunk tags."""
import argparse
import os
from string import punctuation


# List of all symbols
symbols = set(punctuation) - set(';,".')



def read_lines_from_file_with_blanks(file_path):
    """Read lines from a file using its file path."""
    with open(file_path, 'r', encoding='utf-8') as file_read:
        return file_read.readlines()


def update_incorrect_chunk_tags(lines):
    """Update the incprrect chunks tags using some heuristics."""
    updated_lines = []
    prev_label, prev_type = '', ''
    for line in lines:
        #print(f"Line : {line}")
        line = line.strip()
        if line:
            token, pos_tag, chunk_tag = line.split('\t')
            if token in symbols and pos_tag != 'RD_SYM':
                pos_tag = 'RD_SYM'
                line = '\t'.join([token, pos_tag, chunk_tag]) 
            if token in ';,"।.' and pos_tag != 'RD_PUNC':
                pos_tag = 'RD_PUNC'
                line = '\t'.join([token, pos_tag, chunk_tag])
            chunk_label, chunk_type = chunk_tag.split('-')
            if not prev_label and not prev_type:
                if chunk_label == 'I':
                    updated_lines.append(token + '\t' + pos_tag + '\t' + 'B-' + chunkType + '\n') 
                    prev_label = 'B'
                else:
                    updated_lines.append(line)
                    prev_label = chunk_label
                prev_type = chunk_type
            else:
                if chunk_label != prev_label and chunk_type == prev_type:
                    updated_lines.append(line)
                    prev_label = chunk_label
                    prev_type = chunk_type
                elif chunk_type != prev_type and chunk_label == 'I':
                    updated_lines.append(token + '\t' + pos_tag + '\t' + 'B-' + chunk_type +  '\n')
                    prev_label = 'B'
                    prev_type = chunk_type
                else:
                    updated_lines.append(line)
                    prev_label = chunk_label
                    prev_type = chunk_type
        else:
            updated_lines.append(line)
            prev_label, prev_type = '', ''
    updated_lines[-1]='\n'
    return updated_lines


def write_lines_to_file(lines, file_path):
    """Write lines to a file."""
    with open(file_path, 'w', encoding='utf-8') as file_write:
        file_write.write('\n'.join(lines))


def read_files_from_folder_update_incorrect_chunks_and_write(input_folder_path, output_folder_path):
    """Update incorrect chunks for multiple files."""
    if os.path.isdir(input_folder_path):
        for root, dirs, files in os.walk(input_folder_path):
            input_file_paths = [os.path.join(root, fl) for fl in files]
            output_file_paths = [os.path.join(output_folder_path, fl) for fl in files]
        for index_file, input_path in enumerate(input_file_paths):
            input_lines = read_lines_from_file_with_blanks(input_path)
            updated_lines = update_incorrect_chunk_tags(input_lines)
            output_path = output_file_paths[index_file]
            write_lines_to_file(updated_lines, output_path)
    else:
        input_lines = read_lines_from_file_with_blanks(input_folder_path)
        updated_lines = update_incorrect_chunk_tags(input_lines)
        write_lines_to_file(updated_lines, output_folder_path)


def main():
    """Pass arguments and call functions here."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='inp', help='Enter the input folder path')
    parser.add_argument('--output', dest='out', help='Enter the output folder path')
    args = parser.parse_args()
    if os.path.isdir(args.inp) and not os.path.isdir(args.out):
        os.mkdir(args.out)
    read_files_from_folder_update_incorrect_chunks_and_write(args.inp, args.out)


if __name__ == '__main__':
    main()
