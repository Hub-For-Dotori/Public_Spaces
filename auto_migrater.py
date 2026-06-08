from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time
import argparse

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from selenium.webdriver.chrome.options import Options

import CSV_to_List
import Searching_with_url


options = Options()
options.add_argument("disable-blink-features=AutomationControlled")  # 자동화 탐지 방지
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 자동화 표시 제거
options.add_experimental_option('useAutomationExtension', False)  # 자동화 확장 기능 사용 안 함

def GoogleLogin(YouTube_Link,id,pw):
    
    print("유튜브 접속 중..\n")
    #=====================================================
    # 1단계 로그인
    #=====================================================
    driver = webdriver.Chrome(options=options)
    driver.get(YouTube_Link)
    wait = WebDriverWait(driver, 5)
    driver.implicitly_wait(10) # 동적 웹사이트이므로 암시적 대기 사용
    print("유튜브 접속 완료!\n")

    Login_tag = '//*[@id="buttons"]/ytd-button-renderer/yt-button-shape/a'
    Login = driver.find_element(By.XPATH,Login_tag)
    wait.until(EC.element_to_be_clickable((By.XPATH, Login_tag)))  # 요소를 클릭 가능할 때까지 대기
    Login.click()

    IdInput_tag = '//*[@id="identifierId"]'
    IdInput = driver.find_element(By.XPATH, IdInput_tag)
    wait.until(EC.visibility_of_element_located((By.XPATH, IdInput_tag)))  # 요소를 클릭 가능할 때까지 대기
    IdInput.send_keys(id)
    IdInput.send_keys(Keys.ENTER)

    OtherWay_tag = '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div[2]/div/div/button'
    wait.until(EC.element_to_be_clickable((By.XPATH, OtherWay_tag)))  # 요소를 클릭 가능할 때까지 대기
    OtherWay = driver.find_element(By.XPATH, OtherWay_tag).click()

    Login_to_PW_tag = '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div/div/form/span/section[2]/div/div/section/div/div/div/ul/li[2]'
    wait.until(EC.element_to_be_clickable((By.XPATH, Login_to_PW_tag)))  # 요소를 클릭 가능할 때까지 대기
    Login_to_PW = driver.find_element(By.XPATH, Login_to_PW_tag).click()

    PWInput_tag = '//*[@id="password"]/div[1]/div/div[1]/input'
    PWInput = driver.find_element(By.XPATH, PWInput_tag)
    wait.until(EC.visibility_of_element_located((By.XPATH, PWInput_tag)))  # 요소를 클릭 가능할 때까지 대기
    PWInput.send_keys(pw)

    Login_Btn_tag = '//*[@id="passwordNext"]/div/button'
    wait.until(EC.element_to_be_clickable((By.XPATH, Login_Btn_tag)))  # 요소를 클릭 가능할 때까지 대기
    Login_Btn = driver.find_element(By.XPATH, Login_Btn_tag).click()
    #=====================================================
    # 2단계 로그인
    #=====================================================
    try :
        Press_OK_in_Phone_tag = '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div/div/form/span/section[3]/div/div/section/div/div/div/ul/li[2]/div'
        Press_OK_in_Phone = driver.find_element(By.XPATH, Press_OK_in_Phone_tag).click()
    except:
        PassKey_tag = '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div/div/form/span/section[3]/div/div/section/div/div/div/ul/li[1]/div'
        PassKey = driver.find_element(By.XPATH, PassKey_tag).click()

    print("인증 해주십시오.")

    while(YouTube_Link != driver.current_url):
        driver.implicitly_wait(10) # 동적 웹사이트이므로 암시적 대기 사용

    print("로그인 완료!")
    
    return driver
    #=====================================================
    
def migrate_to_youtube(id,pw,PlayList_File_Name):

    #=====================================================
    # 제목과 아티스트 가져오기
    Title_List, Artists_List = CSV_to_List.get_csv_data(PlayList_File_Name)
    print("CSV 변환 완료!")
    #=====================================================
    # 로그인 시도

    print(f"로그인 시도 중입니다.\n")

    YouTube_Link = 'https://www.youtube.com/'
    
    driver = GoogleLogin(YouTube_Link,id,pw)

    #=====================================================
    # 플레이 리스트 이식
    Searching_with_url.Make_PlayList(driver, PlayList_File_Name,Title_List,Artists_List)

    print("플레이 리스트 이식 완료!")

    driver.close()