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

options = Options()
options.add_argument("disable-blink-features=AutomationControlled")  # 자동화 탐지 방지
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 자동화 표시 제거
options.add_experimental_option('useAutomationExtension', False)  # 자동화 확장 기능 사용 안 함

Searching_Base='https://www.youtube.com/results?search_query='

LineDivider = '----------------------------------------'

def Make_PlayList(driver, PlayList_Name, Titles_List, Artists_List):
    
    wait = WebDriverWait(driver, 5)

    print(f"{LineDivider}\n저장명 : {PlayList_Name}\n\n저장 할 곡은 총 {len(Titles_List)}입니다.\n")
    
    for i in range(len(Titles_List)):
        print(f"{LineDivider}\n{i+1}번째\n제목 : {Titles_List[i]}\n아티스트 : {Artists_List[i]}\n")

    print(f"\n{LineDivider}\n\n저장을 시작합니다.\n\n{LineDivider}\n")

    for i in range(len(Titles_List)):
        if '"' in Titles_List[i] : 
            Titles_List[i] = Titles_List[i].replace('"','')
        if '"' in Artists_List[i] :
            Artists_List[i] = Artists_List[i].replace('"','')
        Searching_Url = Searching_Base + Artists_List[i] + '+' + Titles_List[i] + '+' + '가사'
        driver.get(Searching_Url)
        driver.implicitly_wait(10) # 동적 웹사이트이므로 암시적 대기 사용
        print(f"\n{LineDivider}\n 총 {len(Titles_List)} 개 중 {i+1}번째 검색 : {Titles_List[i]}\n")

        Do_more_tag = '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/div/ytd-menu-renderer/yt-icon-button/button'
        Do_more = driver.find_element(By.XPATH,Do_more_tag)
        wait.until(EC.element_to_be_clickable((By.XPATH, Do_more_tag)))  # 요소를 클릭 가능할 때까지 대기
        Do_more.click()

        #=========================================
        # 재생목록에 저장을 클릭
        Is_Selected_Saving = False
        OrderNum = 1

        print(f"{LineDivider}\n재생목록에 저장을 클릭을 시도합니다.\n")
        while Is_Selected_Saving == False:
            Do_More_List_tag = f'/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-menu-popup-renderer/tp-yt-paper-listbox/ytd-menu-service-item-renderer[{OrderNum}]/tp-yt-paper-item'
            Do_More_List = driver.find_element(By.XPATH,Do_More_List_tag)
            ListOption = Do_More_List.text
            if ListOption == '재생목록에 저장':
                wait.until(EC.visibility_of_element_located((By.XPATH, Do_More_List_tag)))  # 요소를 클릭 가능할 때까지 대기
                Do_More_List.click()
                Is_Selected_Saving = True
                OrderNum = 1
            else:
                OrderNum += 1
        print(f"{LineDivider}\n재생목록에 저장을 클릭했습니다.\n")

        
        #=========================================
        # 재생목록 선택 (추후에 이 부분을 개편하여 유저 계정에 플레이리스트가 이미 생성되고 곡이 있는 경우, 추가 곡과 대조하여 있는 경우에는 제외하고 추가 시킬 예정.)
        Is_Playlist_Exist = False
        
        try : 
            while Is_Playlist_Exist == False:
                PlayList_tag = f'/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/ytd-add-to-playlist-renderer/div[2]/ytd-playlist-add-to-option-renderer[{OrderNum}]'
                PlayList = driver.find_element(By.XPATH,PlayList_tag)
                Exist_PlayList_Name = PlayList.text
                if Exist_PlayList_Name == PlayList_Name:
                    print(f"\n재생목록을 찾았습니다.\n")
                    wait.until(EC.element_to_be_clickable((By.XPATH, PlayList_tag)))  # 요소를 클릭 가능할 때까지 대기
                    PlayList.click()
                    Is_Playlist_Exist = True
                    OrderNum = 1
                else:
                    OrderNum += 1
        except:
            print("해당 재생목록이 없습니다.\n새로 생성합니다.\n")
            Create_PlayList_tag = '/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/ytd-add-to-playlist-renderer/div[3]/ytd-button-renderer/yt-button-shape/button'
            Create_PlayList = driver.find_element(By.XPATH,Create_PlayList_tag)
            wait.until(EC.visibility_of_element_located((By.XPATH, Create_PlayList_tag)))  # 요소를 클릭 가능할 때까지 대기
            Create_PlayList.click()

            Name_Playlist_tag = '/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog[2]/yt-dialog-view-model/dialog-layout/div[2]/div[1]/div/span/yt-create-playlist-dialog-form-view-model/div[1]/text-field-view-model/textarea-shape/div/textarea'
            Name_Playlist = driver.find_element(By.XPATH,Name_Playlist_tag)
            wait.until(EC.visibility_of_all_elements_located((By.XPATH, Name_Playlist_tag)))  # 요소를 클릭 가능할 때까지 대기
            Name_Playlist.send_keys(PlayList_Name)

            Set_Showing_Playlist_tag = '/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog[2]/yt-dialog-view-model/dialog-layout/div[2]/div[1]/div/span/yt-create-playlist-dialog-form-view-model/div[2]'
            Set_Showing_Playlist = driver.find_element(By.XPATH,Set_Showing_Playlist_tag)
            wait.until(EC.visibility_of_element_located((By.XPATH, Set_Showing_Playlist_tag)))  # 요소를 클릭 가능할 때까지 대기
            Set_Showing_Playlist.click()

            Set_Public_Playlist_tag = '/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown[2]/div/yt-sheet-view-model/yt-contextual-sheet-layout/div[2]/yt-list-view-model/yt-list-item-view-model[1]'
            Set_Public_Playlist = driver.find_element(By.XPATH,Set_Public_Playlist_tag)
            wait.until(EC.visibility_of_element_located((By.XPATH, Set_Public_Playlist_tag)))  # 요소를 클릭 가능할 때까지 대기
            Set_Public_Playlist.click()

            Save_Playlist_tag = '/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog[2]/yt-dialog-view-model/dialog-layout/div[2]/div[2]/span/yt-form-footer-view-model/yt-panel-footer-view-model/div/div[2]'
            Save_Playlist = driver.find_element(By.XPATH,Save_Playlist_tag)
            wait.until(EC.visibility_of_element_located((By.XPATH, Save_Playlist_tag)))  # 요소를 클릭 가능할 때까지 대기
            Save_Playlist.click()

        print(f"{LineDivider}\n재생목록에 저장을 성공했습니다.\n")
