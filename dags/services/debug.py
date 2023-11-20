import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from dags.services.selenium_tools import (get_content, insta_id, move_next,
#                             random_sec, select_First)
# from dags.services.database import insert_to_mongo


options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # 브라우저 화면 표시 안 함
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-setuid-sandbox")


remote_webdriver = 'http://172.25.0.5:4444/wd/hub'


with webdriver.Remote(remote_webdriver, options=options) as driver:
    driver.get("https://n.news.naver.com/mnews/article/005/0001606450")
    a = main(driver)
    print(a)