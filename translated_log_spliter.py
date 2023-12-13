import jieba
from snownlp import SnowNLP
import thulac

def is_English(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def language_split(log):
    flag = False
    str_list = []
    tmp_eng = ''
    tmp_other_language = ''
    for c in log:
        if (is_English(c)):
            flag = True
        else:
            flag = False
        if (flag):
            tmp_eng = tmp_eng + c
            if (tmp_other_language.__eq__('')):
                pass
            else:
                tmp_other_language = '[otherlanguage]' + tmp_other_language
                str_list.append(tmp_other_language)
                tmp_other_language = ''
        else:
            tmp_other_language = tmp_other_language + c
            if (tmp_eng.__eq__('')):
                pass
            else:
                str_list.append(tmp_eng)
                tmp_eng = ''
    if ((flag == True) & (tmp_eng.__eq__('') == False)):
        str_list.append(tmp_eng)
    if ((flag == False) & (tmp_other_language.__eq__('') == False)):
        tmp_other_language = '[otherlanguage]' + tmp_other_language
        str_list.append(tmp_other_language)
    return str_list

def append_tokens(ori_list, tokens):
    for token in tokens:
        ori_list.append(token)
    return ori_list

def tokenizer_on_list(str_list):
    token_list = []
    for str in str_list:
        if(str.startswith('[otherlanguage]')):
            str = str[15:len(str)]
            tokens = list(SnowNLP(str).words)
            token_list = append_tokens(token_list, tokens)
        else:
            tokens = str.split(' ')
            token_list = append_tokens(token_list, tokens)
    return token_list

def multi_language_tokenizer(log):
    str_list = language_split(log)
    token_list = tokenizer_on_list(str_list)
    return token_list

# str = '1无法配置Resourcemgmt子系统err = 10'
#
# token_list = multi_language_tokenizer(str)
# print(token_list)