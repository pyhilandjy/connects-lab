from datetime import datetime, timedelta
from pymongo import MongoClient
from utils.config import settings
import random


# MongoDB에 데이터를 삽입하는 함수
def insert_into_mongodb():
    client = MongoClient("ig-airflow-mongodb-1", 27017)
    db = client["instagram_data"]
    collection = db["posts"]

    # 삽입할 데이터 예시
    post_data = {
        "username": "가나다",
        "like": 123,
        "body": "하하호호",
        "created_time": datetime.now().strftime("%Y-%m-%d"),
    }

    # 데이터 삽입
    try:
        collection.insert_one(post_data)
    except Exception as e:
        print(f"{e}")
    else:
        print(f"Inserted: {post_data}")

    # MongoDB 연결 종료
    client.close()


def airflow_config():
    print("HIIHIHIHHIHI")
    from airflow import DAG
    from airflow.operators.python_operator import PythonOperator

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
        "main",
        default_args=default_args,
        description="A simple DAG to insert data into MongoDB every 10 seconds",
        schedule_interval=timedelta(seconds=10),
        start_date=datetime(2023, 11, 17),  # 현재 날짜로 변경
        catchup=False,  # 과거 데이터 캐치업 방지
    )

    # Python Operator 정의
    insert_task = PythonOperator(
        task_id="main",
        python_callable=insert_into_mongodb,
        dag=dag,
    )

    # DAG 설정
    return insert_task


if settings.is_prod:
    airflow_config()