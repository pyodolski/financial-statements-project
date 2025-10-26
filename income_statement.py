#!/usr/bin/env python3
"""
손익계산서 생성 메인 모듈
"""
from data_extractor import read_excel_data, extract_all_columns
from calculator import calculate_totals
from excel_generator import generate_excel


def generate_income_statement(input_file, output_file):
    """
    입력 파일로부터 손익계산서 생성
    
    Args:
        input_file: 입력 Excel 파일 경로
        output_file: 출력 Excel 파일 경로
    
    Returns:
        계산 결과 딕셔너리 (거래기간 포함)
    """
    from data_extractor import extract_transaction_period
    
    # 0. 거래기간 추출
    transaction_period = extract_transaction_period(input_file)
    
    # 1. 데이터 읽기
    df_data = read_excel_data(input_file)
    
    # 2. 컬럼 데이터 추출
    column_data = extract_all_columns(df_data)
    
    # 3. 합계 계산
    calc_result = calculate_totals(column_data)
    
    # 4. Excel 생성
    generate_excel(output_file, calc_result)
    
    # 5. 결과 반환
    return {
        'transaction_period': transaction_period,
        'total_maechul': float(calc_result['total_maechul']),
        'maechul_wonka': float(calc_result['maechul_wonka']),
        'maechul_total_iik': float(calc_result['maechul_total_iik']),
        'ipgeum_total': float(calc_result['ipgeum_total']),
        'jumun_jungae_total': float(calc_result['jumun_jungae_total']),
        'baedalbi_total': float(calc_result['baedalbi_total']),
        'gyeoljae_total': float(calc_result['gyeoljae_total']),
        'urigagae_total': float(calc_result['urigagae_total'])
    }
