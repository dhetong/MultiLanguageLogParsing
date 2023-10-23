import pandas as pd
import re

from regex_generate import templates2regex

def replace_first(string, sub, replace):
    where = [m.start() for m in re.finditer(sub, string)][0]
    before = string[:where+1]
    after = string[where+1:]
    before = before.replace(sub, replace, 1)
    newString = before + after
    return newString

translated_template_file = 'Data/TranslatedTemplates/Mac_translated.csv'
log_file = 'Data/Log/MacContent.log'
translated_log_file = 'Data/TranslatedLog/Mac_translated_content.log'
translated_corresspond_log_file = 'Data/TranslatedLog/Mac_correspond_content.log'

translated_df = pd.read_csv(translated_template_file)
templates = list(translated_df['Templates'])
translated_templates = list(translated_df['Translated'])

templates_dict = {}
n_template = len(templates)
template_index = 0
while(template_index < n_template):
    templates_dict[templates[template_index]] = translated_templates[template_index]
    template_index = template_index+1

loglines = open(log_file).readlines()
translated_file = open(translated_log_file, "w")
translated_correspond_file = open(translated_corresspond_log_file, "w")

for log in loglines:
    trans_log = None
    for tmp in templates:
        tmp_regex = templates2regex(tmp)
        if(re.match(tmp_regex, log)):
            trans_tmp = templates_dict[tmp]
            if('<*>' in tmp):
                para_list = re.findall(tmp_regex, log)[0]
                if(isinstance(para_list, tuple)):
                    n_para = len(para_list)
                    index = 0
                    while (index < n_para):
                        trans_tmp = replace_first(trans_tmp, '<*>', str(para_list[index]))
                        index = index + 1
                else:
                    trans_tmp = trans_tmp.replace('<*>', para_list[0])
            trans_log = trans_tmp
            break
    if(trans_log != None):
        translated_file.write(trans_log + '\n')
        translated_correspond_file.write(log)