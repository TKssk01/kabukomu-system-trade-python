import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt
from token_manager import get_token
import market_data
import trading_logic
from settings import settings
import logging

# ロガーを設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

def initialize_session_state():
    if 'token' not in st.session_state:
        try:
            st.session_state.token = get_token()
        except Exception as e:
            logger.error(f"Failed to initialize token: {e}")
            st.error(f"認証に失敗しました。エラー: {e}")

def refresh_token_if_needed():
    try:
        st.session_state.token = get_token()
    except Exception as e:
        logger.error(f"Failed to refresh token: {e}")
        st.error(f"認証に失敗しました。エラー: {e}")
        st.stop()

def home():
    st.title("ホーム")
    st.write("このアプリケーションを使用して、自動取引システムを制御します。")

def market_data_page():
    st.title("マーケットデータ")
    refresh_token_if_needed()
    try:
        for symbol in settings.SYMBOLS:
            data = market_data.get_market_data(st.session_state.token, symbol)
            st.write(f"銘柄 {symbol} の最新のマーケットデータを表示します。")
            historical_data = pd.DataFrame(data['historical_prices'])  # 必要に応じてデータ形式を変換
            historical_data = trading_logic.calculate_moving_averages(historical_data)
            
            # ゴールデンクロスを可視化
            plt.figure(figsize=(10, 5))
            plt.plot(historical_data['Close'], label='Close Price')
            plt.plot(historical_data['Short_MA'], label='Short MA (20)')
            plt.plot(historical_data['Long_MA'], label='Long MA (50)')
            plt.title(f'銘柄 {symbol} の移動平均線')
            plt.legend()
            st.pyplot(plt)
    except Exception as e:
        logger.error(f"Failed to get market data: {e}")
        st.error(f"マーケットデータの取得に失敗しました。エラー: {e}")

def trading_loop_page():
    st.title("取引ループ")
    result_placeholder = st.empty()

    if 'trading' not in st.session_state:
        st.session_state.trading = False

    start_stop_button_label = "取引を開始" if not st.session_state.trading else "取引を停止"

    if st.button(start_stop_button_label):
        st.session_state.trading = not st.session_state.trading
        if st.session_state.trading:
            st.warning("取引ループが開始されました。このページを離れると停止します。")

    while st.session_state.trading:
        refresh_token_if_needed()
        try:
            for symbol in settings.SYMBOLS:
                raw_data = market_data.get_market_data(st.session_state.token, symbol)
                df = pd.DataFrame(raw_data['historical_prices'])  # 必要に応じてデータ形式を変換
                df = trading_logic.calculate_moving_averages(df)
                action = trading_logic.check_conditions(df)
                result_placeholder.success(f"銘柄 {symbol} - 取引アクション: {action}, 現在の価格: {df['Close'].iloc[-1]}")
            time.sleep(60)  # 60秒待機
        except Exception as e:
            logger.error(f"Error in trading loop: {e}")
            result_placeholder.error(f"エラーが発生しました: {e}")
            time.sleep(60)  # エラー時も60秒待機

def main():
    initialize_session_state()

    st.sidebar.title("ナビゲーション")
    selection = st.sidebar.radio("画面を選択", ["ホーム", "マーケットデータ", "取引ループ"])

    if selection == "ホーム":
        home()
    elif selection == "マーケットデータ":
        market_data_page()
    elif selection == "取引ループ":
        trading_loop_page()

if __name__ == "__main__":
    main()
