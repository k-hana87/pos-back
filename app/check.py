from database import SessionLocal
from sqlalchemy import text

def check_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))  # 簡単なSQLで接続確認
        print("データベース接続に成功しました！")
    except Exception as e:
        print("接続エラー:", e)
    finally:
        db.close()

if __name__ == "__main__":
    check_connection()
