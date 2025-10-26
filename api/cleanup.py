"""
Vercel Cron Job용 정리 함수
Vercel Cron을 사용하여 주기적으로 호출
"""
from datetime import datetime, timedelta
import os
import sys

# 상위 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)


def cleanup_old_records():
    """7주(49일) 이상 된 레코드 자동 삭제"""
    try:
        cutoff_date = datetime.now() - timedelta(days=49)
        
        response = supabase.table('income_statements').select('*').lt('upload_date', cutoff_date.isoformat()).execute()
        
        if response.data:
            deleted_count = 0
            for record in response.data:
                try:
                    input_file = record['input_file_path']
                    output_file = record['output_file_path']
                    
                    if os.path.exists(input_file):
                        os.remove(input_file)
                    
                    if os.path.exists(output_file):
                        os.remove(output_file)
                    
                    supabase.table('income_statements').delete().eq('id', record['id']).execute()
                    deleted_count += 1
                except Exception as e:
                    print(f"레코드 {record['id']} 삭제 오류: {e}")
            
            return {'deleted': deleted_count, 'message': f'{deleted_count}개의 오래된 레코드를 삭제했습니다.'}
        
        return {'deleted': 0, 'message': '삭제할 레코드가 없습니다.'}
    except Exception as e:
        return {'error': str(e)}


def handler(request):
    """Vercel 서버리스 함수 핸들러"""
    result = cleanup_old_records()
    return {
        'statusCode': 200,
        'body': result
    }
