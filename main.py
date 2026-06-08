import os

import scraping
import auto_migrater
import CSV_to_List

from tkinter import *
import tkinter.ttk as ttk


current_path = os.path.dirname(os.path.realpath(__file__))
print(f'\n\n현재 경로 : {current_path}\n\n')

PlayList_path = current_path+"/PlayList/"

if (os.path.exists(PlayList_path)==True):
    print("플레이리스트 폴더가 존재 합니다.")
else: 
    print("플레이리스트 폴더가 없습니다.\n자동으로 폴더를 생성합니다.")
    os.mkdir(PlayList_path)

print(f'\n\n현재 플레이리스트 폴더의 위치 : {PlayList_path}\n\n')

page = 1  # CSV_frame는 1, Make_Playlist_frame이 2임.
def change_frame():
    global page, CSV_frame, Make_Playlist_frame
    if page == 2:
        Make_Playlist_frame.lift()
        page = 1
    elif page == 1:
        CSV_frame.lift()
        page = 2

#============================================
# GUI 설정
#============================================

tk = Tk()

tk.title("스포티파이 플레이리스트 이식")
tk.geometry("400x300+300+300")

CSV_frame = Frame(tk, relief='solid', border=2)
CSV_frame.place(x=0, y=0, width=400, height=250) 

Make_Playlist_frame = Frame(tk, relief='solid', border=2)
Make_Playlist_frame.place(x=0, y=0, width=400, height=250) # 이 프레임이 가장 먼저 나타남

but_frame = Frame(tk, relief='solid', border=2)
but_frame.place(x=0, y=250, width=400, height=50)  # 밑 바닥에 이전과 다음이 있을 버튼 영역

#============================================
# Make_Playlist_frame
#============================================

def MakePlaylist():
    Id = IdBox.get()
    Pw = PwBox.get()
    PlayList_File_Name = PlayList_File_list_comboBox.get().replace(".csv","")
    print(f"ID : {Id}")
    print(f"PW : {len(Pw)*"*"}")
    print(f"CSV 파일 : {PlayList_File_Name}\n\n")
    try:
        CSV_to_List.get_csv_data(PlayList_File_Name)
        auto_migrater.migrate_to_youtube(Id,Pw,PlayList_File_Name)
    except:
        print("CSV 파일을 읽어오는 중이거나 플레이리스트 이식에서 오류가 발생했습니다.")
        return


#============================================
# 모드 제목
Label(Make_Playlist_frame, text="Migrate playlist", font= ('bold',20)).grid(row=0, column=1)
Label(Make_Playlist_frame, text="").grid(row=1, column=0)

#============================================
# CSV 파일 목록 상자
current_path = os.path.dirname(os.path.realpath(__file__))
PlayList_path = current_path+"/PlayList/"
PlayList_File_list = os.listdir(PlayList_path)
print(f'\n\n현재 플레이리스트 폴더 속 파일 이름 : {PlayList_File_list}\n\n')

PlayList_File_list_comboBox = ttk.Combobox(Make_Playlist_frame)
PlayList_File_list_comboBox.config(values=PlayList_File_list, state="readonly")
PlayList_File_list_comboBox.set("CSV 파일 목록")
PlayList_File_list_comboBox.grid(row=2, column=1)
Label(Make_Playlist_frame, text="").grid(row=3, column=0)
#============================================
# ID 입력창
Label(Make_Playlist_frame, text="ID").grid(row=4, column=0)
IdBox = Entry(Make_Playlist_frame)
IdBox.grid(row=4, column=1)

#============================================
# PW 입력창
Label(Make_Playlist_frame, text="pw").grid(row=5, column=0)
PwBox = Entry(Make_Playlist_frame, show="*")
PwBox.grid(row=5, column=1)

#============================================
# 플레이리스트 생성 버튼
Make_Btn = Button(Make_Playlist_frame, text='Make',background='grey',foreground="black",command=MakePlaylist).grid(row=6,column=2)

#============================================
# CSV_frame
#============================================

def CSV():
    url = URLBox.get()
    print(url)
    try:
        if (url == ""):
            print("URL을 입력해주세요.")
            return
        if (url.find("spotify") == -1):
            print("스포티파이 링크가 아닙니다.")
            return
        if (url.find("playlist") == -1):
            print("플레이리스트가 아닙니다.")
            return
        else:
            scraping.scraping(url,PlayList_path)
    except:
        print("URL을 읽어오는 중 오류가 발생했습니다.")
        return
#============================================

Label(CSV_frame, text="Parse Spotify Playlist", font= ('bold',20)).grid(row=0, column=1)
Label(CSV_frame, text="").grid(row=1, column=0)

#============================================
# URL 입력창
Label(CSV_frame, text="URL").grid(row=2, column=0)
URLBox = Entry(CSV_frame)
URLBox.grid(row=2, column=1)

#============================================
# CSV 저장 버튼
CSV_Btn = Button(CSV_frame, text='CSV',background='grey',foreground="black",command=CSV).grid(row=3,column=2)
#============================================



#============================================
# 모드 버튼
#============================================

Button(but_frame, text='모드 전환', command=change_frame).pack(side='right')

tk.mainloop()
