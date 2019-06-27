# encoding:utf-8
import re
from  pathlib import Path
from tqdm import tqdm
def sentence_concat(file_path):
    """
    句子拼接，将被切开的句子还原
    :param texts:
    :return:
    """
    with open(file_path,'r',encoding='utf-8') as f:
        is_full = True # 表示句子是否完整
        concat_list = list() # 存放用于拼接的句子
        result_list = list() # 存放最终的句子
        for line in f:
            line = line.strip()
            if line == '' or line == None:
                continue
            if not is_full:
                test = concat_list.pop()
                line = test+' '+line
                is_full = True

            result = re.match('[a-zA-z,]',line[-1])
            if result: # 说明句子需要拼接
                concat_list.append(line)
                is_full = False
            else:
                result_list.append(line)

    with open('/Users/fangwenda/Documents/doctorwho-dialog/concat_text/'+file_path.name,'w',encoding='utf-8') as f:
        for line in result_list:
            f.write(line+'\n')

if __name__ == '__main__':
    p = Path('/Users/fangwenda/Documents/doctorwho-dialog/text')
    text_files = list(p.glob("./*.txt"))
    for text_file in tqdm(text_files):
        sentence_concat(text_file)



