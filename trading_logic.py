import pandas as pd

def calculate_moving_averages(data, short_window=20, long_window=50):
    """
    短期および長期の移動平均線を計算する関数。

    :param data: マーケットデータ（DataFrame形式）
    :param short_window: 短期移動平均線の期間
    :param long_window: 長期移動平均線の期間
    :return: 短期移動平均線と長期移動平均線を含むDataFrame
    """
    data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()
    return data

def check_conditions(data):
    """
    ゴールデンクロスとデッドクロスの取引ロジック:
    - 短期移動平均線が長期移動平均線を上抜けた場合に買い注文を出す（ゴールデンクロス）
    - 短期移動平均線が長期移動平均線を下抜けた場合に売り注文を出す（デッドクロス）
    - それ以外の場合は取引を見送る

    :param data: 移動平均線を含むマーケットデータ（DataFrame形式）
    :return: "BUY", "SELL", "HOLD" のいずれかのアクション
    """
    if data['Short_MA'].iloc[-1] > data['Long_MA'].iloc[-1] and data['Short_MA'].iloc[-2] <= data['Long_MA'].iloc[-2]:
        return "BUY"
    elif data['Short_MA'].iloc[-1] < data['Long_MA'].iloc[-1] and data['Short_MA'].iloc[-2] >= data['Long_MA'].iloc[-2]:
        return "SELL"
    else:
        return "HOLD"
