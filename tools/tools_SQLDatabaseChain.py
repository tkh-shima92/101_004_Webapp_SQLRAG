#LLMモデルによるSQL RAG機能モジュール
#Pythonの標準的なモジュールインポート機能により利用
#SQLDatabaseChainライブラリ

#####################################################
#ライブラリインポート
#####################################################
import configparser
#from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import PromptTemplate
import sqlite3

#BaseCacheライブラリ関連
#BaseCacheライブラリがない、というエラー
#->下記では解消されなかった
#from langchain.cache import BaseCache
#from langchain_core.caches import BaseCache
#BaseCacheライブラリがない、というエラー
#->以前、「test_ipynb」で試した際は上記エラーはなかったため、同じライブラリをインポートしたところエラー解消
#確認の結果、以下のいずれでもエラーは解消された
#したがって、「langchain.agents」に上記ライブラリが同封されていそう
#from langchain.agents import create_sql_agent
#from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
# ====================================
# クラス設定・初期設定
# ====================================
class SQLDatabaseChain_LLMmodels:
    # ====================================
    # 初期設定
    # ====================================
    def __init__(self):
        # 設定ファイルの読み込み
        config = configparser.ConfigParser() #Configのハンドル設定
        config.read("./private/config.ini") #main.pyからの相対パス

        #OpenAI部分の設定参照   
        openai_config = config["OPENAI"] 
        self.input_openai_api_key = openai_config["OPENAI_API_KEY"]
    
    # ====================================
    # LLMモデルの設定
    # ====================================
    def select_SQLDatabaseChain_model(self,db_path,temperature):
        
        #データベースとモデルの設定
        # db = SQLDatabase.from_uri("sqlite:///.././db/chinook.db")
        db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
        
        #システムプロンプトの設定
        #対象DB情報　※システムプロンプト用に設定。システムによっては動的に設定が望ましい
        #table_info = self.get_table_info_from_db(db_path)
        dialect = "SQLite"
        
        #プロンプト作成
        #以下ではSQLAlchemyがSQL以外の文章をSQLと認識してしまうため不採用
        # _DEFAULT_TEMPLATE = """
        # 入力された質問に基づき、まず文法的に正しい {dialect} クエリを作成してください。
        # その後、クエリの結果を確認し、最終的な回答を返してください。
        # 回答にあたっては日本語を使用してください。
        # 以下の形式を使用してください:

        # 質問: "ここに質問を記載"
        # SQLクエリ: "実行するSQLクエリ"

        # 質問: {input}
        # """
        
        _DEFAULT_TEMPLATE = """
        以下の質問についてSQLの実行結果を踏まえて日本語で回答してください。
        質問:{input} 
        """
        
        PROMPT = PromptTemplate(
            #input_variables=["input", "table_info", "dialect"], 
            input_variables=["input", "dialect"], 
            template=_DEFAULT_TEMPLATE
            )
        
        #チェーンの作成
        llm = ChatOpenAI(
            openai_api_key=self.input_openai_api_key,
            temperature=temperature,
            model_name="gpt-3.5-turbo",
            streaming=True,
            )
        
        SQLDatabaseChain.model_rebuild() 
        
        return SQLDatabaseChain.from_llm(
            llm,
            db,
            #prompt=PROMPT,
            verbose=True,
            return_intermediate_steps=True
            )
        
        #return SQLDatabaseChain(llm=llm, database=db, verbose=True, use_cache=False)
        
    # ====================================
    # テーブル情報の取得関数
    # ====================================
    def get_table_info_from_db(self,db_path):
        """
        SQLiteデータベースからテーブル情報を動的に取得し、フォーマットする関数。        
        Parameters:
            db_path (str): SQLiteデータベースのパス。
        Returns:
            str: テーブルとその列情報をフォーマットした文字列。
        """
        try:
            # データベースに接続
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # データベース内のテーブル名を取得
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            # テーブル情報を格納するリスト
            table_info_list = []

            # 各テーブルの列情報を取得
            for table_name in tables:
                table_name = table_name[0]  # タプルからテーブル名を取り出す
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()

                # 列情報を "name (type)" の形式でフォーマット
                column_info = ", ".join([f"{col[1]} ({col[2]})" for col in columns])

                # "table_name: column_info" の形式でリストに追加
                table_info_list.append(f"{table_name} テーブル ({column_info})")

            # テーブル情報を結合して返す
            return "\n".join(table_info_list)

        except sqlite3.Error as e:
            return f"エラー: データベース情報を取得できませんでした。{e}"

        finally:
            if conn:
                conn.close()