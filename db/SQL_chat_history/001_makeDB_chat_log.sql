-- 実行方法
-- cmdでDB起動+クエリ実行
-- SQLite3 ..\chat_log.db
-- .read 001_makeDB_chat_log.sql

-- 1. 新しいテーブルを作成
CREATE TABLE chat_history_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    answer TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 参考：データバックアップを行う場合
-- 2. 既存データを新しいテーブルに移行
-- INSERT INTO chat_history_new (id, query, answer)
-- SELECT id, query, answer
-- FROM User;

-- 3. 古いテーブルを削除
DROP TABLE test01;

-- 4. 新しいテーブルをリネーム
ALTER TABLE chat_history_new RENAME TO chat_history_01;
