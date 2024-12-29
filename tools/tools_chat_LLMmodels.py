#LLMモデルとのチャット機能モジュール
#Pythonの標準的なモジュールインポート機能により利用

#####################################################
#ライブラリインポート
#####################################################
import configparser
from langchain.chat_models import ChatOpenAI
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain



#テスト
def test_hello():
    print_hello='Hello!!!'
    return print_hello

# ====================================
# クラス設定・初期設定
# ====================================
class chat_LLMmodels:
    def __init__(self):
        # 設定ファイルの読み込み
        config = configparser.ConfigParser() #Configのハンドル設定
        config.read("./private/config.ini")

        #OpenAI部分の設定参照   
        openai_config = config["OPENAI"] 
        self.input_openai_api_key = openai_config["OPENAI_API_KEY"]

    # ====================================
    # LLMモデルの設定
    # ====================================
    def select_chatmodel(self,temperature):
        # モデルの選択・設定
        model = "GPT-3.5"
        model_name = "gpt-3.5-turbo"
        
        return ChatOpenAI(openai_api_key=self.input_openai_api_key,temperature=temperature, model_name=model_name,streaming=True)
