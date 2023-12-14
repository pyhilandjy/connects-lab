from services.morphs_tools import remove_emoji, remove_hashtags
from services.database import morphs_to_mongo, pull_daily_mongo
from konlpy.tag import *
import re
import pandas as pd
import json
import os


def morphs(**kwargs):
    """caption을 토크나이징"""
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='split_data_task')

    komoran = Komoran()
    okt = Okt()
    contents = data['caption'].astype(str)
    morphs_list = []

    for content in contents:
        content = remove_hashtags(content)
        content = remove_emoji(content)
        morphs = okt.pos(content, norm=True, stem=True)
        morphs_list.append(morphs)

    data.drop('caption', axis=1, inplace=True)

    kind = ['Noun', 'Verb', 'Adjective', 'Determiner', 'Adverb', 'Conjunction', 'Exclamation', 'Josa', 'PreEomi',
            'Punctuation', 'Foreign', 'Alpha', 'Number', 'KoreanParticle', 'Modifier']

    for i in kind:
        globals()[f"{i}_list"] = []

    #형태소별 리스트에 추가
    for mor in morphs_list:
        for i in kind[5:]:
            try:
                a = [item[0] for item in mor if item[1] == str(i)]
                globals()[f"{i}_list"].append(a)
            except:
                globals()[f"{i}_list"].append('')

    #명사 세분화

    Noun_morphs_list=[]

    for i in Noun_list:
        Noun_morph = komoran.pos(' '.join(i))
        Noun_morphs_list.append(Noun_morph)

    for nou in Noun_morphs_list:
        for i in kind[:5]:
            try:
                b = [item[0] for item in nou if item[1] == str(i)]
                globals()[f"{i}_list"].append(b)
            except:
                globals()[f"{i}_list"].append('')
                
    #기존 데이터프레임에 형태소별 추가            
    for index,value in enumerate(kind):
        data.insert(index+1,f'{value}',globals()[f"{value}_list"])
    data = data.to_dict('records')
    morphs_to_mongo(data=data)
    return data

def split_data(data, num_parts):
    """num_parts만큼 data를 나눔"""
    total_len = len(data)
    part_size = total_len // num_parts
    split_data_list = [pd.DataFrame(data[i:i + part_size]) for i in range(0, total_len, part_size)]
    return split_data_list


def update_json_file(**kwargs):
    ti = kwargs['ti']
    morphs_results = [ti.xcom_pull(task_ids=f"morphs_{i}") for i in range(1, num_parts)]

    # 파일 경로
    file_path = 'insta_crawling_morphs.json'

    # 파일이 존재하지 않을 경우 빈 리스트로 초기화
    if not os.path.exists(file_path):
        all_data = []
    else:
        # 파일이 이미 존재하면 기존 데이터를 읽어옴
        with open(file_path, 'r', encoding='utf-8') as insta_json:
            all_data = json.load(insta_json)

    # morphs_results를 all_data에 추가
    all_data.extend(morphs_results)

    # 파일 쓰기
    with open(file_path, 'w', encoding='utf-8') as insta_json:
        json.dump(all_data, insta_json, ensure_ascii=False, indent=4)



