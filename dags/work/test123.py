from datetime import datetime, timedelta
import pandas as pd
from konlpy.tag import Okt
from pymongo import MongoClient
from services.database import morphs_to_mongo
from services.morphs_tools import remove_emoji, remove_hashtags
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

url = "mongodb+srv://startup_proj_de_08:Team08!!@team08.mi7hgs1.mongodb.net/?retryWrites=true&w=majority"

def pull_daily_mongo():
    """daily로 크롤링한 데이터 불러오기 (return: Dataframe)"""
    client = MongoClient(url)
    db = client["ConnectsLab"]
    collection = db["insta_daily_data_test"]
    query = {}
    daily_data = collection.find(query)
    daily_data = pd.DataFrame(daily_data)
    return daily_data

data = pull_daily_mongo()

def split_data(data, num_parts):
    """num_parts만큼 data를 나눔"""
    total_len = len(data)
    part_size = total_len // num_parts
    split_data_list = [pd.DataFrame(data[i:i + part_size]) for i in range(0, total_len, part_size)]
    return split_data_list

def morphs(**kwargs):
    """caption을 토크나이징"""
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='split_data_task')

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

    for mor in morphs_list:
        for i in kind:
            try:
                a = [item[0] for item in mor if item[1] == str(i)]
                globals()[f"{i}_list"].append(a)
            except:
                globals()[f"{i}_list"].append('')

    for index, value in enumerate(kind):
        data.insert(index + 1, f'{value}', globals()[f"{value}_list"])
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
    "morphs_test",
    default_args=default_args,
    description="A simple DAG to insert data into MongoDB every 10 seconds",
    schedule_interval='@daily',
    start_date=datetime(2023, 11, 30),
    catchup=False,
)

# 데이터를 부분으로 나누기
num_parts = 3
split_data_result = split_data(data, num_parts)

split_data_task = PythonOperator(
    task_id="split_data_task",
    python_callable=split_data,
    op_args=[data, num_parts],
    provide_context=True,
    dag=dag,
)

morphs_tasks = []
for i, dataframe in enumerate(split_data_result, start=1):
    variable_name = f"data_{i}"

    morphs_task = PythonOperator(
        task_id=f"morphs_test_{i}",
        python_callable=morphs,
        op_args=[variable_name],
        provide_context=True,
        dag=dag,
    )

    split_data_task >> morphs_task
    morphs_tasks.append(morphs_task)

# Set up the task dependency
# Set up the task dependency
split_data_task >> [morphs_tasks[0], morphs_tasks[1], morphs_tasks[2]]  # split_data_task이 먼저 실행되고, 그 결과를 morphs_tasks에 전달



