# 배달 손익계산서 변환기 웹 애플리케이션

배민 사장님 사이트에서 다운로드한 거래 내역을 손익계산서로 자동 변환하는 웹 서비스입니다.

## 기능

- 📤 **파일 업로드**: 드래그 앤 드롭 또는 파일 선택으로 간편 업로드
- 🔄 **자동 변환**: Excel 거래 내역을 손익계산서로 자동 변환
- 📊 **실시간 결과**: 총매출, 매출원가, 매출총이익, 입금금액 즉시 확인
- 📥 **다운로드**: 변환된 손익계산서 Excel 파일 다운로드
- 📜 **변환 이력**: 과거 변환 기록 조회 및 재다운로드
- 💾 **데이터 저장**: Supabase를 통한 안전한 데이터 관리

## 설치 방법

### 1. 가상환경 설정

```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# 또는
venv\Scripts\activate  # Windows
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. Supabase 설정

1. [Supabase](https://supabase.com)에서 프로젝트 생성
2. SQL Editor에서 `supabase_setup.sql` 실행
3. Project Settings에서 API URL과 anon key 복사

### 4. 환경 변수 설정

`.env` 파일 생성:

```bash
cp .env.example .env
```

`.env` 파일 편집:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
FLASK_SECRET_KEY=your-secret-key
FLASK_ENV=development
```

## 실행 방법

### 개발 모드

```bash
python app.py
```

브라우저에서 `http://localhost:5000` 접속

### 프로덕션 모드

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 프로젝트 구조

```
.
├── app.py                  # Flask 애플리케이션
├── income_statement.py     # 손익계산서 생성 로직
├── main.py                 # CLI 버전 (기존)
├── requirements.txt        # Python 패키지
├── .env                    # 환경 변수 (생성 필요)
├── .env.example           # 환경 변수 예시
├── supabase_setup.sql     # DB 테이블 생성 SQL
├── templates/             # HTML 템플릿
│   ├── index.html         # 메인 페이지
│   └── history.html       # 이력 페이지
├── static/                # 정적 파일
│   ├── css/
│   │   └── style.css      # 스타일시트
│   └── js/
│       └── main.js        # JavaScript
├── uploads/               # 업로드된 파일 (자동 생성)
└── outputs/               # 생성된 손익계산서 (자동 생성)
```

## API 엔드포인트

### POST /upload

파일 업로드 및 변환

**Request:**

- Content-Type: multipart/form-data
- Body: file (Excel 파일)

**Response:**

```json
{
  "success": true,
  "output_filename": "손익계산서_20241026_120000.xlsx",
  "result": {
    "total_maechul": 35153300,
    "maechul_wonka": -10115692,
    "maechul_total_iik": 25037608,
    "ipgeum_total": 21466308
  },
  "id": 1
}
```

### GET /download/<filename>

손익계산서 다운로드

### GET /history

변환 이력 페이지

### GET /api/records

전체 변환 기록 조회 (JSON)

### GET /api/record/<id>

특정 변환 기록 조회 (JSON)

## 사용 방법

1. **메인 페이지 접속**

   - 브라우저에서 `http://localhost:5000` 접속

2. **파일 업로드**

   - 배민 사장님 사이트에서 다운로드한 거래 내역 파일(.xlsx) 업로드
   - 드래그 앤 드롭 또는 파일 선택 버튼 클릭

3. **결과 확인**

   - 자동으로 변환된 손익계산서 결과 확인
   - 총매출, 매출원가, 매출총이익, 입금금액 표시

4. **다운로드**

   - "손익계산서 다운로드" 버튼 클릭
   - Excel 파일 다운로드

5. **이력 조회**
   - "변환 이력" 메뉴에서 과거 변환 기록 확인
   - 이전에 변환한 손익계산서 재다운로드 가능

## 배포

### Heroku

```bash
# Procfile 생성
echo "web: gunicorn app:app" > Procfile

# 배포
heroku create your-app-name
git push heroku main
```

### Vercel / Railway / Render

각 플랫폼의 가이드를 참고하여 Flask 앱 배포

## 문제 해결

### Supabase 연결 오류

- `.env` 파일의 SUPABASE_URL과 SUPABASE_KEY 확인
- Supabase 프로젝트가 활성화되어 있는지 확인

### 파일 업로드 오류

- 파일 크기가 16MB 이하인지 확인
- Excel 파일(.xlsx) 형식인지 확인

### 컬럼 매칭 오류

- 업로드한 파일이 배민 거래 내역 형식인지 확인
- 4행에 컬럼명이 있는지 확인

## 라이선스

MIT License

## 문의

문제가 발생하거나 개선 사항이 있으면 이슈를 등록해주세요.
