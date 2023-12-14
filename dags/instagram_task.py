from datetime import datetime, timedelta
from konlpy.tag import *

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from services.instagram_job import get_instagram
from services.morphs_job import morphs, split_data,update_json_file
from services.database import pull_daily_mongo

data = pull_daily_mongo()

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
    "insta_morphs",
    default_args=default_args,
    description="daily morphs instagram caption",
    schedule_interval='@daily',
    start_date=datetime(2023, 11, 30),
    catchup=False,
)

# Python Operator 정의
get_instagram_task = PythonOperator(
    task_id="get_instagram_info",
    python_callable=get_instagram,
    dag=dag,
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
        task_id=f"morphs_{i}",
        python_callable=morphs,
        op_args=[variable_name],
        provide_context=True,
        dag=dag,
    )

    split_data_task >> morphs_task
    morphs_tasks.append(morphs_task)

update_json_file_task = PythonOperator(
    task_id="update_json_file_task",
    python_callable=update_json_file,
    provide_context=True,
    dag=dag,
)

# Set up the task dependency
get_instagram_task >> split_data_task >> morphs_tasks >> update_json_file_task

