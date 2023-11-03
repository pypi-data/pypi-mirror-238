import time
import ksxt
from datetime import datetime

################################################################################################
# Public Feeder
################################################################################################
def test_fetch_market(koreainvest_exchange_app: ksxt.KoreaInvest):
    result = koreainvest_exchange_app.fetch_markets(market_name='nasdaq')
    
    assert result['response']['success'] == '0'

def test_fetch_security(koreainvest_exchange_app: ksxt.KoreaInvest, us_stock_symbol_app):
    result = koreainvest_exchange_app.fetch_security(symbol=us_stock_symbol_app, base_market='USD')
    
    assert result['response']['success'] == '0'

def test_fetch_ticker(koreainvest_exchange_app: ksxt.KoreaInvest, us_stock_symbol_app):
    result = koreainvest_exchange_app.fetch_ticker(symbol=us_stock_symbol_app, base_market='USD')
    
    assert result['response']['success'] == '0'
    assert float(result['price']) > 0

def test_fetch_historical_data_daily(koreainvest_exchange_app: ksxt.KoreaInvest, us_stock_symbol_app):
    time_frame = 'D'

    result = koreainvest_exchange_app.fetch_historical_data(symbol=us_stock_symbol_app,
                                                        time_frame=time_frame,
                                                        base_market='USD')
    
    assert result['response']['success'] == '0'
    assert len(result['history']) > 0

def test_fetch_historical_data_weekly(koreainvest_exchange_app: ksxt.KoreaInvest, us_stock_symbol_app):
    time_frame = 'W'

    result = koreainvest_exchange_app.fetch_historical_data(symbol=us_stock_symbol_app,
                                                        time_frame=time_frame,
                                                        base_market='USD')
    
    assert result['response']['success'] == '0'
    assert len(result['history']) > 0

def test_fetch_historical_data_monthly(koreainvest_exchange_app: ksxt.KoreaInvest, us_stock_symbol_app):
    time_frame = 'M'

    result = koreainvest_exchange_app.fetch_historical_data(symbol=us_stock_symbol_app,
                                                        time_frame=time_frame,
                                                        base_market='USD')
    
    assert result['response']['success'] == '0'
    assert len(result['history']) > 0

def test_fetch_historical_data_yearly(koreainvest_exchange_app: ksxt.KoreaInvest, us_stock_symbol_app):
    time_frame = 'Y'

    result = koreainvest_exchange_app.fetch_historical_data(symbol=us_stock_symbol_app,
                                                        time_frame=time_frame,
                                                        base_market='USD')
    
    # 미국장은 년 단위 Historical Data를 조회하지 않음.
    assert result['response']['success'] == '-1'

def test_fetch_is_holiday(koreainvest_exchange_app: ksxt.KoreaInvest):
    holiday = datetime(2023, 8, 13)

    # 미국장은 현재 휴장일 정보 조회가 되지 않음.
    result = koreainvest_exchange_app.fetch_is_holiday(holiday, base_market='USD')
    assert result['response']['success'] != '0'

def test_fetch_is_not_holiday(koreainvest_exchange_app: ksxt.KoreaInvest):
    holiday = datetime(2023, 8, 14)

    # 미국장은 현재 휴장일 정보 조회가 되지 않음.
    result = koreainvest_exchange_app.fetch_is_holiday(holiday, base_market='USD')
    assert result['response']['success'] != '0'


################################################################################################
# Private Feeder
################################################################################################
def test_fetch_balance(koreainvest_exchange_app: ksxt.KoreaInvest, koreainvest_us_accnum_app):
    result = koreainvest_exchange_app.fetch_balance(acc_num=koreainvest_us_accnum_app, base_market='USD')

    assert result['response']['success'] == '0'

def test_fetch_cash(koreainvest_exchange_app: ksxt.KoreaInvest, koreainvest_us_accnum_app):
    result = koreainvest_exchange_app.fetch_cash(acc_num=koreainvest_us_accnum_app, base_market='USD')

    if koreainvest_exchange_app.is_dev:
        assert result['response']['success'] == '-1'
    else:
        assert result['response']['success'] == '0'
        assert result['cash'] > 0

def test_fetch_screener_list(koreainvest_exchange_app: ksxt.KoreaInvest, koreainvest_hts_user_id):
    result = koreainvest_exchange_app.fetch_screener_list(user_id=koreainvest_hts_user_id, base_market='USD')

    # 미국장은 조건검색리스트 기능을 제공하지 않음.
    assert result['response']['success'] == '-1'
        

def test_fetch_screener(koreainvest_exchange_app: ksxt.KoreaInvest, koreainvest_hts_user_id):
    screen_id = '0'
    result = koreainvest_exchange_app.fetch_screener(user_id=koreainvest_hts_user_id, screen_id=screen_id, base_market='USD')

    assert result['response']['success'] == '0'

################################################################################################
# Broker
################################################################################################
def test_create_limit_buy_order(koreainvest_exchange_app: ksxt.KoreaInvest, koreainvest_us_accnum_app, us_stock_symbol_app):
    ticket_type = 'entry_long'
    current_price = float(koreainvest_exchange_app.fetch_ticker(symbol=us_stock_symbol_app, base_market='USD')['price'])
    price = round(current_price * 1.01, 4)
    qty = 1
    otype = 'limit'

    result = koreainvest_exchange_app.create_order(acc_num=koreainvest_us_accnum_app,
                                               symbol=us_stock_symbol_app,
                                               ticket_type=ticket_type,
                                               price=price,
                                               qty=qty,
                                               otype=otype,
                                               base_market='USD')
    
    assert result['response']['success'] == '0'

def test_create_market_buy_order(koreainvest_exchange_app: ksxt.KoreaInvest, koreainvest_us_accnum_app, us_stock_symbol_app):
    ticket_type = 'entry_long'
    current_price = float(koreainvest_exchange_app.fetch_ticker(symbol=us_stock_symbol_app, base_market='USD')['price'])
    price = round(current_price * 1.01, 4)
    qty = 1
    otype = 'market'

    result = koreainvest_exchange_app.create_order(acc_num=koreainvest_us_accnum_app,
                                               symbol=us_stock_symbol_app,
                                               ticket_type=ticket_type,
                                               price=price,
                                               qty=qty,
                                               otype=otype,
                                               base_market='USD')
    
    # 미국장은 시장가 거래를 지원하지 않음
    assert result['response']['success'] == '-1'

def test_create_limit_sell_order(koreainvest_exchange_app: ksxt.KoreaInvest, koreainvest_us_accnum_app, us_stock_symbol_app):
    ticket_type = 'exit_long'
    current_price = float(koreainvest_exchange_app.fetch_ticker(symbol=us_stock_symbol_app, base_market='USD')['price'])
    price = round(current_price * 0.99, 4)
    qty = 1
    otype = 'limit'

    result = koreainvest_exchange_app.create_order(acc_num=koreainvest_us_accnum_app,
                                               symbol=us_stock_symbol_app,
                                               ticket_type=ticket_type,
                                               price=price,
                                               qty=qty,
                                               otype=otype,
                                               base_market='USD')
    
    assert result['response']['success'] == '0'

def test_create_market_sell_order(koreainvest_exchange_app: ksxt.KoreaInvest, koreainvest_us_accnum_app, us_stock_symbol_app):
    ticket_type = 'exit_long'
    current_price = float(koreainvest_exchange_app.fetch_ticker(symbol=us_stock_symbol_app, base_market='USD')['price'])
    price = round(current_price * 0.99, 4)
    qty = 1
    otype = 'market'

    result = koreainvest_exchange_app.create_order(acc_num=koreainvest_us_accnum_app,
                                               symbol=us_stock_symbol_app,
                                               ticket_type=ticket_type,
                                               price=price,
                                               qty=qty,
                                               otype=otype,
                                               base_market='USD')
    
    # 미국장은 시장가 거래를 지원하지 않음
    assert result['response']['success'] == '-1'

def test_cancel_order(koreainvest_exchange_app: ksxt.KoreaInvest, koreainvest_us_accnum_app, us_stock_symbol_app):
    ticket_type = 'entry_long'
    current_price = float(koreainvest_exchange_app.fetch_ticker(symbol=us_stock_symbol_app, base_market='USD')['price'])
    price = round(current_price * 0.97, 4)
    qty = 1
    otype = 'limit'

    result = koreainvest_exchange_app.create_order(acc_num=koreainvest_us_accnum_app,
                                               symbol=us_stock_symbol_app,
                                               ticket_type=ticket_type,
                                               price=price,
                                               qty=qty,
                                               otype=otype,
                                               base_market='USD')
    
    order_id = result['order_id']

    time.sleep(3)

    result = koreainvest_exchange_app.cancel_order(acc_num=koreainvest_us_accnum_app,
                                               order_id=order_id,
                                               symbol=us_stock_symbol_app,
                                               base_market='USD',
                                               qty=qty)
    
    assert result['response']['success'] == '0'


def test_modify_order(koreainvest_exchange_app: ksxt.KoreaInvest, koreainvest_us_accnum_app, us_stock_symbol_app):
    ticket_type = 'entry_long'
    current_price = float(koreainvest_exchange_app.fetch_ticker(symbol=us_stock_symbol_app, base_market='USD')['price'])
    price = round(current_price * 0.97, 4)
    qty = 1
    otype = 'limit'

    result = koreainvest_exchange_app.create_order(acc_num=koreainvest_us_accnum_app,
                                               symbol=us_stock_symbol_app,
                                               ticket_type=ticket_type,
                                               price=price,
                                               qty=qty,
                                               otype=otype,
                                               base_market='USD')
    
    order_id = result['order_id']

    current_price = float(koreainvest_exchange_app.fetch_ticker(symbol=us_stock_symbol_app, base_market='USD')['price'])
    price = round(current_price * 1.03, 4)

    time.sleep(3)

    result = koreainvest_exchange_app.modify_order(acc_num=koreainvest_us_accnum_app,
                                               order_id=order_id,
                                               price=price,
                                               qty=qty,
                                               symbol=us_stock_symbol_app,
                                               base_market='USD')
    
    assert result['response']['success'] == '0'

def test_fetch_open_order(koreainvest_exchange_app: ksxt.KoreaInvest, koreainvest_us_accnum_app):
    result = koreainvest_exchange_app.fetch_open_order(acc_num=koreainvest_us_accnum_app, base_market='USD')

    assert result['response']['success'] == '0'

def test_fetch_closed_order(koreainvest_exchange_app: ksxt.KoreaInvest, koreainvest_us_accnum_app):
    result = koreainvest_exchange_app.fetch_closed_order(acc_num=koreainvest_us_accnum_app, base_market='USD')

    assert result['response']['success'] == '0'