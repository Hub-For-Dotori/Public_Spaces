import os
import csv

def get_csv_data(CSV_FILE_NAME):

    current_path = os.path.dirname(os.path.realpath(__file__))
    PlayList_path = current_path+"/PlayList/"

    titles = []
    artists = []

    f = open(f'{PlayList_path}{CSV_FILE_NAME}.csv','r')
    read = csv.reader(f)

    for row in read:
        temp = str(row)
        #==============================================
        # csv 데이터를 문자로 변화시킴
        temp = temp.replace('[','')
        temp = temp.replace(']','')
        temp = temp.replace("'",'')
        #==============================================
        # 변형 텍스트를 ,로 나누어 리스트로 변환
        temp = temp.split(',')
        #==============================================
        # 리스트에서 제목과 아티스트를 각각 저장
        titles.append(temp[0])
        artists.append(temp[1])
        #==============================================

    titles = titles[1:]
    artists = artists[1:]

    f.close()

    return titles, artists