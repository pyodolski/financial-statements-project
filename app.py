#!/usr/bin/env python3
"""
배달 손익계산서 변환기 웹 애플리케이션
"""
from flask import Flask, render_template, request, send_file, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from supabase import create_client, Client
from dotenv import load_dotenv
import json
import threading
import time
import traceback

# 환경 변수 로드
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')

# Vercel 환경 감지
IS_VERCEL = os.getenv('VERCEL') == '1' or os.getenv('VERCEL_ENV') is not None

if IS_VERCEL:
    # Vercel에서는 /tmp 디렉토리 사용
    app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
    app.config['OUTPUT_FOLDER'] = '/tmp/outputs'
    print("✓ Vercel 환경 감지됨 - /tmp 디렉토리 사용")
else:
    # 로컬 환경
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['OUTPUT_FOLDER'] = 'outputs'

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# 폴더 생성 (에러 무시)
try:
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
except Exception as e:
    print(f"폴더 생성 오류 (무시됨): {e}")

# Supabase 클라이언트
try:
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL 또는 SUPABASE_KEY가 설정되지 않았습니다")
    
    supabase: Client = create_client(supabase_url, supabase_key)
    print("✓ Supabase 연결 성공")
except Exception as e:
    print(f"❌ Supabase 연결 오류: {e}")
    raise

# main.py의 함수들 가져오기
from income_statement import generate_income_statement

@app.route('/health')
def health():
    """헬스 체크 엔드포인트"""
    return jsonify({
        'status': 'healthy',
        'environment': 'vercel' if IS_VERCEL else 'local',
        'upload_folder': app.config['UPLOAD_FOLDER'],
        'output_folder': app.config['OUTPUT_FOLDER']
    }), 200


@app.route('/')
def index():
    """메인 페이지"""
    # 오래된 레코드 자동 삭제 (Vercel이 아닌 경우만)
    if not IS_VERCEL:
        cleanup_old_records()
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """파일 업로드 및 변환"""
    if 'file' not in request.files:
        return jsonify({'error': '파일이 없습니다'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '파일이 선택되지 않았습니다'}), 400
    
    if not file.filename.endswith('.xlsx'):
        return jsonify({'error': 'Excel 파일(.xlsx)만 업로드 가능합니다'}), 400
    
    try:
        # 파일 저장
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        input_filename = f"{timestamp}_{filename}"
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
        file.save(input_path)
        
        # 손익계산서 생성
        output_filename = f"손익계산서_{timestamp}.xlsx"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        result = generate_income_statement(input_path, output_path)
        transaction_period = result.get('transaction_period')
        
        # 동일한 거래기간의 기존 데이터 확인 및 삭제
        is_updated = False
        if transaction_period:
            try:
                existing = supabase.table('income_statements').select('*').eq('transaction_period', transaction_period).execute()
                
                if existing.data:
                    for old_record in existing.data:
                        # 기존 파일 삭제
                        old_input = old_record['input_file_path']
                        old_output = old_record['output_file_path']
                        
                        if os.path.exists(old_input):
                            os.remove(old_input)
                        
                        if os.path.exists(old_output):
                            os.remove(old_output)
                        
                        # DB에서 기존 레코드 삭제
                        supabase.table('income_statements').delete().eq('id', old_record['id']).execute()
                    
                    is_updated = True
                    print(f"✓ 동일한 거래기간({transaction_period})의 기존 데이터 {len(existing.data)}건을 삭제했습니다.")
            except Exception as e:
                print(f"기존 데이터 삭제 오류: {e}")
        
        # DB에 새 데이터 저장
        data = {
            'upload_filename': filename,
            'transaction_period': transaction_period,
            'input_file_path': input_path,
            'output_file_path': output_path,
            'upload_date': datetime.now().isoformat(),
            'total_sales': result['total_maechul'],
            'total_cost': result['maechul_wonka'],
            'gross_profit': result['maechul_total_iik'],
            'deposit_amount': result['ipgeum_total']
        }
        
        response = supabase.table('income_statements').insert(data).execute()
        
        return jsonify({
            'success': True,
            'output_filename': output_filename,
            'result': result,
            'id': response.data[0]['id'],
            'updated': is_updated
        })
        
    except Exception as e:
        # 오류 발생 시 임시 파일 정리
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """파일 다운로드"""
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': '파일을 찾을 수 없습니다'}), 404

def cleanup_old_records():
    """7주(49일) 이상 된 레코드 자동 삭제"""
    try:
        cutoff_date = datetime.now() - timedelta(days=49)
        
        # 7주 이상 된 레코드 조회
        response = supabase.table('income_statements').select('*').lt('upload_date', cutoff_date.isoformat()).execute()
        
        if response.data:
            deleted_count = 0
            for record in response.data:
                try:
                    # 파일 삭제
                    input_file = record['input_file_path']
                    output_file = record['output_file_path']
                    
                    if os.path.exists(input_file):
                        os.remove(input_file)
                    
                    if os.path.exists(output_file):
                        os.remove(output_file)
                    
                    # DB에서 레코드 삭제
                    supabase.table('income_statements').delete().eq('id', record['id']).execute()
                    deleted_count += 1
                except Exception as e:
                    print(f"레코드 {record['id']} 삭제 오류: {e}")
            
            if deleted_count > 0:
                print(f"✓ {deleted_count}개의 오래된 레코드를 삭제했습니다.")
    except Exception as e:
        print(f"자동 삭제 오류: {e}")


def cleanup_scheduler():
    """백그라운드에서 매일 자동 삭제 실행"""
    while True:
        try:
            cleanup_old_records()
        except Exception as e:
            print(f"스케줄러 오류: {e}")
        # 24시간마다 실행
        time.sleep(86400)

@app.route('/history')
def history():
    """변환 이력 조회"""
    try:
        # 오래된 레코드 자동 삭제 (Vercel이 아닌 경우만)
        if not IS_VERCEL:
            cleanup_old_records()
        
        response = supabase.table('income_statements').select('*').order('upload_date', desc=True).execute()
        return render_template('history.html', records=response.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/records')
def get_records():
    """API: 전체 기록 조회"""
    try:
        response = supabase.table('income_statements').select('*').order('upload_date', desc=True).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/record/<int:record_id>')
def get_record(record_id):
    """API: 특정 기록 조회"""
    try:
        response = supabase.table('income_statements').select('*').eq('id', record_id).execute()
        if response.data:
            return jsonify(response.data[0])
        return jsonify({'error': '기록을 찾을 수 없습니다'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin')
def admin():
    """관리자 페이지"""
    return render_template('admin.html')

@app.route('/admin/verify', methods=['POST'])
def admin_verify():
    """관리자 비밀번호 확인"""
    data = request.get_json()
    password = data.get('password', '')
    
    if password == '0928':
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': '비밀번호가 올바르지 않습니다'}), 401

def parse_month_from_period(period_str):
    """거래기간에서 월 추출 (종료일 기준)"""
    if not period_str:
        return None
    
    try:
        # "2024.07.26 ~ 2024.08.26" 또는 "07-26-08-26" 형식 처리
        period_str = str(period_str).strip()
        
        # ~ 기준으로 분리
        if '~' in period_str:
            parts = period_str.split('~')
            end_date = parts[1].strip() if len(parts) > 1 else parts[0].strip()
        else:
            # 하이픈으로만 구분된 경우 (07-26-08-26)
            parts = period_str.split('-')
            if len(parts) >= 4:
                # 마지막 두 부분이 종료 월-일
                end_date = f"{parts[-2]}-{parts[-1]}"
            else:
                end_date = period_str
        
        # 날짜에서 연도와 월 추출
        end_date = end_date.replace('.', '-').replace('/', '-')
        date_parts = [p.strip() for p in end_date.split('-') if p.strip()]
        
        if len(date_parts) >= 2:
            year = date_parts[0] if len(date_parts[0]) == 4 else f"20{date_parts[0]}"
            month = date_parts[1].zfill(2)
            return f"{year}-{month}"
        
        return None
    except Exception as e:
        print(f"월 파싱 오류: {e}, 입력: {period_str}")
        return None


@app.route('/admin/data')
def admin_data():
    """관리자 데이터 조회 (비밀번호 확인 후)"""
    password = request.args.get('password', '')
    
    if password != '0928':
        return jsonify({'error': '권한이 없습니다'}), 403
    
    try:
        response = supabase.table('income_statements').select('*').order('upload_date', desc=True).execute()
        return jsonify(response.data)
    except Exception as e:
        print(f"admin_data 오류: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/admin/statistics')
def admin_statistics():
    """관리자 통계 조회"""
    password = request.args.get('password', '')
    
    if password != '0928':
        return jsonify({'error': '권한이 없습니다'}), 403
    
    try:
        response = supabase.table('income_statements').select('*').execute()
        records = response.data
        
        # 월별 통계 집계
        monthly_stats = {}
        
        for record in records:
            month = parse_month_from_period(record.get('transaction_period'))
            
            if month:
                if month not in monthly_stats:
                    monthly_stats[month] = {
                        'month': month,
                        'count': 0,
                        'total_sales': 0,
                        'total_cost': 0,
                        'gross_profit': 0,
                        'deposit_amount': 0
                    }
                
                monthly_stats[month]['count'] += 1
                monthly_stats[month]['total_sales'] += float(record.get('total_sales', 0) or 0)
                monthly_stats[month]['total_cost'] += float(record.get('total_cost', 0) or 0)
                monthly_stats[month]['gross_profit'] += float(record.get('gross_profit', 0) or 0)
                monthly_stats[month]['deposit_amount'] += float(record.get('deposit_amount', 0) or 0)
        
        # 월별로 정렬 (최신순)
        sorted_stats = sorted(monthly_stats.values(), key=lambda x: x['month'], reverse=True)
        
        # 전체 통계
        total_stats = {
            'total_records': len(records),
            'total_sales': sum(float(r.get('total_sales', 0) or 0) for r in records),
            'total_cost': sum(float(r.get('total_cost', 0) or 0) for r in records),
            'gross_profit': sum(float(r.get('gross_profit', 0) or 0) for r in records),
            'deposit_amount': sum(float(r.get('deposit_amount', 0) or 0) for r in records)
        }
        
        return jsonify({
            'monthly': sorted_stats,
            'total': total_stats
        })
        
    except Exception as e:
        print(f"admin_statistics 오류: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/admin/download/input/<int:record_id>')
def admin_download_input(record_id):
    """원본 파일 다운로드"""
    password = request.args.get('password', '')
    
    if password != '0928':
        return jsonify({'error': '권한이 없습니다'}), 403
    
    try:
        response = supabase.table('income_statements').select('*').eq('id', record_id).execute()
        if response.data:
            file_path = response.data[0]['input_file_path']
            if os.path.exists(file_path):
                return send_file(file_path, as_attachment=True)
        return jsonify({'error': '파일을 찾을 수 없습니다'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/download/output/<int:record_id>')
def admin_download_output(record_id):
    """손익계산서 파일 다운로드"""
    password = request.args.get('password', '')
    
    if password != '0928':
        return jsonify({'error': '권한이 없습니다'}), 403
    
    try:
        response = supabase.table('income_statements').select('*').eq('id', record_id).execute()
        if response.data:
            file_path = response.data[0]['output_file_path']
            if os.path.exists(file_path):
                return send_file(file_path, as_attachment=True)
        return jsonify({'error': '파일을 찾을 수 없습니다'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/delete/<int:record_id>', methods=['DELETE'])
def admin_delete_record(record_id):
    """데이터 삭제"""
    data = request.get_json()
    password = data.get('password', '')
    
    if password != '0928':
        return jsonify({'error': '권한이 없습니다'}), 403
    
    try:
        # DB에서 레코드 조회
        response = supabase.table('income_statements').select('*').eq('id', record_id).execute()
        
        if not response.data:
            return jsonify({'error': '데이터를 찾을 수 없습니다'}), 404
        
        record = response.data[0]
        
        # 파일 삭제
        input_file = record['input_file_path']
        output_file = record['output_file_path']
        
        if os.path.exists(input_file):
            os.remove(input_file)
        
        if os.path.exists(output_file):
            os.remove(output_file)
        
        # DB에서 레코드 삭제
        supabase.table('income_statements').delete().eq('id', record_id).execute()
        
        return jsonify({'success': True, 'message': '삭제되었습니다'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 백그라운드 스케줄러 시작 (Vercel이 아닌 경우만)
if not IS_VERCEL:
    scheduler_thread = threading.Thread(target=cleanup_scheduler, daemon=True)
    scheduler_thread.start()
    print("✓ 자동 삭제 스케줄러가 시작되었습니다 (매일 실행)")
else:
    print("✓ Vercel 환경: Cron Job을 사용하여 자동 삭제가 실행됩니다")

if __name__ == '__main__':
    # 개발 환경
    app.run(debug=True, host='0.0.0.0', port=5001)
