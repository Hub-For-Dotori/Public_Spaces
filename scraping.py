import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time
import argparse

from selenium.webdriver.common.action_chains import ActionChains


def scraping(spotify_playlist_url, PlayList_path):

    driver = webdriver.Chrome('') #should use r in the behind of the path
    driver.get(spotify_playlist_url)
    driver.implicitly_wait(10) # because this is a dynamic website we need to used this implicitly_wait() function
    time.sleep(3)

    print(f'\n\n접속한 주소 : {spotify_playlist_url}\n\n')
    
    PlayListBody = driver.find_element(By.XPATH,'//*[@id="main"]/div/div[2]/div[5]/div/div[2]/div[1]/div/main/section/div[2]/div[3]/div/div[1]/div/div[2]')
    ScrollBody = driver.find_element(By.XPATH,'//*[@id="main"]/div/div[2]/div[5]/div/div[2]/div[1]/div/main/section/div[2]/div[3]/div/div[1]/div')
    
    print("플레이 리스트의 개수를 계산합니다..\n\n")

    Full_height = PlayListBody.value_of_css_property('height')
    Full_height = int(Full_height.replace('px',''))

    ListBoxHeight = 56
    ListCnt = Full_height//ListBoxHeight-1
    print(f"전체 리스트 : {ListCnt}개\n\n")

    # Now that all data is loaded, scrape it

    #//*[@id="main"]/div/div[2]/div[5]/div/div[2]/div[1]/div/main/section/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/div/a/div
  
    all_data = []

    PlayListName_tag = '//*[@id="main"]/div/div[2]/div[5]/div/div[2]/div[1]/div/main/section/div[1]/div[3]/div[3]/span[2]/h1'
    PlayListName = driver.find_element(By.XPATH,PlayListName_tag)
    output_csv = PlayListName.text
    output_csv = output_csv.replace(" ","_")
    
    ActionChains(driver).move_to_element(PlayListName).double_click().perform()
    ActionChains(driver).move_to_element(PlayListName).double_click().perform()

    print(f'플레이 리스트 이름 : {output_csv}')

    CurrentListBody_tag = '//*[@id="main"]/div/div[2]/div[5]/div/div[2]/div[1]/div/main/section/div[2]/div[3]/div/div[1]/div/div[2]/div[2]'
    
    index = 1 # 시스템에서 가져올 번째 : XPATH에서는 순서가 1씩 증가함. 하지만, 일정 개수가 넘어가면 파싱 중 순서가 바뀌어 제대로 못 긁어옴.
    currnet_getting_order = index # 현재 불러와야 하는 순서 : 흐름 제어용으로 사용
    
    while (True):
        if(currnet_getting_order>ListCnt): # 모두 긁어온 경우
            print(f"총 {ListCnt} 중 {len(all_data)}")
            print("스캔을 정상적으로 마칩니다.")
            break

        OrderListBox_tag=f'//*[@id="main"]/div/div[2]/div[5]/div/div[2]/div[1]/div/main/section/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div[{index}]'
        
        OrderNum = int(driver.find_element(By.XPATH,OrderListBox_tag).get_attribute("aria-rowindex"))-1 #플레이 리스트 순번.
        
        if (currnet_getting_order!=OrderNum):
            Interval = OrderNum - currnet_getting_order #순서와 현재 시스템에서의 순번의 간격 저장         
            index = index - Interval #간격을 인덱스에 반영하여 오류 해결
            '''
            print(f'현재 들어와야할 값 : {currnet_getting_order}')
            print(f'시스템의 순번과 불러와야하는 순번 차이가 발생합니다.\n차이 값 : {Interval}')
            print(f'수정된 인덱스 값 : {index}')
            '''
        else : 
            print(f'start {OrderNum}..')

            Title_tag=f'//*[@id="main"]/div/div[2]/div[5]/div/div[2]/div[1]/div/main/section/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div[{index}]/div/div[2]/div/a/div'
            Artist_tag=f'//*[@id="main"]/div/div[2]/div[5]/div/div[2]/div[1]/div/main/section/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div[{index}]/div/div[2]/div/span/div/a'
            

            title = driver.find_element(By.XPATH,Title_tag)
            artist = driver.find_element(By.XPATH,Artist_tag)
            
            
            ActionChains(driver).move_to_element(title).perform()


            print(f"{OrderNum}/{ListCnt}")
            print(f"제목 : {title.text}")
            print(f"가수 : {artist.text}\n=====")
            all_data.append({
                "title": title.text,
                "artist": artist.text,
            })
            title = None
            artist = None

            currnet_getting_order += 1 #현재 시스템에서 인식하는 가져올 값.
            index = index + 1
        
    print("CSV 변환 완료!")
    df = pd.DataFrame(data=all_data)
    df.to_csv(f'{PlayList_path}{output_csv}.csv', index=False)

    driver.close()

# getData("https://open.spotify.com/playlist/0L39AS9Z3C8A8Pt0YZvT9p", "playlist.csv")

if __name__ == "__main__":

# Initialize parser
    parser = argparse.ArgumentParser()
    
    # Adding optional argument
    parser.add_argument("-u", "--url", help = "file path of your dataset")
    
    # Read arguments from command line
    args = parser.parse_args()

    scraping(args.url)