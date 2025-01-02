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
    ####ここから！！！