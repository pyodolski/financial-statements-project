# Supabase 설정 가이드

## 1. Supabase 프로젝트 생성

### 1-1. 회원가입 및 로그인

1. [https://supabase.com](https://supabase.com) 접속
2. "Start your project" 클릭
3. GitHub 계정으로 로그인 (또는 이메일로 가입)

### 1-2. 새 프로젝트 생성

1. Dashboard에서 "New Project" 클릭
2. 프로젝트 정보 입력:
   - **Name**: `income-statement-converter` (원하는 이름)
   - **Database Password**: 강력한 비밀번호 생성 (저장해두세요!)
   - **Region**: `Northeast Asia (Seoul)` 선택 (한국에서 가장 빠름)
   - **Pricing Plan**: `Free` 선택
3. "Create new project" 클릭
4. 프로젝트 생성 완료까지 1-2분 대기

## 2. 데이터베이스 테이블 생성

### 2-1. SQL Editor 열기

1. 왼쪽 메뉴에서 **"SQL Editor"** 클릭
2. "New query" 클릭

### 2-2. 테이블 생성 SQL 실행

`supabase_setup.sql` 파일의 내용을 복사해서 붙여넣고 "Run" 클릭:

```sql
CREATE TABLE IF NOT EXISTS income_statements (
    id BIGSERIAL PRIMARY KEY,
    upload_filename TEXT NOT NULL,
    input_file_path TEXT NOT NULL,
    output_file_path TEXT NOT NULL,
    upload_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    total_sales NUMERIC(15, 2) NOT NULL,
    total_cost NUMERIC(15, 2) NOT NULL,
    gross_profit NUMERIC(15, 2) NOT NULL,
    deposit_amount NUMERIC(15, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_upload_date ON income_statements(upload_date DESC);

ALTER TABLE income_statements ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable read access for all users" ON income_statements
    FOR SELECT USING (true);

CREATE POLICY "Enable insert access for all users" ON income_statements
    FOR INSERT WITH CHECK (true);
```

### 2-3. 테이블 확인

1. 왼쪽 메뉴에서 **"Table Editor"** 클릭
2. `income_statements` 테이블이 생성되었는지 확인

## 3. API 키 가져오기

### 3-1. Project Settings 열기

1. 왼쪽 하단의 **⚙️ Settings** 클릭
2. **"API"** 메뉴 클릭

### 3-2. 필요한 정보 복사

다음 두 가지 정보를 복사하세요:

1. **Project URL**

   ```
   https://xxxxxxxxxxxxx.supabase.co
   ```

2. **anon public key** (API Keys 섹션에서)
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6...
   ```

⚠️ **주의**: `service_role` 키는 절대 사용하지 마세요! (보안 위험)

## 4. 환경 변수 설정

### 4-1. .env 파일 생성

프로젝트 루트 디렉토리에 `.env` 파일 생성:

```bash
# Supabase 설정
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Flask 설정
FLASK_SECRET_KEY=your-random-secret-key-here
FLASK_ENV=development
```

### 4-2. Secret Key 생성

Python으로 랜덤 키 생성:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

생성된 키를 `FLASK_SECRET_KEY`에 입력

## 5. 연결 테스트

### 5-1. 테스트 스크립트 실행

```bash
python3 -c "
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

# 테이블 조회 테스트
result = supabase.table('income_statements').select('*').execute()
print('✅ Supabase 연결 성공!')
print(f'현재 레코드 수: {len(result.data)}')
"
```

### 5-2. 성공 메시지 확인

```
✅ Supabase 연결 성공!
현재 레코드 수: 0
```

## 6. Row Level Security (RLS) 설정 (선택사항)

현재는 모든 사용자가 읽기/쓰기 가능하도록 설정되어 있습니다.
더 강력한 보안이 필요하면:

### 6-1. 인증 추가

1. Authentication 메뉴에서 사용자 인증 설정
2. RLS 정책을 사용자별로 제한

### 6-2. 정책 수정 예시

```sql
-- 자신이 업로드한 것만 볼 수 있도록
CREATE POLICY "Users can view own records" ON income_statements
    FOR SELECT USING (auth.uid() = user_id);

-- 자신만 삽입 가능
CREATE POLICY "Users can insert own records" ON income_statements
    FOR INSERT WITH CHECK (auth.uid() = user_id);
```

## 7. 데이터 확인

### 7-1. Table Editor에서 확인

1. 왼쪽 메뉴 **"Table Editor"** 클릭
2. `income_statements` 테이블 선택
3. 업로드된 데이터 확인

### 7-2. SQL로 확인

SQL Editor에서:

```sql
SELECT * FROM income_statements ORDER BY upload_date DESC;
```

## 8. 문제 해결

### 연결 오류

```
Error: Invalid API key
```

**해결**: `.env` 파일의 `SUPABASE_KEY`가 올바른지 확인

### 테이블 없음 오류

```
Error: relation "income_statements" does not exist
```

**해결**: SQL Editor에서 `supabase_setup.sql` 다시 실행

### RLS 정책 오류

```
Error: new row violates row-level security policy
```

**해결**: SQL Editor에서 정책 확인:

```sql
-- 모든 정책 보기
SELECT * FROM pg_policies WHERE tablename = 'income_statements';

-- 정책 삭제 후 재생성
DROP POLICY IF EXISTS "Enable insert access for all users" ON income_statements;
CREATE POLICY "Enable insert access for all users" ON income_statements
    FOR INSERT WITH CHECK (true);
```

## 9. 프로덕션 배포 시 주의사항

### 9-1. 환경 변수 보안

- `.env` 파일을 Git에 커밋하지 마세요
- `.gitignore`에 `.env` 추가:
  ```
  .env
  *.env
  ```

### 9-2. API 키 관리

- 프로덕션에서는 환경 변수로 관리
- Heroku: `heroku config:set SUPABASE_URL=...`
- Vercel: Settings → Environment Variables

### 9-3. 백업 설정

1. Supabase Dashboard → Settings → Database
2. "Enable automatic backups" 활성화

## 10. 무료 플랜 제한사항

Supabase 무료 플랜:

- ✅ 500MB 데이터베이스
- ✅ 1GB 파일 스토리지
- ✅ 50,000 월간 활성 사용자
- ✅ 2GB 대역폭

대부분의 개인 프로젝트에 충분합니다!

## 완료! 🎉

이제 웹 애플리케이션을 실행하면 Supabase와 연결되어 데이터가 저장됩니다.

```bash
python app.py
```

브라우저에서 `http://localhost:5000` 접속하여 테스트하세요!
