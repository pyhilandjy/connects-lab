from datetime import datetime, timedelta
import pandas as pd
from konlpy.tag import Okt
from pymongo import MongoClient
import re
from services.database import morphs_to_mongo
from services.morphs_tools import remove_emoji, remove_hashtags
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

url = "mongodb+srv://startup_proj_de_08:Team08!!@team08.mi7hgs1.mongodb.net/?retryWrites=true&w=majority"

def pull_daily_mongo():
    """daily로 크롤링한 데이터 불러오기 (return: Dataframe)"""
    client = MongoClient(url)
    db = client["ConnectsLab"]
    collection = db["insta_crawling"]
    query = {}
    daily_data = collection.find(query)
    daily_data = pd.DataFrame(daily_data)
    return daily_data

data = pull_daily_mongo()

# 데이터를 부분으로 나누는 함수 정의
def split_data(data, num_parts):
    total_len = len(data)
    part_size = total_len // num_parts
    split_data_list = [pd.DataFrame(data[i:i + part_size]) for i in range(0, total_len, part_size)]
    return split_data_list

# 데이터를 3 부분으로 나눔 (원하는 부분의 수로 변경 가능)
num_parts = 3
split_data_result = split_data(data, num_parts)

# 리스트의 각 데이터프레임에 접근
for i, dataframe in enumerate(split_data_result, start=1):
    variable_name = f"data_{i}"
    globals()[variable_name] = dataframe

for i in range(1, num_parts + 1):
    variable_name = f"data_{i}"



def morphs(data):
    okt = Okt()

    contents = data['caption'].astype(str)
    morphs_list = []


    for content in contents:
        #형태소 분석
        content = remove_hashtags(content)
        content = remove_emoji(content)
        morphs = okt.pos(content,norm=True, stem=True)
        morphs_list.append(morphs)

    data.drop('caption',axis=1,inplace=True)

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
        data.insert(index+1,f'{value}',globals()[f"{value}_list"])
    data = data.to_dict('records')
    morphs_to_mongo(data=data)

# Airflow DAG 설정
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    "get_instagram_info",
    default_args=default_args,
    description="A simple DAG to insert data into MongoDB every 10 seconds",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 11, 30),  # 현재 날짜로 변경
    catchup=False,  # 과거 데이터 캐치업 방지
)

# Python Operator 정의
morphs_ts_1 = PythonOperator(
    task_id="test_1",
    python_callable=morphs(data=data_1),
    dag=dag,
)

morphs_ts_2 = PythonOperator(
    task_id="test_2",
    python_callable=morphs(data=data_2),
    dag=dag,
)

morphs_ts_3 = PythonOperator(
    task_id="test_3",
    python_callable=morphs(data=data_3),
    dag=dag,
)

# Set up the task dependency
[morphs_ts_1, morphs_ts_2, morphs_ts_3]