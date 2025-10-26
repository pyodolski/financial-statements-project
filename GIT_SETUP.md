# Git 설정 및 배포 가이드

## 1. Git 초기화

```bash
# Git 초기화 (아직 안했다면)
git init

# 현재 상태 확인
git status
```

## 2. .gitignore 확인

`.gitignore` 파일이 제대로 설정되어 있는지 확인:

- `.env` 파일이 제외되는지 확인
- `venv/` 폴더가 제외되는지 확인
- `uploads/`, `outputs/` 폴더가 제외되는지 확인

## 3. 첫 커밋

```bash
# 모든 파일 추가
git add .

# 커밋
git commit -m "Initial commit: 배달 손익계산서 변환기"
```

## 4. GitHub 저장소 생성 및 연결

### GitHub에서:

1. GitHub 웹사이트 접속
2. New repository 클릭
3. 저장소 이름 입력 (예: `delivery-income-statement`)
4. Public 또는 Private 선택
5. Create repository 클릭

### 로컬에서:

```bash
# GitHub 저장소 연결
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 브랜치 이름 확인 및 변경 (필요시)
git branch -M main

# 푸시
git push -u origin main
```

## 5. 환경 변수 설정 (중요!)

### GitHub Secrets 설정 (GitHub Actions 사용 시)

1. GitHub 저장소 → Settings → Secrets and variables → Actions
2. New repository secret 클릭
3. 다음 시크릿 추가:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `FLASK_SECRET_KEY`

### 배포 플랫폼 환경 변수 설정

각 플랫폼의 대시보드에서 환경 변수 설정:

- Heroku: Settings → Config Vars
- Railway: Variables 탭
- Render: Environment 탭

## 6. 배포 전 체크리스트

- [ ] `.env` 파일이 Git에 포함되지 않았는지 확인
- [ ] `.env.example` 파일이 포함되어 있는지 확인
- [ ] `requirements.txt`에 모든 패키지가 포함되어 있는지 확인
- [ ] `README.md`가 최신 상태인지 확인
- [ ] Supabase 데이터베이스가 설정되어 있는지 확인
- [ ] 관리자 비밀번호를 변경했는지 확인 (선택사항)

## 7. 지속적인 업데이트

```bash
# 변경사항 확인
git status

# 변경사항 추가
git add .

# 커밋
git commit -m "설명적인 커밋 메시지"

# 푸시
git push origin main
```

## 8. 브랜치 전략 (선택사항)

### 개발/프로덕션 분리

```bash
# 개발 브랜치 생성
git checkout -b develop

# 작업 후 커밋
git add .
git commit -m "새 기능 추가"

# 개발 브랜치 푸시
git push origin develop

# 메인 브랜치로 병합 (준비되면)
git checkout main
git merge develop
git push origin main
```

## 9. 협업 시 주의사항

### Pull Request 워크플로우

1. 새 브랜치 생성: `git checkout -b feature/new-feature`
2. 작업 및 커밋
3. 푸시: `git push origin feature/new-feature`
4. GitHub에서 Pull Request 생성
5. 리뷰 후 병합

### 충돌 해결

```bash
# 최신 변경사항 가져오기
git pull origin main

# 충돌 발생 시 파일 수정 후
git add .
git commit -m "충돌 해결"
git push origin main
```

## 10. 유용한 Git 명령어

```bash
# 변경사항 확인
git diff

# 커밋 히스토리 확인
git log --oneline

# 특정 파일 변경사항 취소
git checkout -- filename

# 마지막 커밋 수정
git commit --amend

# 브랜치 목록 확인
git branch -a

# 원격 저장소 확인
git remote -v
```

## 11. 문제 해결

### .env 파일을 실수로 커밋한 경우

```bash
# Git 히스토리에서 제거
git rm --cached .env
git commit -m "Remove .env from repository"
git push origin main

# GitHub에서 시크릿 재생성 권장
```

### 대용량 파일 문제

```bash
# Git LFS 사용 (100MB 이상 파일)
git lfs install
git lfs track "*.xlsx"
git add .gitattributes
git commit -m "Add Git LFS"
```

## 12. 배포 자동화 (선택사항)

### GitHub Actions 예시 (.github/workflows/deploy.yml)

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{secrets.HEROKU_API_KEY}}
          heroku_app_name: "your-app-name"
          heroku_email: "your-email@example.com"
```
