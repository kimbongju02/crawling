import json
import time
from time import sleep
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException


import subprocess
from selenium.webdriver.chrome.service import Service

name_path = '#_title > div > span:nth-child(1)'
kind_path = '#_title > div > span:nth-child(2)'
address_path = '#app-root > div > div > div > div:nth-child(5) > div > div.place_section.no_margin > div.place_section_content > div > div:nth-child(1) > div > a > span'
workTime_path = '#app-root > div > div > div > div:nth-child(5) > div > div.place_section.no_margin > div.place_section_content > div > div:nth-child(3) > div > a'
workTime_path_v2 = '#app-root > div > div > div > div:nth-child(5) > div > div.place_section.no_margin > div.place_section_content > div > div:nth-child(2) > div > a'
phone_path = '#app-root > div > div > div > div:nth-child(5) > div > div.place_section.no_margin > div.place_section_content > div > div:nth-child(4) > div > span'
phone_path_v2 = '#app-root > div > div > div > div:nth-child(5) > div > div.place_section.no_margin > div.place_section_content > div > div:nth-child(3) > div > span'

json_file_name = "hospital_v2.json"
def load_hospital_json():
    with open(json_file_name, "r", encoding="utf-8") as file_data:
        result = json.load(file_data)
    return result

def save_toJson(crawling_data):
    import json
    json_file_name = "crawling_on_hospital.json"
    
    with open(json_file_name, "r", encoding="utf-8") as file_data:
        result = json.load(file_data)
        result.append(crawling_data)
    with open(json_file_name, "w", encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)

# css 찾을때 까지 10초대기
def time_wait(code):
    try:
        return WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code))
        )
    except:
        print(code, '태그를 찾지 못하였습니다.')
        driver.quit()

# frame 변경 메소드
def switch_frame(frame):
    driver.switch_to.default_content()  # frame 초기화
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, frame))  # 프레임이 로드될 때까지 대기하고 전환
    )

# 페이지 다운
def page_down(num):
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    body.click()
    for i in range(num):
        body.send_keys(Keys.PAGE_DOWN)

def crawling(search_key):
    print("===================", search_key,"=======================")

    driver.switch_to.default_content()  # frame 초기화
    # css를 찾을때 까지 10초 대기
    time_wait('div.input_box > input.input_search')

    # (1) 검색창 찾기
    search = time_wait('#home_search_input_box > div > div > div > input')
    search.send_keys(Keys.CONTROL, 'a', Keys.BACKSPACE)
    search.send_keys(search_key)
    search.send_keys(Keys.ENTER)
    sleep(5)
    
    switch_frame('searchIframe')
    
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#_pcmap_list_scroll_container > ul > li:first-child > div > div:last-child > a:nth-child(1)'))
        )
        element.click()
        switch_frame('entryIframe')
        result = craw_data()
    except TimeoutException as e:
        return "key"
    except Exception as e:
        switch_frame('entryIframe')
        result = craw_data()

    print(result)
    return result

def craw_data():
    try:
        name = driver.find_element(By.CSS_SELECTOR, name_path).text
    except Exception as e:
        name = ""
    try:
        kind = driver.find_element(By.CSS_SELECTOR, kind_path).text
        if kind =="요양병원":
            print("요양병원")
            return False
    except Exception as e:
        kind = ""
    try:
        address = driver.find_element(By.CSS_SELECTOR, address_path).text
    except Exception as e:
        address = ""
    try:
        phone = driver.find_element(By.CSS_SELECTOR, phone_path).text
    except Exception as e:
        phone = ""
    try:
        time_a_element = driver.find_element(By.CSS_SELECTOR, workTime_path)
        time_a_element.click()
        work_time = time_a_element.find_elements(By.CSS_SELECTOR, 'div')
    except NoSuchElementException as e:
        print("time_a_element NoSuchElementException")
        try:
            phone = driver.find_element(By.CSS_SELECTOR, phone_path_v2).text
        except Exception as e:
            phone = ""
        time_a_element = driver.find_element(By.CSS_SELECTOR, workTime_path_v2)
        time_a_element.click()
        work_time = time_a_element.find_elements(By.CSS_SELECTOR, 'div')
    except Exception as e:
        print("time_a_element Exception")
    work_time_list = []
        
    sig_text=""
    for i in work_time:
        try:
            day_element = i.find_element(By.CSS_SELECTOR, 'div > span > span')
            day = day_element.text if day_element else "N/A"
            if day==sig_text:
                continue
            sig_text = day
            t_element = i.find_element(By.CSS_SELECTOR, 'div > span > div')
            t = t_element.text if t_element else "N/A"
            
            
            t_split = t.split('\n')
            time_json = {}

            # 추출한 값 출력
            for i, val in enumerate(t_split):
                time_json[i] = val
                
            work_time_list.append(
                {
                    "요일": day,
                    "시간": time_json,
                }
            )
        except Exception as e:
            print("for i in work_time error")
    
    result={
        '의료기관명':name,
        '의료기관종별':kind,
        '의료기관주소':address,
        '전화번호': phone,
        '근무시간': work_time_list
    }
    
    if "부산진구" not in result['의료기관주소']:
        print("부산진구 아님")
        return False
    else:
        return result

if __name__ == "__main__":
    # 브라우저 꺼짐 방지 옵션
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    url = 'https://map.naver.com/v5/search'
    driver = webdriver.Chrome()
    driver.get(url)

    hospital_info = load_hospital_json()
    log = "권혁진이비인후과의원"
    sig = True
    for i in hospital_info:
        if i['의료기관명']==log:
            sig = False
        if sig:
            continue
        search_key = f"{i['의료기관명']}, {i['의료기관주소']}"
        result = crawling(search_key)
        if result == "key":
            result = crawling(i['의료기관명'])
        if not result:
            continue
        save_toJson(result)
        
        # 춘해병원 데이터 이상해