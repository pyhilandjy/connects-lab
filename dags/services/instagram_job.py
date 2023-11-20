import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dags.services.selenium_tools import (get_content, insta_id, move_next,
                            random_sec, select_First)
from dags.services.database import insert_to_mongo

options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # 브라우저 화면 표시 안 함
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-setuid-sandbox")

def get_instagram():
    

    remote_webdriver = 'http://172.25.0.5:4444/wd/hub'

    """셀레니움으로 수집, 적재"""
    with webdriver.Remote(remote_webdriver, options=options) as driver:
        driver.get("https://www.instagram.com")
        time.sleep(random_sec)

        login_id = "wnsdyd54@naver.com"
        login_pw = "chlwns!4862"

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

        time.sleep(random_sec)

        user_ids = [
            "to.gangnang",
            # "baby._.tobitori",
            # "skwhaqkqk",
            # "lovely._.yuminimi",
            # "lovelyjyeun",
            # "anvely._.22",
            # "_rubi.21",
            # "harin_kong",
            # "hendel0312",
            # "choi._.maeum",
            # "hitobok_ahin",
            # "__sol.2020__v",
            # "jiyoung.lchf",
            # "bring_luck_b",
            # "40_ellie",
            # "yeony_m0m",
            # "chandolmom",
            # "l___br",
            # "_torimom96",
            # "painpang",
            # "princesa_hana20",
            # "woo___89",
            # "avelymami",
            # "si__a_a_",
            # "syws1473",
            # "9._.kan",
            # "dahye11_28",
            # "___j.nsa",
            # "kokoamy2011",
            # "_ye.luv_",
            # "yooyoo_log",
            # "2ddu_inside",
            # "wonian_love",
            # "dh_ruri",
            # "mjmc_0323",
            # "lua_onew",
            # "20210101_jelly",
            # "chaebly_daddy",
            # "p_g_y__",
            # "arin_jy",
            # "nayeon.wk",
            # "joyjoy_3_",
            # "evain425",
            # "chenvely_yun",
            # "babemini",
            # "rohee_days",
        ]

        results = []
        for user_id in user_ids:
            url = insta_id(user_id)
            driver.get(url)
            time.sleep(9) # TODO

            select_First(driver)

            n = 0
            while True:
                try:
                    next = driver.find_element(
                        By.CSS_SELECTOR, "button._abl- svg[aria-label=다음]"
                    )
                    data = get_content(driver)
                    results.append(data)
                    move_next(driver)
                except:
                    time.sleep(random_sec)
                    data = get_content(driver)
                    results.append(data)
                    break
                time.sleep(random_sec)

                n += 1
                if n == 1:
                    break


    # columns = ['user_name', 'caption', 'date', 'like_count']

    # df = pd.DataFrame(results, columns=columns)

    # 중복된거 있는지 제거하는 로직 여기에다가 python collections 찾아보면 나올거임

    insert_to_mongo(data=results)


if __name__ == '__main__':
    get_instagram()