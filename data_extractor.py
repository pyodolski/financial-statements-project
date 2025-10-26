#!/usr/bin/env python3
"""
Excel 데이터 추출 모듈
"""
import pandas as pd


def read_excel_data(file_path):
    """Excel 파일에서 데이터 읽기"""
    df_raw = pd.read_excel(file_path, sheet_name=0, header=None)
    headers = df_raw.iloc[4].tolist()
    df_data = df_raw.iloc[5:].copy()
    df_data.columns = headers
    return df_data


def extract_transaction_period(file_path):
    """Excel 파일에서 거래기간 추출"""
    try:
        df_raw = pd.read_excel(file_path, sheet_name=0, header=None)
        
        # 첫 5행에서 거래기간 찾기
        for row_idx in range(min(5, len(df_raw))):
            row = df_raw.iloc[row_idx]
            for cell in row:
                if pd.notna(cell):
                    cell_str = str(cell).strip()
                    # 거래기간 패턴 찾기
                    if '거래기간' in cell_str:
                        # "거래기간: 2024.01.01 ~ 2024.01.31" 형식
                        period = cell_str.replace('거래기간:', '').replace('거래기간', '').strip()
                        if period:
                            return period
                    # 날짜 범위 패턴 (YYYY.MM.DD ~ YYYY.MM.DD 또는 YYYY-MM-DD ~ YYYY-MM-DD)
                    elif '~' in cell_str and (cell_str.count('.') >= 4 or cell_str.count('-') >= 4):
                        return cell_str
                    # 날짜 범위 패턴 (YYYY.MM.DD-YYYY.MM.DD)
                    elif '-' in cell_str and cell_str.count('.') >= 4:
                        parts = cell_str.split('-')
                        if len(parts) == 2 and '.' in parts[0] and '.' in parts[1]:
                            return f"{parts[0].strip()} ~ {parts[1].strip()}"
        
        # 못 찾은 경우 None 반환
        return None
    except Exception as e:
        print(f"거래기간 추출 오류: {e}")
        return None


def get_column_sum(df, column_names):
    """
    여러 가능한 컬럼명 중 하나를 찾아서 합계 반환
    """
    if isinstance(column_names, str):
        column_names = [column_names]

    for col_name in column_names:
        if col_name in df.columns:
            return pd.to_numeric(df[col_name], errors='coerce').sum()

        for df_col in df.columns:
            if isinstance(df_col, str) and isinstance(col_name, str):
                if col_name.replace(' ', '').replace('(', '').replace(')', '') in df_col.replace(' ', '').replace('(', '').replace(')', ''):
                    return pd.to_numeric(df[df_col], errors='coerce').sum()
    return 0


def extract_all_columns(df_data):
    """모든 필요한 컬럼 데이터 추출"""
    return {
        'f': get_column_sum(df_data, ['바로결제주문금액', '바로결제 주문금액', '직접결제주문금액']),
        'g': get_column_sum(df_data, ['만나서결제주문금액', '만나서결제 주문금액', '현장결제주문금액']),
        'h': get_column_sum(df_data, ['배민1중개이용료', '배민1 중개이용료', '배민 1 중개이용료']),
        'i': get_column_sum(df_data, ['알뜰배달 중개이용료', '알뜰배달중개이용료']),
        'j': get_column_sum(df_data, ['오픈리스트중개이용료', '오픈리스트 중개이용료']),
        'k': get_column_sum(df_data, ['배민포장주문중개이용료', '배민포장 주문중개이용료', '포장주문중개이용료']),
        'l': get_column_sum(df_data, ['주문금액 즉시할인', '주문금액즉시할인', '즉시할인']),
        'm': get_column_sum(df_data, ['주문금액 즉시할인 지원', '주문금액즉시할인지원', '즉시할인지원']),
        'n': get_column_sum(df_data, ['바로결제배달팁', '바로결제 배달팁', '직접결제배달팁']),
        'o': get_column_sum(df_data, ['만나서결제배달팁', '만나서결제 배달팁', '현장결제배달팁']),
        'p': get_column_sum(df_data, ['배민클럽(한집배달) 배달팁 할인', '배민클럽한집배달배달팁할인']),
        'q': get_column_sum(df_data, ['배민클럽(한집배달) 배달팁 할인 지원', '배민클럽한집배달배달팁할인지원']),
        'r': get_column_sum(df_data, ['배민클럽(알뜰배달) 배달팁 할인', '배민클럽알뜰배달배달팁할인']),
        's': get_column_sum(df_data, ['배민클럽(알뜰배달) 배달팁 할인 지원', '배민클럽알뜰배달배달팁할인지원']),
        't': get_column_sum(df_data, ['배민1 한집배달 배달비', '배민1한집배달배달비']),
        'u': get_column_sum(df_data, ['배민1 한집배달 배달비할인', '배민1한집배달배달비할인']),
        'v': get_column_sum(df_data, ['알뜰배달 배달비', '알뜰배달배달비']),
        'w': get_column_sum(df_data, ['알뜰배달 배달비할인', '알뜰배달배달비할인']),
        'x': get_column_sum(df_data, ['기본수수료(정률)', '기본수수료', '정률수수료']),
        'y': get_column_sum(df_data, ['우대수수료', '할인수수료']),
        'z': get_column_sum(df_data, ['배민 만나서결제주문금액', '배민만나서결제주문금액']),
        'aa': get_column_sum(df_data, ['배민 만나서결제배달팁', '배민만나서결제배달팁']),
        'ab': get_column_sum(df_data, ['보정금액', '조정금액']),
        'ac': get_column_sum(df_data, ['(E) 부가세', 'E부가세', '부가세E']),
        'ad': get_column_sum(df_data, ['우리가게클릭 이용요금', '우리가게클릭이용요금']),
        'ae': get_column_sum(df_data, ['부가세', '부가세F'])
    }
