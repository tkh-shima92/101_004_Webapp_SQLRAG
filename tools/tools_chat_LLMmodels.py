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
# 定数定義
# ====================================
# def __init__(self, color, model):
# # 設定ファイルの読み込み
# config = configparser.ConfigParser() #Configのハンドル設定
# config.read(".././private/config.ini")

# #OpenAI部分の設定参照
# openai_config = config["OPENAI"] 
# input_openai_api_key = openai_config["OPENAI_API_KEY"]


