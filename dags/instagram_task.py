from datetime import datetime, timedelta
from konlpy.tag import *

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from services.instagram_job import get_instagram
from services.morphs_job import morphs

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
get_instagram_task = PythonOperator(
    task_id="get_instagram_info",
    python_callable=get_instagram,
    dag=dag,
)

morphs_task = PythonOperator(
    task_id="morphs_info",
    python_callable=morphs,
    dag=dag,
)

# Set up the task dependency
get_instagram_task >> morphs_task