# Spotify Playlist Migrator

Spotify 플레이리스트를 YouTube 플레이리스트로 자동 이전해주는 Python 기반 GUI 프로그램입니다.

Selenium을 활용하여 Spotify 플레이리스트의 곡 정보를 수집하고, 동일한 곡들을 YouTube 플레이리스트에 자동으로 추가합니다.

---

## Features

### Spotify 플레이리스트 추출

Spotify 플레이리스트 URL을 입력하면

- 플레이리스트 이름
- 곡 제목
- 아티스트 정보

를 수집하여 CSV 파일로 저장합니다.

### YouTube 플레이리스트 자동 생성

생성된 CSV를 기반으로

- Google 계정 로그인
- YouTube 접속
- 플레이리스트 생성
- 곡 검색
- 플레이리스트 자동 저장

과정을 자동으로 수행합니다.

### GUI 지원

Tkinter 기반 인터페이스를 통해 코딩 지식 없이 사용할 수 있습니다.

---

## Workflow

```text
Spotify Playlist URL
        │
        ▼
Spotify Scraper
        │
        ▼
CSV Export
        │
        ▼
YouTube Login
        │
        ▼
Playlist Creation
        │
        ▼
Automatic Song Import
```

---

## Screenshots

### CSV 생성 모드

- Spotify 플레이리스트 URL 입력
- CSV 파일 생성

### Playlist Migration 모드

- CSV 파일 선택
- Google 계정 입력
- YouTube 플레이리스트 생성

---

## Project Structure

```text
.
├── main.py
├── scraping.py
├── auto_migrater.py
├── Searching_with_url.py
├── CSV_to_List.py
└── PlayList/
```

### main.py

GUI 진입점

기능

- Tkinter GUI 생성
- Spotify URL 입력
- CSV 생성
- YouTube 플레이리스트 이식 실행

---

### scraping.py

Spotify 플레이리스트 스크래퍼

기능

- Spotify 플레이리스트 접속
- 플레이리스트명 수집
- 곡 정보 수집
- CSV 파일 저장

출력 예시

```csv
title,artist
Shape of You,Ed Sheeran
Blinding Lights,The Weeknd
Dynamite,BTS
```

---

### CSV_to_List.py

CSV 파일을 Python 리스트로 변환

반환값

```python
titles
artists
```

---

### auto_migrater.py

Google 로그인 및 마이그레이션 실행

기능

- YouTube 접속
- Google 로그인
- 2단계 인증 처리
- 플레이리스트 생성 호출

---

### Searching_with_url.py

YouTube 플레이리스트 처리 모듈

기능

- 곡 검색
- "재생목록에 저장" 클릭
- 플레이리스트 생성
- 검색 결과 자동 추가

검색 방식

```text
아티스트 + 곡 제목 + 가사
```

예시

```text
BTS + Dynamite + 가사
```

---

## Requirements

### Python

- Python 3.9+

### Browser

- Google Chrome

### Driver

- ChromeDriver

Chrome 버전에 맞는 드라이버 설치 필요

https://chromedriver.chromium.org/

---

## Installation

### Clone Repository

```bash
git clone https://github.com/username/spotify-playlist-migrator.git

cd spotify-playlist-migrator
```

### Install Dependencies

```bash
pip install selenium
pip install pandas
```

또는

```bash
pip install -r requirements.txt
```

---

## Run

```bash
python main.py
```

---

## Usage

### 1. Spotify Playlist → CSV

1. 프로그램 실행
2. CSV Mode 선택
3. Spotify Playlist URL 입력
4. Parse 버튼 클릭
5. CSV 생성

결과

```text
PlayList/
└── My_Playlist.csv
```

---

### 2. CSV → YouTube Playlist

1. Playlist Migration Mode 선택
2. CSV 파일 선택
3. Google ID 입력
4. Google Password 입력
5. Make 버튼 클릭
6. 2단계 인증 완료
7. 플레이리스트 자동 생성

---

## Generated Files

```text
PlayList/
├── KPOP.csv
├── STUDY.csv
├── DRIVE.csv
└── FAVORITES.csv
```

---

## Known Issues

### Spotify UI 변경

Spotify의 HTML 구조가 변경될 경우 XPath 수정이 필요합니다.

### YouTube UI 변경

YouTube 메뉴 구조 변경 시 자동화 로직이 동작하지 않을 수 있습니다.

### Google 로그인 정책

Google 보안 정책 변경 시 로그인 실패 가능성이 있습니다.

### 2FA 필요

Google 2단계 인증은 사용자가 직접 완료해야 합니다.

---

## Limitations

현재 프로젝트는

- Spotify API 미사용
- YouTube Data API 미사용

방식으로 구현되어 있습니다.

모든 작업은 Selenium 기반 웹 자동화로 수행됩니다.

---

## Future Improvements

- Spotify API 연동
- YouTube Data API 연동
- OAuth 로그인
- ChromeDriver 자동 설치
- 중복 곡 검사
- 진행률 표시
- 에러 로그 저장
- 다국어 지원
- Docker 지원

---

## License

MIT License