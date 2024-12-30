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

#LLM関連ライブラリ
import configparser
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain

#モジュール
#from tools.tools_chat_LLMmodels import test_hello
from tools.tools_chat_LLMmodels import chat_LLMmodels
from tools.tools_SQLDatabaseChain import SQLDatabaseChain_LLMmodels

#####################################################
# アプリケーション全般
#####################################################
def main():        
    #ウェブページの設定
    st.set_page_config(
        page_title="Test App",
        page_icon="./pic/figure_chatGPT.png"
    )

    #サイドバーの表示
    db_path,image_file_pass,rag_method,temperature,opt_system_prompt=options_view_sidebar()

    #LLMモデルの設定
    if rag_method=="LLM Nomal chat":
        #ChatOpenAIクラスのインスタンス化
        #llm = select_model(temperature)
        #temperature=0.7
        instance_LLMmodele=chat_LLMmodels()
        llm = instance_LLMmodele.select_chatmodel(temperature)
        prompt=ChatPromptTemplate.from_messages([
            ("system",opt_system_prompt),
            ("user","{input}")
        ])
        #GPTの返答をパースするための処理
        output_parser=StrOutputParser()
        # #LCELでの記法
        # chain = prompt | llm | output_parser
        
        # LLMChainの作成 (| 演算子は使わず、LLMChainで組み立て)
        chain = LLMChain(
        prompt=prompt,
        llm=llm,
        output_key="parsed_output"  # 出力をパースした後のキーを指定
        )
        
    elif rag_method=="Langchain SQLDatabaseChain":
        #外部モジュールの利用
        instance_LLMmodele=SQLDatabaseChain_LLMmodels()
        chain=instance_LLMmodele.select_SQLDatabaseChain_model(
            db_path,temperature
            )
        
    elif rag_method=="Langchain create_sql_agent":
        #
        print("test")
        
    elif rag_method=="OpenAI codeInterpreter":
        #
        print("test")
        
    #メイン画面の表示
    options_view_main(image_file_pass,chain)

#####################################################
# 　メイン画面
#####################################################
def options_view_main(image_file_pass,llm_model):
    st.title("SQL AGENT app")

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

    # # チャット履歴をセッションで管理
    # if "chat_history" not in st.session_state:
    #     st.session_state["chat_history"] = []
    
    # セッション状態の初期化
    if "messages" not in st.session_state:
        st.session_state.messages = []  # メッセージを保存するためのリスト

    # ユーザーからの入力
    user_input = st.text_input("メッセージを入力してください:", "")
    if user_input:
        # 入力メッセージを履歴に追加
        #st.session_state["chat_history"].append(f"User: {user_input}")
        st.session_state.messages.append(f"User: {user_input}")
        with st.spinner("ChatGPT is typing ..."):
            #コストを計上する場合に利用
            #with get_openai_callback() as cb:
                #response = chain.invoke({"input": st.session_state.messages})
                response = llm_model.invoke({"input": st.session_state.messages})
                response=response["parsed_output"]
        st.session_state.messages.append(f"Agent: {response}")  # 仮の応答

    # チャット履歴を表示
    for message in st.session_state.messages:
        st.write(message)


#####################################################
# サイドバー
#####################################################
def options_view_sidebar():
    st.sidebar.title("設定")
    # DBパスを入力するテキストボックス
    db_path = st.sidebar.text_input("DBの絶対パスを入力してください:", "")

    # 画像フォルダを指定するテキストボックス
    image_file_pass = st.sidebar.text_input("表示したい画像ファイルの絶対パスを入力してください:", "")

    # ラジオボタンでSQL RAGの手法を選択
    rag_method = st.sidebar.radio(
        "SQL RAGの手法を選択してください:",
        [
            "LLM Nomal chat",
            "Langchain SQLDatabaseChain",
            "Langchain create_sql_agent",
            "OpenAI codeInterpreter",
        ]
    )

    #LLMの設定
    # サイドバーにスライダーを追加し、temperatureを0から2までの範囲で選択可能にする
    # 初期値は0.0、刻み幅は0.1とする
    temperature = st.sidebar.slider("Temperature:", min_value=0.0, max_value=2.0, value=0.0, step=0.1)
    # サイドバーにテキスト入力ウィジェットを追加
    opt_system_prompt = st.sidebar.text_input("Enter the system prompt:")
    
    # チャット履歴を削除するボタン
    if st.sidebar.button("チャット履歴を削除"):
        st.session_state["chat_history"] = []  # 履歴をリセット
        st.sidebar.success("チャット履歴が削除されました！")
    
    return db_path,image_file_pass,rag_method,temperature,opt_system_prompt

# サイドバー：モデルの選択
def select_model(temperature):
    # モデルの選択・設定
    model = "GPT-3.5"
    model_name = "gpt-3.5-turbo"
    
    return ChatOpenAI(openai_api_key=input_openai_api_key,temperature=temperature, model_name=model_name,streaming=True)


# ====================================
# プログラムの実行
# ====================================
if __name__ == '__main__':
    main()