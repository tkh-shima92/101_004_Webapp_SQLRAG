#LLMモデルによるSQL RAG機能モジュール
#Pythonの標準的なモジュールインポート機能により利用
#create_sql_agentライブラリ

#####################################################
#ライブラリインポート
#####################################################
import configparser
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.sql_database import SQLDatabase

# ====================================
# クラス設定・初期設定
# ====================================
class create_sql_agent_LLMmodels:
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
    def select_create_sql_agent_model(self,db_path,temperature):
        #データベースとモデルの設定
        db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
        
        llm = ChatOpenAI(
            openai_api_key=self.input_openai_api_key,
            temperature=temperature,
            model_name="gpt-3.5-turbo",
            streaming=True
            )
        
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        
        return create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            )