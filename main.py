#Webアプリ画面設定
#バックエンド的な機能についてはPythonの標準的なモジュールインポート機能を利用（未整備）

#実行コマンド：streamlit run main.py

#####################################################
#ライブラリインポート
#####################################################
#ライブラリ
import streamlit as st
import os
from PIL import Image

#モジュール


#####################################################
# タイトル
#####################################################
st.title("SQL AGENT app")

#####################################################
# サイドバー
#####################################################
st.sidebar.title("設定")

# DBパスを入力するテキストボックス
db_path = st.sidebar.text_input("DBのパスを入力してください:", "")

# 画像フォルダを指定するテキストボックス
image_file_pass = st.sidebar.text_input("表示したい画像ファイルのパスを入力してください:", "")

# ラジオボタンでSQL RAGの手法を選択
rag_method = st.sidebar.radio(
    "SQL RAGの手法を選択してください:",
    [
        "Langchain SQLDatabaseChain",
        "Langchain create_sql_agent",
        "OpenAI codeInterpreter",
    ]
)

# チャット履歴を削除するボタン
if st.sidebar.button("チャット履歴を削除"):
    st.session_state["chat_history"] = []  # 履歴をリセット
    st.sidebar.success("チャット履歴が削除されました！")

#####################################################
# メイン画面
#####################################################
# dbフォルダ内のjpgファイルを表示
st.subheader("対象DBの参考図")
# img_path='./db/sqlite-sample-database-color.jpg'
# image = Image.open(img_path)
# st.image(image, use_container_width=True)
if image_file_pass and os.path.exists(image_file_pass):
    img_path = image_file_pass
    image = Image.open(img_path)
    st.image(image,  use_container_width=True)
else:
    st.info("表示する画像はありません。")


st.subheader("チャット画面")

# チャット履歴をセッションで管理
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# ユーザーからの入力
user_input = st.text_input("メッセージを入力してください:", "")
if user_input:
    # 入力メッセージを履歴に追加
    st.session_state["chat_history"].append(f"User: {user_input}")
    st.session_state["chat_history"].append(f"Agent: 回答内容はここに表示されます")  # 仮の応答

# チャット履歴を表示
for message in st.session_state["chat_history"]:
    st.write(message)

