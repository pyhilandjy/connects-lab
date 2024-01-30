"""셀레니움 관련 함수"""
import random
import time
import unicodedata

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver


random_sec = random.uniform(6, 9)

def scroll_down(driver):
    """스크롤 내리기 현재 사용x"""
    last_page_height = driver.execute_script(
        "return document.documentElement.scrollHeight"
    )

    while True:
        driver.execute_script(
            "window.scrollTo(0, document.documentElement.scrollHeight);"
        )
        time.sleep(1.0)
        new_page_height = driver.execute_script(
            "return document.documentElement.scrollHeight"
        )
        if new_page_height == last_page_height:
            time.sleep(1.0)
            if new_page_height == driver.execute_script(
                "return document.documentElement.scrollHeight"
            ):
                break
        else:
            last_page_height = new_page_height


def insta_id(user_id):
    """선정된 id의 계정의 url반환"""
    url = "https://www.instagram.com/" + str(user_id)
    return url


def select_First(driver):
    """가장 위에 보이는 게시글 선택"""
    first = driver.find_elements(By.CSS_SELECTOR, "div._aagw")[0]
    first.click()
    time.sleep(random_sec)


def get_content(driver):
    """user_name, like, content, upload_date data clawring"""
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # 유저ID
    user_id = soup.select("div.x6s0dn4 h2")[0].text

    # 본문
    try:
        content = soup.select("div._a9zs h1")[0].text
        content = unicodedata.normalize("NFC", content)
    except:
        content = ""

    # 작성일자
    global date
    date = soup.select("time._aaqe")[0]["datetime"][:10]

    # 종아요수
    if len(soup.select("span.html-span")) == 4:
        like = soup.select("span.html-span")[-1].text
    else:
        like = 0

    result_dict = {
        'user_name': user_id,
        'like_count': like,
        'caption': content,
        'upload_date': date
    }
    return result_dict


def move_next(driver):
    """다음 게시물 버튼 클릭"""
    next = driver.find_element(By.CSS_SELECTOR, "button._abl- svg[aria-label=Next]")
    next.click()

def initialize_webdriver():
    """firefox 드라이버 연결"""
    firefox_options = webdriver.FirefoxOptions()
    # 웹 드라이버 초기화
    driver = webdriver.Remote(
        command_executor='http://remote_firefox:4444',  # Selenium Standalone Server 주소
        options=firefox_options,
    )
    return driver




