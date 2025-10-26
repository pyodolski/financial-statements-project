# Vercel 배포 문제 해결

## 500 INTERNAL_SERVER_ERROR 해결

### 1. 로그 확인

Vercel 대시보드에서:

1. 프로젝트 선택
2. **Deployments** 탭
3. 최신 배포 클릭
4. **Functions** 탭에서 로그 확인

또는 CLI로:

```bash
vercel logs
```

### 2. 환경 변수 확인

**필수 환경 변수:**

- `SUPABASE_URL`
- `SUPABASE_KEY`
- `FLASK_SECRET_KEY`

**확인 방법:**

```bash
vercel env ls
```

**추가 방법:**

```bash
vercel env add SUPABASE_URL
vercel env add SUPABASE_KEY
vercel env add FLASK_SECRET_KEY
```

또는 Vercel 대시보드:

1. Settings → Environment Variables
2. 각 변수 추가
3. Production, Preview, Development 모두 체크

### 3. 빌드 확인

**로컬에서 테스트:**

```bash
# 가상환경 활성화
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# 로컬 실행
python app.py

# 헬스 체크
curl http://localhost:5001/health
```

### 4. requirements.txt 확인

모든 패키지가 포함되어 있는지 확인:

```bash
pip freeze > requirements.txt
```

### 5. Python 버전 확인

`runtime.txt` 파일:

```
python-3.11.0
```

Vercel이 지원하는 버전인지 확인

### 6. 일반적인 오류

#### 오류: "Module not found"

**해결:**

```bash
# requirements.txt 업데이트
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

#### 오류: "Supabase connection failed"

**해결:**

1. Vercel 환경 변수 확인
2. Supabase URL이 올바른지 확인
3. Supabase Key가 올바른지 확인

#### 오류: "Permission denied"

**해결:**

- Vercel은 `/tmp` 외 쓰기 불가
- `app.py`에서 `IS_VERCEL` 확인

#### 오류: "Function timeout"

**해결:**

- 무료 플랜: 10초 제한
- Pro 플랜: 60초 제한
- 파일 처리 최적화 필요

## 디버깅 팁

### 1. 헬스 체크 엔드포인트 사용

```bash
curl https://your-app.vercel.app/health
```

응답 예시:

```json
{
  "status": "healthy",
  "environment": "vercel",
  "upload_folder": "/tmp/uploads",
  "output_folder": "/tmp/outputs"
}
```

### 2. 로그 추가

`app.py`에 디버그 로그 추가:

```python
import sys
print("환경 변수:", os.environ.keys(), file=sys.stderr)
print("Supabase URL:", os.getenv('SUPABASE_URL')[:20], file=sys.stderr)
```

### 3. 단계별 테스트

1. **헬스 체크**: `/health`
2. **메인 페이지**: `/`
3. **파일 업로드**: 작은 파일로 테스트
4. **관리자 페이지**: `/admin`

## Vercel 대안

Vercel이 계속 문제가 있다면:

### Railway (추천)

```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

**장점:**

- 파일 시스템 지원
- 더 긴 실행 시간
- 무료 Cron Job

### Render

1. https://render.com 가입
2. New Web Service
3. GitHub 연결
4. 환경 변수 설정
5. Deploy

**장점:**

- 파일 시스템 지원
- 무료 플랜
- 간단한 설정

## 체크리스트

배포 전 확인:

- [ ] `requirements.txt`에 모든 패키지 포함
- [ ] `wsgi.py` 파일 존재
- [ ] `vercel.json` 설정 확인
- [ ] 환경 변수 3개 모두 설정
- [ ] 로컬에서 정상 작동 확인
- [ ] `.env` 파일이 Git에 포함되지 않음

배포 후 확인:

- [ ] `/health` 엔드포인트 응답 확인
- [ ] 메인 페이지 로딩 확인
- [ ] Vercel 로그에 에러 없음
- [ ] 환경 변수 올바르게 설정됨

## 추가 도움

### Vercel 지원

- [Vercel 문서](https://vercel.com/docs)
- [Vercel Discord](https://vercel.com/discord)
- [Vercel GitHub](https://github.com/vercel/vercel)

### 커뮤니티

- Stack Overflow: `[vercel] [flask]` 태그
- GitHub Issues: 프로젝트 저장소

## 최종 권장사항

**Vercel이 적합한 경우:**

- 간단한 데모/프로토타입
- 파일 업로드가 적음
- 빠른 배포 필요

**Railway/Render가 적합한 경우:**

- 프로덕션 환경
- 많은 파일 업로드
- 백그라운드 작업 필요
- 안정적인 파일 저장소 필요

**현재 프로젝트는 Railway 또는 Render를 권장합니다!** ✅
