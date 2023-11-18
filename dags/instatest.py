from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from pymongo import MongoClient
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import re
import ssl
import time
import random
import unicodedata
import urllib.request
import pandas as pd

random_sec= random.uniform(3,5)
driver = webdriver.Chrome()
client = MongoClient("ig-airflow-mongodb-1", 27017)
db = client["instagram_data"]
collection = db["posts"]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # 브라우저 화면 표시 안 함

def scroll_down():
    #스크롤 내리기
    last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(1.0)
        new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_page_height == last_page_height:
            time.sleep(1.0)
            if new_page_height == driver.execute_script("return document.documentElement.scrollHeight"):
                break
        else:
            last_page_height = new_page_height


def insta_id(user_id):
    url = "https://www.instagram.com/" + str(user_id)
    return url

def select_First(driver):
    first = driver.find_elements(By.CSS_SELECTOR, "div._aagw")[0]
    first.click()
    time.sleep(random_sec)

def get_content(driver):
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    
    #유저ID
    user_id = soup.select('div.x6s0dn4 h2')[0].text
    
    #본문
    try:
        content = soup.select('div._a9zs h1')[0].text
        content = unicodedata.normalize('NFC', content)
    except:
        content = ''

    #작성일자
    global date
    date = soup.select('time._aaqe')[0]['datetime'][:10]

    #종아요수
    if len(soup.select('span.html-span')) == 4:
        like = soup.select('span.html-span')[-1].text
    else:
        like = 0

    data = [user_id, content, date, like]
    return data

def move_next(driver):
    next = driver.find_element(By.CSS_SELECTOR, "button._abl- svg[aria-label=다음]")
    next.click()
    time.sleep(random_sec)


# MongoDB에 데이터를 삽입하는 함수
def insert_into_mongodb():
    # 적재할 데이터
    driver.get('https://www.instagram.com')
    time.sleep(random_sec)

    login_id = 'wnsdyd54@naver.com'
    login_pw = 'chlwns!4862'

    input_login_id = driver.find_elements(By.CSS_SELECTOR, 'input._aa4b._add6._ac4d._ap35')[0]
    input_login_id.clear()
    input_login_id.send_keys(login_id)

    input_login_pw = driver.find_elements(By.CSS_SELECTOR, 'input._aa4b._add6._ac4d._ap35')[-1]
    input_login_pw.clear()
    input_login_pw.send_keys(login_pw)
    input_login_pw.submit()

    time.sleep(random_sec)

    user_ids = ['to.gangnang','baby._.tobitori','skwhaqkqk','lovely._.yuminimi','lovelyjyeun','anvely._.22',
            '_rubi.21','harin_kong','hendel0312','choi._.maeum','hitobok_ahin','__sol.2020__v','jiyoung.lchf',
            'bring_luck_b','40_ellie','yeony_m0m','chandolmom','l___br','_torimom96','painpang','princesa_hana20',
            'woo___89','avelymami','si__a_a_','syws1473','9._.kan','dahye11_28','___j.nsa','kokoamy2011','_ye.luv_',
            'yooyoo_log','2ddu_inside','wonian_love','dh_ruri','mjmc_0323','lua_onew','20210101_jelly','chaebly_daddy',
            'p_g_y__','arin_jy','nayeon.wk','joyjoy_3_','evain425','chenvely_yun','babemini','rohee_days']

    results = []

    for user_id in user_ids:
        url = insta_id(user_id)
        driver.get(url)
        time.sleep(9)

        select_First(driver)

        while True:
            try:
                next = driver.find_element(By.CSS_SELECTOR, "button._abl- svg[aria-label=다음]")
                data = get_content(driver)
                results.append(data)
                move_next(driver)
            except:
                time.sleep(random_sec)
                data = get_content(driver)
                results.append(data)
                break
            time.sleep(random_sec)

    columns = ['user_name', 'caption', 'date', 'like_count']

    df = pd.DataFrame(results, columns=columns)

    # 데이터 삽입
    try:
        collection.insert_one(df)
    except Exception as e:
        print(f"{e}")
    else:
        print(f"Inserted: {results}")

    # MongoDB 연결 종료
    client.close()


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
    "insta_test",
    default_args=default_args,
    description="A DAG to insert unique Instagram data into MongoDB every day",
    schedule_interval=timedelta(days=1),  # 매일 한 번 실행
    start_date=datetime(2023, 11, 17),
    catchup=False,
)

# Python Operator 정의
insert_task = PythonOperator(
    task_id="insta_test",
    python_callable=insert_into_mongodb,
    dag=dag,
)

# DAG 설정
insert_task