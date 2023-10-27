import sys
import time
import parameter_config as pc

sys.path.append('../../')
from Drain_for_translated import LogParser_translated
from Drain import LogParser
from Drain_for_translated_split import LogParser_translated_split

input_dir = 'Data/TranslatedLog/'
output_dir = 'Data/Output/'
translated_log_file = 'Apache_translated_content.log'
correspond_log_file = 'Apache_correspond_content.log'
log_format = '<Content>'
regex = pc.Apache_regex
depth = pc.Apache_depth
st = pc.Apache_st

start_time = time.time()

parser_translated = LogParser_translated(log_format, indir=input_dir, outdir=output_dir,  depth=depth, st=st, rex=regex)
parser_translated.parse(translated_log_file)

translated_time = time.time()

parser_correspond = LogParser(log_format, indir=input_dir, outdir=output_dir,  depth=depth, st=st, rex=regex)
parser_correspond.parse(correspond_log_file)

original_time = time.time()

parser_translated_split = LogParser_translated_split(log_format, indir=input_dir, outdir=output_dir,  depth=depth, st=st, rex=regex)
parser_translated_split.parse(translated_log_file)

translated_split_time = time.time()

print("end-to-end time for original log: " + str(original_time-translated_time))
print("end-to-end time for translated log: " + str(translated_time-start_time))
print("end-to-end time for translated log with split strategy: " + str(translated_split_time-original_time))