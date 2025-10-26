# 배포 가이드

## 로컬 개발 환경

### 요구사항

- Python 3.8 이상
- pip
- Supabase 계정

### 설정

1. 가상환경 생성 및 활성화
2. `pip install -r requirements.txt`
3. `.env` 파일 설정
4. Supabase 데이터베이스 설정
5. `python app.py` 실행

## 프로덕션 배포

### 1. Heroku 배포

#### Procfile 생성

```
web: gunicorn app:app
```

#### runtime.txt 생성

```
python-3.11.0
```

#### requirements.txt에 gunicorn 추가

```bash
pip install gunicorn
pip freeze > requirements.txt
```

#### Heroku 배포 명령

```bash
heroku create your-app-name
heroku config:set SUPABASE_URL=your_url
heroku config:set SUPABASE_KEY=your_key
heroku config:set FLASK_SECRET_KEY=your_secret
git push heroku main
```

### 2. Railway 배포

1. Railway 계정 생성
2. GitHub 저장소 연결
3. 환경 변수 설정:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `FLASK_SECRET_KEY`
4. 자동 배포 시작

### 3. Render 배포

1. Render 계정 생성
2. New Web Service 선택
3. GitHub 저장소 연결
4. 설정:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. 환경 변수 추가
6. Deploy

### 4. Docker 배포

#### Dockerfile 생성

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p uploads outputs

EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
```

#### docker-compose.yml

```yaml
version: "3.8"
services:
  web:
    build: .
    ports:
      - "5001:5001"
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
      - FLASK_SECRET_KEY=${FLASK_SECRET_KEY}
    volumes:
      - ./uploads:/app/uploads
      - ./outputs:/app/outputs
```

#### 실행

```bash
docker-compose up -d
```

## 환경 변수

프로덕션 환경에서 반드시 설정해야 할 환경 변수:

- `SUPABASE_URL`: Supabase 프로젝트 URL
- `SUPABASE_KEY`: Supabase anon/public key
- `FLASK_SECRET_KEY`: Flask 세션 암호화 키 (랜덤 문자열)

## 보안 체크리스트

- [ ] `.env` 파일이 `.gitignore`에 포함되어 있는지 확인
- [ ] 프로덕션에서 `DEBUG=False` 설정
- [ ] 관리자 비밀번호 변경 (코드에서 하드코딩된 '0928')
- [ ] HTTPS 사용
- [ ] CORS 설정 확인
- [ ] Rate limiting 추가 고려

## 성능 최적화

### 프로덕션 서버 설정

```python
# app.py 마지막 부분 수정
if __name__ == '__main__':
    # 개발 환경
    scheduler_thread = threading.Thread(target=cleanup_scheduler, daemon=True)
    scheduler_thread.start()
    app.run(debug=True, host='0.0.0.0', port=5001)
else:
    # 프로덕션 환경 (gunicorn 등)
    scheduler_thread = threading.Thread(target=cleanup_scheduler, daemon=True)
    scheduler_thread.start()
```

### Gunicorn 설정

```bash
gunicorn --workers 4 --threads 2 --bind 0.0.0.0:5001 app:app
```

## 모니터링

### 로그 설정

```python
import logging
logging.basicConfig(level=logging.INFO)
```

### 헬스 체크 엔드포인트 추가

```python
@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200
```

## 백업

### 데이터베이스 백업

- Supabase 대시보드에서 자동 백업 설정
- 정기적으로 수동 백업 수행

### 파일 백업

- `uploads/` 및 `outputs/` 폴더 정기 백업
- 클라우드 스토리지 연동 고려 (S3, Google Cloud Storage 등)

## 문제 해결

### 일반적인 문제

1. **포트 충돌**: 다른 포트 사용 (`--bind 0.0.0.0:8000`)
2. **메모리 부족**: Worker 수 줄이기
3. **파일 업로드 실패**: `MAX_CONTENT_LENGTH` 확인
4. **데이터베이스 연결 실패**: Supabase 자격 증명 확인

### 로그 확인

```bash
# Heroku
heroku logs --tail

# Docker
docker-compose logs -f

# 로컬
tail -f app.log
```
