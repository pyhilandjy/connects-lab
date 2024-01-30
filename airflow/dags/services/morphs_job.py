from services.morphs_tools import remove_emoji, remove_hashtags
from services.database import morphs_to_mongo, pull_daily_mongo
from konlpy.tag import *
import re
import pandas as pd
import json
import os
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta


def morphs(**kwargs):
    """caption을 토크나이징"""
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='split_data_task', key='morphs')

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

def split_data(data, num_parts, **kwargs):
    """num_parts만큼 data를 나눔"""
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='get_instagram_info', key='instagram_data')
    num_parts = kwargs['num_parts']
    total_len = len(data)
    part_size = total_len // num_parts
    split_data_list = [pd.DataFrame(data[i:i + part_size]) for i in range(0, total_len, part_size)]
    kwargs['ti'].xcom_push(key='morphs', value= split_data_list) 
    return split_data_list


def update_json():
    one_day_ago = datetime.now() - timedelta(days=1)

    one_day_ago = one_day_ago.strftime('%Y-%m-%d')


    url = "mongodb+srv://startup_proj_de_08:Team08!!@team08.mi7hgs1.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(url)

    db = client["ConnectsLab"]
    collection = db["insta_crawling_morphs"]

    def json_serial(obj):
        """JSON serializer for objects not serializable by default."""
        if isinstance(obj, ObjectId):
            return str(obj)
        raise TypeError("Type not serializable")

    file_path = '/opt/airflow/dags/services/insta_crawling_morphs.json'

    with open(file_path, "r") as existing_json_file:
        existing_data = json.load(existing_json_file)

        mongo_data = list(collection.find({'upload_date': one_day_ago}))

        existing_data.extend(mongo_data)


    with open(file_path, "w") as json_file:
        json.dump(existing_data, json_file, default=json_serial,ensure_ascii=False, indent=4)