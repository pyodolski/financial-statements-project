#!/usr/bin/env python3
"""
손익계산서 계산 로직 모듈
"""


def calculate_totals(data):
    """
    추출된 데이터로부터 모든 합계 계산
    
    Args:
        data: extract_all_columns()에서 반환된 딕셔너리
    
    Returns:
        계산된 모든 합계를 포함하는 딕셔너리
    """
    # 중개이용료 합계
    jungae_total = data['h'] + data['i'] + data['j'] + data['k']
    
    # 고객할인 합계
    gohak_total = data['l'] + data['m']
    
    # 주문중개 합계
    jumun_jungae_total = data['f'] + data['g'] + jungae_total + gohak_total
    
    # 배달비 합계
    baedalbi_total = (data['n'] + data['o'] + data['p'] + data['q'] + 
                      data['r'] + data['s'] + data['t'] + data['u'] + 
                      data['v'] + data['w'])
    
    # 결제정산수수료 합계
    gyeoljae_total = data['x'] + data['y'] + data['z'] + data['aa']
    
    # 우리가게클릭 합계
    urigagae_total = data['ad'] + data['ae']
    
    # 입금금액
    ipgeum_total = (jumun_jungae_total + baedalbi_total + gyeoljae_total + 
                    data['ab'] + data['ac'] + urigagae_total)
    
    # 총매출
    total_maechul = data['f'] + data['g'] + data['n'] + data['o']
    
    # 매출원가
    maechul_wonka = (data['h'] + data['i'] + data['j'] + data['k'] +
                     data['l'] + data['m'] +
                     data['p'] + data['q'] + data['r'] + data['s'] +
                     data['t'] + data['u'] + data['v'] + data['w'] +
                     data['x'] + data['y'] +
                     data['ab'] +
                     data['ac'] +
                     data['ad'] + data['ae'])
    
    # 매출총이익
    maechul_total_iik = total_maechul + maechul_wonka
    
    return {
        'data': data,
        'jungae_total': jungae_total,
        'gohak_total': gohak_total,
        'jumun_jungae_total': jumun_jungae_total,
        'baedalbi_total': baedalbi_total,
        'gyeoljae_total': gyeoljae_total,
        'urigagae_total': urigagae_total,
        'ipgeum_total': ipgeum_total,
        'total_maechul': total_maechul,
        'maechul_wonka': maechul_wonka,
        'maechul_total_iik': maechul_total_iik
    }
