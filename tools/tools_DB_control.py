#LLMモデルによるSQL RAG機能モジュール
#Pythonの標準的なモジュールインポート機能により利用
#会話履歴の保管用のSQLiteの操作用ライブラリ

#####################################################
#ライブラリインポート
#####################################################
import sqlite3

# ====================================
# クラス設定・初期設定
# ====================================
class DBtool_SQLite3:
    # ====================================
    # 初期設定　DBの設定
    # ====================================
    def __init__(self):
        self.output_DB_pass="./db/chat_log.db"
        self.output_DB_name_table="chat_history_01"
        self.output_DB_name_table_Q="query"
        self.output_DB_name_table_A="answer"
 
    # ====================================
    # データベース接続関数
    # ====================================
    def save_to_db(self,question="No Question", answer="No Answer"):
        conn = sqlite3.connect(self.output_DB_pass)
        cursor = conn.cursor()

        # データ挿入
        make_SQL_query=f"INSERT INTO {self.output_DB_name_table} ({self.output_DB_name_table_Q}, {self.output_DB_name_table_A}) VALUES (?, ?)"
        cursor.execute(make_SQL_query, (question, answer))
        conn.commit()
        conn.close()