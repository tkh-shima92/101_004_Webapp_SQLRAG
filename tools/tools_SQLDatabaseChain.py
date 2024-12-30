#LLMモデルによるSQL RAG機能モジュール
#Pythonの標準的なモジュールインポート機能により利用

#####################################################
#ライブラリインポート
#####################################################
import configparser
from langchain.chat_models import ChatOpenAI
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

#from langchain.cache import BaseCache
#from langchain_core.caches import BaseCache
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
# ====================================
# クラス設定・初期設定
# ====================================
class SQLDatabaseChain_LLMmodels:
    # ====================================
    # APIキーの設定
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
        
        llm = ChatOpenAI(
            openai_api_key=self.input_openai_api_key,
            temperature=0,
            model_name="gpt-3.5-turbo",
            streaming=True,
            )
        
        SQLDatabaseChain.model_rebuild() 
        
        return SQLDatabaseChain.from_llm(
            llm,
            db,
            verbose=True
            )
        
        #return SQLDatabaseChain(llm=llm, database=db, verbose=True, use_cache=False)