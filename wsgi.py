"""
WSGI entry point for Vercel
"""
from app import app

# Vercel이 이 변수를 찾습니다
application = app

if __name__ == "__main__":
    app.run()
