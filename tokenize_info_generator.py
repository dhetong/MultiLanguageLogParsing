import csv
from snownlp import SnowNLP
from translated_log_spliter import multi_language_tokenizer

def translated_log_tokenizer(line, is_split):
    if(is_split):
        token_list = list(SnowNLP(line).words)
        return token_list
    else:
        token_list = multi_language_tokenizer(line)
        return token_list

is_split = False
translated_log_file = 'Data/TranslatedLog/HPC_translated_content.log'
tokenize_output_file = 'Data/TokenizeInfo/HPC_translated_tokenize.csv'

tokenize_output = open(tokenize_output_file, 'w')
tokenize_writer = csv.writer(tokenize_output)
tokenize_writer.writerow(['Tokenlist'])
loglines = open(translated_log_file).readlines()

for log in loglines:
    token_list = translated_log_tokenizer(log, is_split)
    row = []
    row.append(token_list)
    tokenize_writer.writerow(row)