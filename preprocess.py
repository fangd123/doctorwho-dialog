# encoding:utf-8
import re
from pathlib import Path
from tqdm import tqdm
import json
import pickle
from nltk.tokenize import word_tokenize


def sentence_concat(file_path):
    """
    句子拼接，将被切开的句子还原
    :param texts:
    :return:
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        is_full = True  # 表示句子是否完整
        concat_list = list()  # 存放用于拼接的句子
        result_list = list()  # 存放最终的句子
        for line in f:
            line = line.strip()
            if line == '' or line == None:
                continue
            if not is_full:
                test = concat_list.pop()
                line = test + ' ' + line
                is_full = True

            result = re.match('[a-zA-z,]', line[-1])
            if result:  # 说明句子需要拼接
                concat_list.append(line)
                is_full = False
            else:
                result_list.append(line)

    Path('text/concat_text/' + file_path.parts[-2]).mkdir(exist_ok=True, parents=True)
    with open('text/concat_text/' + file_path.parts[-2] + '/' + file_path.name, 'w', encoding='utf-8') as f:
        for line in result_list:
            f.write(line + '\n')


def preprocess_s_concat():
    p = Path('text/stories')
    text_files = list(p.glob("./*/*.txt"))
    for text_file in tqdm(text_files):
        sentence_concat(text_file)


def character_episode_match(chara_path, episode_path):
    chara_path = Path(chara_path)
    chara_list = list(chara_path.glob('*.txt'))
    chara_list = [x.stem for x in chara_list]
    episode_path = Path(episode_path)
    episodes = list(episode_path.glob("./*/*.txt"))
    for episode in tqdm(episodes):
        with open(episode, 'r', encoding='utf-8') as f:
            characters = set()
            for line in f:
                line = line.strip()
                # 如果到了文本最后，就可以直接翻篇了
                if line[:2] == '[<' or line == '---':
                    break
                # 这些不属于对白，可以直接跳过
                if line == '' or line[:3] == '**[' or line[0] == '(':
                    continue

                who_said = line.split(':')
                if len(who_said) > 1 and who_said[0][:3].isupper():
                    characters.add(who_said[0].lower().replace('[oc]', '').strip())
        char_map = dict()
        for charactor in characters:
            if charactor == "doctor":
                continue
            temp = list(filter(lambda x: charactor in x.lower(), chara_list))
            if len(temp) > 0:
                char_map[charactor] = temp[0]
        if char_map == {}:
            continue
        Path('text/char_map/' + episode.parts[-2]).mkdir(exist_ok=True)
        with open('text/char_map/' + episode.parts[-2] + '/' + episode.name, 'w', encoding='utf-8') as f1:
            json.dump(char_map, f1)


def split_by_scene():
    from collections import defaultdict
    import re
    import pickle
    """
    根据剧本场景分割剧本
    :return: 
    """
    p = Path('text/concat_text')
    files = list(p.glob('./*/*.txt'))
    for one_file in tqdm(files):
        with open(one_file, 'r', encoding='utf-8') as f:
            is_saying = False
            scene_list = list()
            scene_info = dict()
            dialog = list()
            who_sents = defaultdict(list)
            for line in f:
                if line[:2] == '[<' or line == '---':
                    break
                if line[0] == '(':
                    continue
                if len(re.findall(r"\*\*\[(.*)\]\*\*", line)) > 0:
                    if len(dialog) > 0:
                        dialog.append(who_sents)
                        scene_info['dialog'] = dialog
                        scene_list.append(scene_info)

                        scene_info = dict()
                        dialog = list()

                    scene = re.findall(r"\*\*\[(.*)\]\*\*", line)
                    scene_info['scene'] = scene[0]
                    continue

                who_said = line.split(':')
                if len(who_said) > 1 and who_said[0][:3].isupper():
                    is_saying = True
                    if len(who_sents) > 0:
                        dialog.append(who_sents)
                        who_sents = defaultdict(list)
                    who_sents[who_said[0]].append(who_said[1])
                elif is_saying:
                    who_sents[who_said[0]].append(line)
        Path(f'text/format_dialog/{one_file.parts[-2]}').mkdir(parents=True, exist_ok=True)
        with open(f'text/format_dialog/{one_file.parts[-2]}/{one_file.name}.pkl', 'wb') as f:
            pickle.dump(scene_list, f)


def dialog_chunk(size=640):
    """
    对话数据分块
    考虑到使用BPE算法之后，词长度会变大，因此需要留有一定的余量
    这里就是简单的分词之后直接判断了
    :return:
    """
    p = Path('text/format_dialog')
    files = list(p.glob('./*/*.txt.pkl'))
    for one_file in tqdm(files):
        with open(one_file, 'rb') as f:
            scences = pickle.load(f)


class PersonSay:
    def __init__(self, one: dict):
        self.name = one.keys()[0]
        self.sents = list(one.values())

    def __len__(self):
        return sum(map(lambda x: len(word_tokenize(x.strip()), self.sents)))

def scence_chunk(scence, chunk_size):
    """
    对场景按照一定的大小限制进行分块
    分割为多个场景
    :param scence:
    :param chunk_size:
    :return:
    """
    dialog = scence['dialog']
    place = scence['place']
    for one in dialog:
        chunk_list = []
        chunk_text = ''
        cache_text = None

        person_say = PersonSay(one)
        # 不存在缓存
        if cache_text == None:
            if sum(map(lambda x: len(x), chunk_text)) + len(person_say) > chunk_size:
                assert sum(map(lambda x: len(x), chunk_text)) <= chunk_size
                chunk_list.append(chunk_text)
                chunk_text = list()
                cache_text = person_say
            else:
                chunk_text.append(person_say)
        # 存在缓存
        else:
            if sum(map(lambda x: len(x), chunk_text)) + len(cache_text) > chunk_size:
                assert sum(map(lambda x: len(x), chunk_text)) <= chunk_size
                chunk_list.append(chunk_text)
                chunk_text = list()
            chunk_text.append(person_say)
            cache_text = None
            if sum(map(lambda x: len(x), chunk_text)) + len(person_say) > chunk_size:
                assert sum(map(lambda x: len(x), chunk_text)) <= chunk_size
                chunk_list.append(chunk_text)
                chunk_text = list
                cache_text = person_say
            else:
                chunk_text.append(person_say)

    chunk_scence = list()
    for one in chunk_list:
        dialog_list = [{x.name:x.sents} for x in one]
        chunk_scence.append({'place':place,'dialog':dialog_list})

    return chunk_scence


if __name__ == '__main__':
    # split_by_scene()
    # preprocess_s_concat()
    # character_episode_match('text/characters','text/stories')
    #filter_has_doctor()
    pass
