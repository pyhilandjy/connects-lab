import time
from datetime import datetime, timedelta
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from services.selenium_tools import (get_content, insta_id, move_next,
                            select_First, initialize_webdriver)
from services.database import (crawl_to_mongo, crawl_to_mongo_daily, search_id)


options = webdriver.FirefoxOptions()
options.add_argument("--headless")  # 브라우저 화면 표시 안 함
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-setuid-sandbox")

def get_instagram(**kwargs):
    """필요 데이터 수집, 적재"""
    before_one_day = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    driver = initialize_webdriver()

    try:
        driver.get("https://www.instagram.com")
        driver.implicitly_wait(15)

        login_id = "du5694@naver.com"
        login_pw = "kang5984!!"

        input_login_id = driver.find_elements(
            By.CSS_SELECTOR, "input._aa4b._add6._ac4d._ap35"
        )[0]
        input_login_id.clear()
        input_login_id.send_keys(login_id)

        input_login_pw = driver.find_elements(
            By.CSS_SELECTOR, "input._aa4b._add6._ac4d._ap35"
        )[-1]
        input_login_pw.clear()
        input_login_pw.send_keys(login_pw)
        input_login_pw.submit()
        time.sleep(5)
        #driver.implicitly_wait(15)
        user_ids = search_id()


        results = []


        for user_id in user_ids:
            url = insta_id(user_id)
            driver.get(url)
            time.sleep(4)
            driver.implicitly_wait(15)

            try:
                select_First(driver)
                driver.implicitly_wait(15)
                data = get_content(driver)
                date = data['upload_date']
            except:
                delete_id(user_id)
                print(f"{user_id} does not exist.")
                continue

            for post in range(3):
                if date == before_one_day:
                    results.append(data)
                move_next(driver)
                driver.implicitly_wait(15)
                data = get_content(driver)
                date = data['upload_date']



            while date >= before_one_day:
                if date == before_one_day:
                    results.append(data)
                move_next(driver)
                driver.implicitly_wait(15)
                data = get_content(driver)
                date = data['upload_date']

    except Exception as e:
        print(f"driver error: {e}")
        driver.quit()

    finally:
        driver.quit()
        crawl_to_mongo(data=results)
        crawl_to_mongo_daily(data=results)
        kwargs['ti'].xcom_push(key='instagram_data', value=results)

    return results