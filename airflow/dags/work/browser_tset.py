from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import pymongo
import math
import time
from datetime import datetime, timedelta
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from services.selenium_tools import (get_content, insta_id, move_next,
                            select_First)
from services.database import (crawl_to_mongo, crawl_to_mongo_daily, search_id)


options = webdriver.FirefoxOptions()
options.add_argument("--headless")  # 브라우저 화면 표시 안 함
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-setuid-sandbox")

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

def initialize_webdriver(port, con_num):
    # 4444, 4445, 4446
    """firefox 드라이버 연결"""
    firefox_options = webdriver.FirefoxOptions()
    # 웹 드라이버 초기화
    driver = webdriver.Remote(
        command_executor=f'http://remote_firefox-{con_num}:{port}',  # Selenium Standalone Server 주소
        options=firefox_options,
    )
    return driver

def crawl_instagram(user_names, port, con_num):
    driver = initialize_webdriver(port, con_num)
    try:
        driver.get(user_names)
        time.sleep(60)
        print(user_names)
    finally:
        driver.quit()

jobs = [{"port":"4444","con_num": "1", "user_names":"https://www.naver.com"},
        {"port":"4445","con_num": "2", "user_names":"https://www.google.com"},
        {"port":"4446","con_num": "3", "user_names":"https://www.instagram.com"}]

dag = DAG(
    'browser_test',
    default_args=default_args,
    description='initialize_webdriver123',
    schedule_interval=timedelta(days=1),
)

for idx, job in enumerate(jobs):
    # chunk = usernames[i*chunk_size:(i+1)*chunk_size]
    task = PythonOperator(
        task_id=f'process_usernames_{idx+1}',
        python_callable=crawl_instagram,
        op_kwargs={'user_names': job["user_names"], 'con_num': job["con_num"], 'port': job["port"]},
        dag=dag,
    )

# def initialize_webdriver(session_id=None):
#     """firefox 드라이버 연결"""
#     firefox_options = webdriver.FirefoxOptions()
#     capabilities = {
#         "browserName": "firefox",
#         "moz:firefoxOptions": {
#             "args": [],
#             "log": {"level": "trace"},
#         },
#     }
#     if session_id:
#         capabilities["moz:firefoxOptions"]["args"].append(f"--sessionId={session_id}")

#     # 웹 드라이버 초기화
#     driver = webdriver.Remote(
#         command_executor='http://remote_firefox:4444',  # Selenium Standalone Server 주소
#         options=firefox_options,
#     )
#     return driver


# # def initialize_webdriver(session_id, con_num):
# #     # 4444, 4445, 4446
# #     """firefox 드라이버 연결"""
# #     print("session_id:", session_id)
# #     firefox_options = webdriver.FirefoxOptions()
# #     # 웹 드라이버 초기화
# #     driver = webdriver.Remote(
# #         command_executor=f'http://remote_firefox:{port}',  # Selenium Standalone Server 주소
# #         options=firefox_options,
# #     )
# #     return driver

# def crawl_instagram(user_names, session_id):
#     driver = initialize_webdriver(session_id)
#     driver.get(user_names)
#     print(user_names)

# dag = DAG(
#     'browser_test',
#     default_args=default_args,
#     description='initialize_webdriver 123',
#     schedule_interval=timedelta(days=1),
# )
# #port_nums = [4444, 4445, 4446]

# # 여기서 유저 네임 자르는 작업을 함 (시작)
# user_name_list_1 = "https://www.naver.com"
# user_name_list_2 = "https://www.google.com"
# user_name_list_3 = [7,8,9]
# # 여기서 유저 네임 자르는 작업을 함 (끝)
# # ,{"port":4446,"user_names": user_name_list_3, "con_num":3}
# jobs = [{"session_id":"c1","user_names": user_name_list_1},{"session_id":"c2","user_names": user_name_list_2}]

# for idx, job in enumerate(jobs):
#     # chunk = usernames[i*chunk_size:(i+1)*chunk_size]
#     task = PythonOperator(
#         task_id=f'process_usernames_{idx+1}',
#         python_callable=crawl_instagram,
#         op_kwargs={'user_names': job["user_names"], 'session_id': job["session_id"]},
#         dag=dag,
#     )

