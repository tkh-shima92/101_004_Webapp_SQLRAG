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
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.runnables import RunnableConfig

#モジュール
#from tools.tools_chat_LLMmodels import test_hello
from tools.tools_chat_LLMmodels import chat_LLMmodels
from tools.tools_SQLDatabaseChain import SQLDatabaseChain_LLMmodels
from tools.tools_create_sql_agent import create_sql_agent_LLMmodels

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
        instance_LLMmodel=SQLDatabaseChain_LLMmodels()
        chain=instance_LLMmodel.select_SQLDatabaseChain_model(
            db_path,temperature
            )
        
    elif rag_method=="Langchain create_sql_agent":
        #外部モジュールの利用
        instance_LLMmodel=create_sql_agent_LLMmodels()
        chain=instance_LLMmodel.select_create_sql_agent_model(
            db_path,temperature
            )
        
    elif rag_method=="OpenAI codeInterpreter":
        #
        print("test")
        
    #メイン画面の表示
    options_view_main(image_file_pass,rag_method,chain)

#####################################################
# 　メイン画面
#####################################################
def options_view_main(image_file_pass,rag_method,llm_model):
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

    # チャット履歴の表示
    messages = st.session_state.get('messages', [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message('assistant'):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message('user'):
                st.markdown(message.content)
        else:  # isinstance(message, SystemMessage):
            st.write(f"System message: {message.content}")

    # チャット履歴を表示 ※JSON形式での確認用
    # for message in st.session_state.messages:
    #     st.write(message)

    # ユーザーからの入力
    #user_input = st.text_input("メッセージを入力してください:", "")
    #if user_input:
    if user_input := st.chat_input("メッセージを入力してください:"):
        # 入力メッセージを履歴に追加
        #st.session_state["chat_history"].append(f"User: {user_input}")
        #st.session_state.messages.append(f"User: {user_input}")
        st.session_state.messages.append(HumanMessage(content=user_input))
        st.chat_message("user").write(user_input)
        
        with st.spinner("ChatGPT is typing ..."):
            #コストを計上する場合に利用
            #with get_openai_callback() as cb:
                #response = chain.invoke({"input": st.session_state.messages})
                if rag_method=="LLM Nomal chat":
                    response = llm_model.invoke({"input": st.session_state.messages})
                    response=response["parsed_output"]
                    #st.session_state.messages.append(f"Agent: {response}") 
                    st.session_state.messages.append(AIMessage(content=response))
                elif rag_method=="Langchain SQLDatabaseChain":
                    #StreamlitCallbackHandlerによるエージェント行動の可視化
                     with st.chat_message("assistant"):
                         st_cb = StreamlitCallbackHandler(
                             st.container(), expand_new_thoughts=True)
                         response = llm_model.invoke(#{"query": st.session_state.messages}
                                                     {"query":user_input}, 
                                                     #callbacks=[st_cb]
                                                     config=RunnableConfig({'callbacks': [st_cb]})
                                                     ) 
                         st.write(response["result"])
                         response_natural_language_output=response["result"]
                         st.session_state.messages.append(AIMessage(content=response_natural_language_output))
                    #コードと実行結果の取り出し
                    # response_SQL_code=response["intermediate_steps"][2]['sql_cmd']
                    #response_SQL_output=response["intermediate_steps"][3]
                    
                elif rag_method=="Langchain create_sql_agent":
                    #StreamlitCallbackHandlerによるエージェント行動の可視化
                     with st.chat_message("assistant"):
                         st_cb = StreamlitCallbackHandler(
                             st.container(), expand_new_thoughts=True)
                         #response = llm_model.run(st.session_state.messages)
                         response = llm_model.invoke({"input":user_input}, 
                                                     config=RunnableConfig({'callbacks': [st_cb]})
                                                     ) 
                         st.write(response["output"])
                         #response=response["result"]
                         #st.session_state.messages.append(f"Agent: {response}")  # 仮の応答
                         st.session_state.messages.append(AIMessage(content=response["output"]))
                
#####################################################
# サイドバー
#####################################################
def options_view_sidebar():
    st.sidebar.title("設定")
    # DBパスを入力するテキストボックス
    #db_path = st.sidebar.text_input("DBの絶対パスを入力してください:", "")
    db_path = "./db/chinook.db"

    # 画像フォルダを指定するテキストボックス
    #image_file_pass = st.sidebar.text_input("表示したい画像ファイルの絶対パスを入力してください:", "")
    image_file_pass = "./db/sqlite-sample-database-color.jpg"

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
    temperature = st.sidebar.slider("Temperature:", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
    # サイドバーにテキスト入力ウィジェットを追加
    opt_system_prompt = st.sidebar.text_input("Enter the system prompt:")
    
    # チャット履歴を削除するボタン
    if st.sidebar.button("チャット履歴を削除"):
        st.session_state.messages = []  # 履歴をリセット
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