import sqlite3

def save_response(interviewer_id, question_id, answer):
    """
    データベースに応答を保存します。
    :param interviewer_id: 面接官のID
    :param question_id: 質問のID
    :param answer: ユーザーの回答
    """
    conn = sqlite3.connect("responses.db")
    cursor = conn.cursor()

    # テーブルが存在しない場合に作成
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interviewer_id TEXT,
            question_id INTEGER,
            answer TEXT
        )
    """)

    cursor.execute(
        "INSERT INTO responses (interviewer_id, question_id, answer) VALUES (?, ?, ?)",
        (interviewer_id, question_id, answer)
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    save_response("12345", 1, "Pythonとデータ分析が得意です。")
