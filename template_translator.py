from time import sleep
import pandas as pd
import re
from googletrans import Translator

def punctuation_translate(origin):
    punctuation_tmp = origin

    punctuation_tmp = re.sub('，', ',', punctuation_tmp)
    punctuation_tmp = re.sub('：', ':', punctuation_tmp)
    punctuation_tmp = re.sub('（', '(', punctuation_tmp)
    punctuation_tmp = re.sub('）', ')', punctuation_tmp)
    punctuation_tmp = re.sub('。', '.', punctuation_tmp)

    return punctuation_tmp


template_file = 'Data/Templates/Mac_templates_doublecheck.csv'
translated_file = 'Data/TranslatedTemplates/Mac_translated.csv'

templates = pd.read_csv(template_file)['Templates']
translated_templates = []
templates_list = []

translator = Translator()
translator.raise_Exception = True
for tmp in templates:
    translated_tmp = translator.translate(text=tmp, dest='zh-cn').text
    translated_tmp = punctuation_translate(translated_tmp)
    sleep(0.2)
    if(tmp.count('<*>') == translated_tmp.count('<*>')):
        translated_templates.append(translated_tmp)
        templates_list.append(tmp)

translated_df = pd.DataFrame(
    {'Templates' : templates_list,
    'Translated' : translated_templates})
translated_df.to_csv(translated_file, index=False)