from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.task_group import TaskGroup
from services.morphs_tools import remove_emoji, remove_hashtags
from services.database import morphs_to_mongo, pull_daily_mongo
from konlpy.tag import *
import re
import math
import pandas as pd
import pymongo
from pymongo import MongoClient

url = "mongodb+srv://startup_proj_de_08:Team08!!@team08.mi7hgs1.mongodb.net/?retryWrites=true&w=majority"

def pull_mongo():
    """daily로 크롤링한 데이터 불러오기 (return:Dataframe)"""
    client = MongoClient(url)
    db = client["ConnectsLab"]
    collection = db["insta_crawling"]
    query = {}
    daily_data = collection.find(query)
    daily_data = pd.DataFrame(daily_data)
    return daily_data

# MongoDB에서 인스타그램 캡션을 가져오는 함수
def fetch_instagram_caption():
    client = pymongo.MongoClient(url)
    db = client.ConnectsLab
    collection = db.insta_crawling
    captions = collection.find({}, {"caption": 1})  # 필드명에 맞게 조정 필요
    return [u["caption"] for u in captions]

def process_caption(**kwargs):
    ti = kwargs['ti']
    captions = ti.xcom_pull(task_ids='task_id_fetch_instagram_caption')  # 이전 task에서 xcom_pull로 captions를 가져옴
    
    okt = Okt()
    data = fetch_instagram_caption()
    contents = captions.astype(str)
    morphs_list = []

    for content in contents:
        content = remove_hashtags(content)
        content = remove_emoji(content)
        morphs = okt.pos(content, norm=True, stem=True)
        morphs_list.append(morphs)

    data.drop('caption', axis=1, inplace=True)

    kind = ['Noun','Verb','Adjective','Determiner','Adverb','Conjunction','Exclamation','Josa','PreEomi',
            'Punctuation','Foreign','Alpha','Number','KoreanParticle','Modifier']

    for i in kind:
        globals()[f"{i}_list"] = []

    for mor in morphs_list:
        for i in kind:
            try:
                a = [item[0] for item in mor if item[1] == str(i)]
                globals()[f"{i}_list"].append(a)
            except:
                globals()[f"{i}_list"].append('')

    for index,value in enumerate(kind):
        data.insert(index+1, f'{value}', globals()[f"{value}_list"])
    
    data = data.to_dict('records')
    morphs_to_mongo(data=data)


# 기본 DAG 설정
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 12, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG 인스턴스 생성
dag = DAG(
    'instagram_username_tasks',
    default_args=default_args,
    description='A DAG to process Instagram captions',
    schedule_interval=timedelta(days=1),
)

# TaskGroup 생성
with TaskGroup(group_id='inner_group_1') as process_caption_group:
    # 태스크 생성
    for i in range(3):
        chunk = captions[i * chunk_size:(i + 1) * chunk_size]
        task = PythonOperator(
            task_id=f'process_caption_{i}',
            python_callable=process_caption,
            provide_context=True,
            op_kwargs={'captions': chunk},
            dag=dag,
        )

# 의존성 설정: TaskGroup 내의 태스크들을 병렬로 실행하도록 설정
process_caption_group
