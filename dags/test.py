from datetime import datetime, timedelta
import pandas as pd
from konlpy.tag import Okt
from pymongo import MongoClient
from services.database import morphs_to_mongo
from services.morphs_tools import remove_emoji, remove_hashtags
from airflow import DAG
from airflow.operators.python_operator import PythonOperator


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

