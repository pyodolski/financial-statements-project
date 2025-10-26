# 빠른 시작 가이드

## Git에 올리기 (지금 바로!)

```bash
# 1. 모든 파일 추가
git add .

# 2. 커밋
git commit -m "Initial commit: 배달 손익계산서 변환기 v1.0"

# 3. GitHub에서 새 저장소 생성 후 (https://github.com/new)
# 저장소 URL을 복사하고 아래 명령어 실행

# 4. 원격 저장소 연결 (YOUR_USERNAME과 YOUR_REPO를 실제 값으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# 5. 푸시
git push -u origin main
```

## 배포하기 (Railway 추천 - 가장 쉬움)

### Railway 배포 (5분 완료)

1. **Railway 가입**: https://railway.app
2. **New Project** 클릭
3. **Deploy from GitHub repo** 선택
4. 방금 만든 저장소 선택
5. **환경 변수 추가**:
   - `SUPABASE_URL`: Supabase 프로젝트 URL
   - `SUPABASE_KEY`: Supabase anon key
   - `FLASK_SECRET_KEY`: 아무 랜덤 문자열 (예: `my-super-secret-key-12345`)
6. **Deploy** 클릭
7. 완료! 🎉

### Render 배포 (무료)

1. **Render 가입**: https://render.com
2. **New Web Service** 클릭
3. GitHub 저장소 연결
4. 설정:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. **환경 변수 추가** (위와 동일)
6. **Create Web Service** 클릭
7. 완료! 🎉

## 로컬에서 실행하기

```bash
# 1. 가상환경 활성화
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows

# 2. .env 파일 생성 및 설정
cp .env.example .env
# .env 파일을 열어서 Supabase 정보 입력

# 3. 폴더 생성
mkdir -p uploads outputs

# 4. 서버 실행
python app.py

# 5. 브라우저에서 접속
# http://localhost:5001
```

## Supabase 설정

1. **Supabase 가입**: https://supabase.com
2. **New Project** 생성
3. **SQL Editor**에서 `supabase_setup.sql` 실행
4. **Settings → API**에서 URL과 anon key 복사
5. `.env` 파일에 붙여넣기

## 문제 해결

### "Module not found" 에러

```bash
pip install -r requirements.txt
```

### "Permission denied" 에러

```bash
chmod +x app.py
```

### 포트 충돌

```bash
# app.py 마지막 줄 수정
app.run(debug=True, host='0.0.0.0', port=8000)  # 5001 → 8000
```

## 다음 단계

- [ ] 관리자 비밀번호 변경 (app.py에서 '0928' 검색)
- [ ] 커스텀 도메인 연결
- [ ] HTTPS 설정 (대부분 자동)
- [ ] 모니터링 설정

## 도움이 필요하신가요?

- 📖 자세한 문서: `README.md`
- 🚀 배포 가이드: `DEPLOYMENT.md`
- ✅ 체크리스트: `CHECKLIST.md`
- 🔧 Git 설정: `GIT_SETUP.md`
