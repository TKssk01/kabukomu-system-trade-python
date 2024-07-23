import streamlit as st
import urllib.request
import json

# 設定情報
API_PASSWORD = '1995taka'
ORDER_PASSWORD = '1995tAkA@@'
API_URL = 'http://localhost:18080/kabusapi'
SYMBOLS = {
    '1321': '野村日経平均',
    '1332': '日本水産',
    '1306': 'TOPIX連動型上場投資信託'
}

# トークンを取得する関数
def generate_token(api_password):
    obj = {'APIPassword': api_password}
    json_data = json.dumps(obj).encode('utf8')
    url = f'{API_URL}/token'
    req = urllib.request.Request(url, json_data, method='POST')
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as res:
            content = json.loads(res.read())
            token_value = content.get('Token')
            return token_value
    except urllib.error.HTTPError as e:
        st.error(f"HTTP Error: {e}")
        try:
            error_content = json.loads(e.read())
            st.json(error_content)
        except Exception as json_err:
            st.error(f"Failed to parse error content: {json_err}")
    except Exception as e:
        st.error(f"Error: {e}")
    return None

# 注文を送信する関数
def send_order(token, symbol):
    # 注文パラメータ
    obj = {
        'Password': ORDER_PASSWORD,
        'Symbol': symbol,
        'Exchange': 1,
        'SecurityType': 1,
        'Side': '2',  # 買い注文
        'CashMargin': 1,  # 現物取引
        'DelivType': 2,  # 預り金
        'FundType': 'AA',  # 信用代用
        'AccountType': 2,  # 一般口座
        'Qty': 1,  # 注文数量 1株
        'FrontOrderType': 10,  # 成行注文
        'Price': 0,  # 成行注文なので価格は0
        'ExpireDay': 0,  # 当日限り
    }
    json_data = json.dumps(obj).encode('utf-8')
    url = f'{API_URL}/sendorder'
    req = urllib.request.Request(url, json_data, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', token)
    
    try:
        with urllib.request.urlopen(req) as res:
            st.write(f"Status: {res.status}, Reason: {res.reason}")
            content = json.loads(res.read())
            st.json(content)
    except urllib.error.HTTPError as e:
        st.error(f"HTTP Error: {e}")
        try:
            error_content = json.loads(e.read())
            st.json(error_content)
        except Exception as json_err:
            st.error(f"Failed to parse error content: {json_err}")
    except Exception as e:
        st.error(f"Error: {e}")

# StreamlitアプリケーションのUI
def main():
    st.title("シンプル株購入システム")
    
    # トークン取得
    st.subheader("トークンを取得")
    if st.button("トークン取得"):
        token = generate_token(API_PASSWORD)
        if token:
            st.session_state.token = token
            st.success("トークンを取得しました")
            st.write(f"取得したトークン: {token}")
        else:
            st.error("トークンの取得に失敗しました")
    
    # 株購入
    if 'token' in st.session_state:
        st.subheader("株を購入")
        selected_symbol = st.selectbox("購入する銘柄を選択", [f"{symbol}: {name}" for symbol, name in SYMBOLS.items()])
        selected_symbol = selected_symbol.split(":")[0]  # 選択された銘柄コードを抽出
        if st.button("購入"):
            send_order(st.session_state.token, selected_symbol)
    else:
        st.warning("まずトークンを取得してください")

if __name__ == "__main__":
    main()
