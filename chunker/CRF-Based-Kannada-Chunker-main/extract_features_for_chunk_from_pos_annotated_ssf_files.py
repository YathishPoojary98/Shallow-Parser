"""Extract raw sentences from a tokenized SSF file with no other annotations."""
from argparse import ArgumentParser
from re import findall
from re import DOTALL
from re import search
import os


def read_text_from_file(file_path):
	"""Read text from a file using a file path."""
	with open(file_path, 'r', encoding='utf-8') as file_read:
		return file_read.read().strip()


def find_sentences_from_ssf_text(text):
	"""Find all the sentences from text annotated in SSF format."""
	sentence_pattern = '<Sentence id=.*?>\n(.*?)\n</Sentence>'
	return findall(sentence_pattern, text, DOTALL)


def extract_features_for_chunking(sentences):
	"""Extract raw sentences from SSF tokenized sentences."""
	conll_sentences_with_chunk_features = []
	for sentence in sentences:
		tokens_in_ssf = sentence.split('\n')
		for token_in_ssf in tokens_in_ssf:
			token_in_ssf = token_in_ssf.strip()
			if token_in_ssf:
				addr, token, pos = token_in_ssf.split('\t')[: 3]
				conll_sentences_with_chunk_features.append(token + '\t' + pos)
		# the below code inserts a blank line between 2 sentences in conll format.		
		conll_sentences_with_chunk_features.append('')
	return conll_sentences_with_chunk_features


def write_lines_to_file(lines, file_path):
	"""Write lines to a file."""
	with open(file_path, 'w', encoding='utf-8') as file_write:
		file_write.write('\n'.join(lines))


def main():
	"""Pass arguments and call functions here."""
	parser = ArgumentParser()
	parser.add_argument('--input', dest='inp', help='Enter annotated SSF file or folder path')
	parser.add_argument('--output', dest='out', help='Enter the output file or folder path where features will be written to')
	args = parser.parse_args()
	# the below code is for processing a single file
	if not os.path.isdir(args.inp):
		input_text = read_text_from_file(args.inp)
		sentences = find_sentences_from_ssf_text(input_text)
		chunk_features_in_conll = extract_features_for_chunking(sentences)
		write_lines_to_file(chunk_features_in_conll, args.out)
	else:
		# the below code is for processing files inside a folder
		if not os.path.isdir(args.out):
			os.makedirs(args.out)
		for root, dirs, files in os.walk(args.inp):
			for fl in files:
				file_name = fl[: fl.rfind('.')]
				input_path = os.path.join(root, fl)
				input_text = read_text_from_file(input_path)
				sentences = find_sentences_from_ssf_text(input_text)
				chunk_features_in_conll = extract_features_for_chunking(sentences)
				output_path = os.path.join(args.out, file_name + '-chunk-features.txt')
				write_lines_to_file(chunk_features_in_conll, output_path)


if __name__ == '__main__':
	main()
