# Vercel 배포 가이드

## Vercel이란?

Vercel은 서버리스 플랫폼으로, Flask 앱을 쉽게 배포할 수 있습니다.

- ✅ 무료 플랜 제공
- ✅ 자동 HTTPS
- ✅ 글로벌 CDN
- ✅ GitHub 자동 배포
- ⚠️ 서버리스 환경 (파일 시스템 제한)

## 빠른 배포 (5분)

### 1. Vercel 계정 생성

https://vercel.com 에서 GitHub 계정으로 가입

### 2. Vercel CLI 설치 (선택사항)

```bash
npm install -g vercel
```

### 3. GitHub에 코드 푸시

```bash
git add .
git commit -m "Add Vercel configuration"
git push origin main
```

### 4. Vercel에서 배포

#### 방법 A: 웹 대시보드 (추천)

1. Vercel 대시보드 접속
2. **New Project** 클릭
3. GitHub 저장소 선택
4. **Environment Variables** 추가:
   - `SUPABASE_URL`: Supabase 프로젝트 URL
   - `SUPABASE_KEY`: Supabase anon key
   - `FLASK_SECRET_KEY`: 랜덤 문자열
5. **Deploy** 클릭
6. 완료! 🎉

#### 방법 B: CLI

```bash
vercel

# 환경 변수 추가
vercel env add SUPABASE_URL
vercel env add SUPABASE_KEY
vercel env add FLASK_SECRET_KEY

# 배포
vercel --prod
```

## 중요 사항

### 파일 저장소 제한

Vercel은 서버리스 환경이므로:

- 업로드된 파일은 `/tmp` 디렉토리에 저장됩니다
- 함수 실행이 끝나면 파일이 삭제될 수 있습니다
- **해결책**: 파일을 Supabase Storage나 AWS S3에 저장하는 것을 권장

### Cron Job 설정

자동 삭제 기능은 Vercel Cron을 사용합니다:

- `vercel.json`에 이미 설정되어 있음
- 매일 자정(UTC)에 실행
- Pro 플랜에서만 사용 가능 (무료 플랜은 수동 실행)

### 무료 플랜 제한

- 함수 실행 시간: 10초
- 메모리: 1024MB
- 대역폭: 100GB/월
- Cron Job: Pro 플랜만 가능

## 파일 저장소 개선 (권장)

Vercel의 파일 시스템 제한을 해결하려면 Supabase Storage를 사용하세요:

### 1. Supabase Storage 설정

```python
# storage_helper.py
from supabase import create_client
import os

supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

def upload_file(file_path, bucket_name='uploads'):
    """파일을 Supabase Storage에 업로드"""
    with open(file_path, 'rb') as f:
        file_data = f.read()

    file_name = os.path.basename(file_path)
    response = supabase.storage.from_(bucket_name).upload(file_name, file_data)
    return response

def download_file(file_name, bucket_name='uploads'):
    """Supabase Storage에서 파일 다운로드"""
    response = supabase.storage.from_(bucket_name).download(file_name)
    return response
```

### 2. app.py 수정

```python
# 파일 업로드 후
upload_file(input_path, 'uploads')
upload_file(output_path, 'outputs')

# 파일 다운로드 시
file_data = download_file(filename, 'outputs')
```

## 배포 후 확인

### 1. 웹사이트 접속

```
https://your-project.vercel.app
```

### 2. 로그 확인

```bash
vercel logs
```

### 3. 환경 변수 확인

```bash
vercel env ls
```

## 커스텀 도메인 연결

1. Vercel 대시보드 → Settings → Domains
2. 도메인 입력 (예: `myapp.com`)
3. DNS 설정 (Vercel이 안내)
4. 완료!

## 문제 해결

### "Module not found" 에러

- `requirements.txt`에 모든 패키지가 포함되어 있는지 확인
- Vercel 빌드 로그 확인

### "Function timeout" 에러

- 파일 처리 시간이 10초를 초과하는 경우
- Pro 플랜으로 업그레이드 (60초)
- 또는 Railway/Render 사용 권장

### 파일이 사라지는 문제

- `/tmp` 디렉토리는 임시 저장소
- Supabase Storage 사용 권장

### Cron Job이 작동하지 않음

- 무료 플랜에서는 Cron 사용 불가
- Pro 플랜으로 업그레이드
- 또는 외부 Cron 서비스 사용 (cron-job.org)

## Vercel vs 다른 플랫폼

| 기능        | Vercel | Railway | Render | Heroku |
| ----------- | ------ | ------- | ------ | ------ |
| 무료 플랜   | ✅     | ✅      | ✅     | ✅     |
| 파일 저장   | ❌     | ✅      | ✅     | ✅     |
| Cron Job    | 💰     | ✅      | ✅     | 💰     |
| 배포 속도   | ⚡️    | ⚡️     | 🐢     | 🐢     |
| 설정 난이도 | 쉬움   | 쉬움    | 보통   | 보통   |

**추천:**

- 간단한 앱: Vercel ✅
- 파일 업로드 많음: Railway 또는 Render ✅
- 프로덕션: Railway (유료) 또는 AWS ✅

## 대안 플랫폼

파일 저장소가 중요하다면:

### Railway (추천)

```bash
# Railway CLI 설치
npm install -g @railway/cli

# 로그인
railway login

# 배포
railway up
```

### Render

- 웹 대시보드에서 배포
- 파일 시스템 지원
- 무료 플랜 제공

## 추가 리소스

- [Vercel 문서](https://vercel.com/docs)
- [Flask on Vercel](https://vercel.com/guides/using-flask-with-vercel)
- [Supabase Storage](https://supabase.com/docs/guides/storage)
