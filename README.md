# 배달 손익계산서 변환기

배민 거래 내역 Excel 파일을 손익계산서로 자동 변환하는 웹 애플리케이션입니다.

## 주요 기능

- 📊 **자동 변환**: 배민 거래 내역을 손익계산서로 자동 변환
- 📈 **월별 통계**: 거래기간 기반 월별 매출/이익 통계
- 🔄 **자동 갱신**: 동일 거래기간 데이터 자동 업데이트
- 🗑️ **자동 삭제**: 7주 후 자동 데이터 삭제
- 🔒 **관리자 페이지**: 비밀번호로 보호되는 데이터 관리
- 📥 **파일 다운로드**: 원본 파일 및 손익계산서 다운로드

## 기술 스택

- **Backend**: Flask (Python)
- **Database**: Supabase (PostgreSQL)
- **Frontend**: HTML, CSS, JavaScript
- **Excel Processing**: pandas, openpyxl

## 설치 방법

### 1. 저장소 클론

```bash
git clone <repository-url>
cd financial-statement
```

### 2. 가상환경 생성 및 활성화

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정

`.env.example` 파일을 `.env`로 복사하고 설정값을 입력하세요:

```bash
cp .env.example .env
```

`.env` 파일 내용:

```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
FLASK_SECRET_KEY=your_random_secret_key
```

### 5. Supabase 데이터베이스 설정

Supabase 대시보드의 SQL Editor에서 다음 파일들을 순서대로 실행:

1. `supabase_setup.sql` - 테이블 생성
2. `supabase_migration.sql` - 컬럼 추가 (기존 테이블이 있는 경우)

### 6. 폴더 생성

```bash
mkdir uploads outputs
```

### 7. 서버 실행

```bash
python app.py
```

서버가 http://localhost:5001 에서 실행됩니다.

## 사용 방법

### 일반 사용자

1. **파일 업로드**: 메인 페이지에서 배민 거래 내역 Excel 파일 업로드
2. **변환 확인**: 자동으로 손익계산서가 생성되고 결과 표시
3. **다운로드**: 생성된 손익계산서 다운로드
4. **이력 조회**: 변환 이력 페이지에서 과거 데이터 확인

### 관리자

1. **관리자 페이지 접속**: 상단의 "🔒 데이터 관리" 버튼 클릭
2. **비밀번호 입력**: 기본 비밀번호 `0928` 입력
3. **통계 확인**: 월별 통계 및 전체 통계 확인
4. **데이터 관리**: 데이터 목록에서 파일 다운로드 또는 삭제

## 프로젝트 구조

```
financial-statement/
├── app.py                  # Flask 메인 애플리케이션
├── income_statement.py     # 손익계산서 생성 메인 모듈
├── data_extractor.py       # Excel 데이터 추출
├── calculator.py           # 계산 로직
├── excel_generator.py      # Excel 파일 생성
├── main.py                 # CLI 버전
├── templates/              # HTML 템플릿
│   ├── index.html
│   ├── history.html
│   └── admin.html
├── static/                 # 정적 파일
│   ├── css/
│   └── js/
├── uploads/                # 업로드된 파일 (gitignore)
├── outputs/                # 생성된 손익계산서 (gitignore)
├── requirements.txt        # Python 패키지 목록
├── .env.example           # 환경 변수 예시
└── README.md              # 프로젝트 문서
```

## 주요 기능 설명

### 자동 갱신

- 동일한 거래기간의 파일을 업로드하면 기존 데이터를 자동으로 삭제하고 새 파일로 갱신

### 자동 삭제

- 업로드 후 7주(49일)가 지난 데이터는 자동으로 삭제
- 매일 자동으로 체크하며, 페이지 방문 시에도 체크

### 월별 통계

- 거래기간을 파싱하여 월별로 집계
- 총매출, 매출원가, 매출총이익, 이익률 표시

## 보안

- 관리자 페이지는 비밀번호로 보호
- 환경 변수로 민감한 정보 관리
- `.env` 파일은 Git에 포함되지 않음

## 라이선스

MIT License

## 문의

문제가 발생하거나 기능 제안이 있으시면 Issue를 등록해주세요.
