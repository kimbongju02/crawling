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


import subprocess
from selenium.webdriver.chrome.service import Service


# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

subprocess.Popen(r'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe --remote-debugging-port=9222 --user-data-dir="E:\chromeCookie"')
#url = 
option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
driver.maximize_window()
driver.get(url)


key_word = '부산 중구 병원'  # 검색어

# css 찾을때 까지 10초대기
def time_wait(num, code):
    try:
        wait = WebDriverWait(driver, num).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code)))
    except:
        print(code, '태그를 찾지 못하였습니다.')
        driver.quit()
    return wait

# frame 변경 메소드
def switch_frame(frame):
    driver.switch_to.default_content()  # frame 초기화
    driver.switch_to.frame(frame)  # frame 변경

# 페이지 다운
def page_down(num):
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    body.click()
    for i in range(num):
        body.send_keys(Keys.PAGE_DOWN)
'''
# css를 찾을때 까지 10초 대기
time_wait(10, 'div.input_box > input.input_search')

# (1) 검색창 찾기
search = driver.find_element(By.CSS_SELECTOR, 'div.input_box > input.input_search')
search.send_keys(key_word)  # 검색어 입력
search.send_keys(Keys.ENTER)  # 엔터버튼 누르기

sleep(5)

# (2) frame 변경
switch_frame('searchIframe')
page_down(40)
sleep(5)

# 장소 리스트ㄴ
# dictionary 생성
parking_dict = {'병원정보': []}
'''
sleep(30)

print('[크롤링 시작...]')

div_1 = driver.find_element(By.ID, 'content_wrapper')
div_2 = div_1.find_element(By.CLASS_NAME, 'content')
div_3 = div_2.find_element(By.CLASS_NAME, 'at-content')
div_4 = div_3.find_element(By.ID, 'at-wrap')
div_5 = div_4.find_element(By.CLASS_NAME, 'board-list')
div_6 = div_5.find_element(By.CLASS_NAME, 'list-wrap')
div_7 = div_6.find_element(By.ID, 'fboardlist')
div_8 = div_7.find_element(By.CLASS_NAME, 'webtoon-list')
print(div_8.text)
'''
for _ in range(6):
    
    entire = len(parking_list)
    for data in range(len(parking_list)):  #장소 리스트 만큼₩
        print(data+1, '/' , entire)

        sleep(5)
        try:
            # (3) 병원 버튼 누르기
            try:
                driver.find_element(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]/ul/li[{}]/div[2]/a[1]'.format(data+1)).click()
                sleep(2)                       
            except: 
                driver.find_element(By.XPATH, '#_pcmap_list_scroll_container > ul > li:nth-child({}) > div.IPtqD > a:nth-child(1)'.format(data+1)).click()
                sleep(2)
     
            #프레임전환
            # driver.switch_to.default_content()
            switch_frame('entryIframe')
            print('프레임 전환 성공')
            sleep(5)

            # (4) 병원 이름 및 타입 가져오기
            try:
                name_and_categorie = driver.find_element(By.ID, '_title')
            except:
                name_and_categorie =driver.find_element(By.CLASS_NAME, 'zD5Nm.undefined')
            # name, categorie, phone, address = None, None, None, None
            
            #병원이름
            try:
                name = name_and_categorie.find_element(By.CLASS_NAME, 'Fc1rA').text
            except:
                name = None

            try:
                categorie = name_and_categorie.find_element(By.CLASS_NAME, 'DJJvD').text
            except:
                categorie=None

            print(name, categorie)

            # 주소
            try:
                address = driver.find_element(By.CLASS_NAME, 'PkgBl').text
            except:
                address=None


            # 전화번호
            try:
                phone = driver.find_element(By.CSS_SELECTOR, '#app-root > div > div > div > div:nth-child(5) > div > div.place_section.no_margin > div.place_section_content > div > div.O8qbU.nbXkr > div > span.xlx7Q').text
            except:
                phone = None
            
            
            # (5) 병원 운영시간 상세 버튼 누르기
            try:
                driver.find_element(By.CLASS_NAME, 'gKP9i.RMgN0').click()
                sleep(5)

                work = []
                detail = driver.find_element(By.CLASS_NAME, 'gKP9i.RMgN0')
                days = detail.find_elements(By.CLASS_NAME, 'w9QyJ')
                sleep(4)

                for day in days:
                    div_tag = day.find_element(By.CLASS_NAME, 'y6tNq')
                    detail_day = div_tag.find_element(By.TAG_NAME, 'span').text
                    work.append(detail_day)

                # 요일별 시간을 저장할 변수들 초기화
                mon, tue, wed, thu, fri, sat, sun = None, None, None, None, None, None, None
                mon_breaktime, tue_breaktime, wed_breaktime, thu_breaktime, fri_breaktime, sat_breaktime, sun_breaktime = None, None, None, None, None, None, None

                for item in work:
                    parts = item.split('\n')
                    if len(parts) > 1:
                        day = parts[0]
                        time_range = parts[1]
                        if len(parts) > 2:  # 휴게시간이 있는 경우
                            breaktime = parts[2]
                        else:
                            breaktime = None
                            
                        if '월' in day:
                            mon = time_range
                            mon_breaktime = breaktime
                            if mon_breaktime is not None:
                                mon_breaktime = re.sub(r"[ㄱ-ㅣ가-힣]", "", mon_breaktime) # 한글만 제거하기
                        elif '화' in day:
                            tue = time_range
                            tue_breaktime = breaktime
                            if tue_breaktime is not None:
                                tue_breaktime = re.sub(r"[ㄱ-ㅣ가-힣]", "", tue_breaktime) # 한글만 제거하기
                        elif '수' in day:
                            wed = time_range
                            wed_breaktime = breaktime
                            if wed_breaktime is not None:
                                wed_breaktime = re.sub(r"[ㄱ-ㅣ가-힣]", "", wed_breaktime) # 한글만 제거하기
                        elif '목' in day:
                            thu = time_range
                            thu_breaktime = breaktime
                            if thu_breaktime is not None:
                                thu_breaktime = re.sub(r"[ㄱ-ㅣ가-힣]", "", thu_breaktime) # 한글만 제거하기
                        elif '금' in day:
                            fri = time_range
                            fri_breaktime = breaktime
                            if fri_breaktime is not None:
                                fri_breaktime = re.sub(r"[ㄱ-ㅣ가-힣]", "", fri_breaktime) # 한글만 제거하기
                        elif '토' in day:
                            sat = time_range
                            sat_breaktime = breaktime
                            if sat_breaktime is not None:
                                sat_breaktime = re.sub(r"[ㄱ-ㅣ가-힣]", "", sat_breaktime) # 한글만 제거하기
                        elif '일' in day:
                            sun = time_range
                            sun_breaktime = breaktime
                            if sun_breaktime is not None:
                                sun_breaktime = re.sub(r"[ㄱ-ㅣ가-힣]", "", sun_breaktime) # 한글만 제거하기

                print("월요일 휴게시간:", mon_breaktime)
                print("월요일:", mon)
            except:
                work = None


            #프레임전환
            # driver.switch_to.default_content()
            switch_frame('searchIframe')
            sleep(5)

            # 변수를 dict에 넣기
            dict_result = {
                '병원이름': name,
                '병원종류': categorie,
                '병원주소' : address,
                '전화번호' : phone,
                '월요일': mon,
                '월요일 휴게시간': mon_breaktime,
                '화요일': tue,
                '화요일 휴게시간': tue_breaktime,
                '수요일': wed,
                '수요일 휴게시간': wed_breaktime,
                '목요일': thu,
                '목요일 휴게시간': thu_breaktime,
                '금요일': fri,
                '금요일 휴게시간': fri_breaktime,
                '토요일': sat,
                '토요일 휴게시간': sat_breaktime,
                '일요일': sun,
                '일요일 휴게시간': sun_breaktime
            }       

            parking_dict['병원정보'].append(dict_result)

            print('...완료')
        

        except Exception as e:
            print(e)
            print("!!!!!!!! ERROR !!!!!!!!")
            # 변수를 dict에 넣기
            dict_result = {
                '병원이름': name,
                '병원종류': categorie,
                '병원주소' : address,
                '전화번호' : phone,
                '월요일': mon,
                '월요일 휴게시간': mon_breaktime,
                '화요일': tue,
                '화요일 휴게시간': tue_breaktime,
                '수요일': wed,
                '수요일 휴게시간': wed_breaktime,
                '목요일': thu,
                '목요일 휴게시간': thu_breaktime,
                '금요일': fri,
                '금요일 휴게시간': fri_breaktime,
                '토요일': sat,
                '토요일 휴게시간': sat_breaktime,
                '일요일': sun,
                '일요일 휴게시간': sun_breaktime
            }    

            parking_dict['병원정보'].append(dict_result)

            print('...완료')
            sleep(1)
            
    try:
        driver.find_element(By.CSS_SELECTOR, '#app-root > div > div.XUrfU > div.zRM9F > a:nth-child(7)').click()
    except:
        try:
            driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[2]/a[7]').click()
        except:
            continue

    # parking_list = driver.find_elements(By.CSS_SELECTOR, 'li.DWs4Q')

print("데이터 수집 완료")

driver.quit()  # 작업이 끝나면 창을 닫는다.

# json 파일로 저장
file_name = './data/data_test_{}_{}.json'.format(key_word, datetime.now().strftime('%Y-%m-%d'))

with open(file_name, 'w', encoding='utf-8') as f:
    json.dump(parking_dict, f, indent=4, ensure_ascii=False, default=str)
    '''