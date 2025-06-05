from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv
import os

# .envファイルから環境変数を読み込む
load_dotenv()

# .envファイルからデータベース接続情報を取得
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")  # デフォルト3306
DB_NAME = os.getenv("DB_NAME")

# MySQL接続URLを構築
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemyのエンジンとセッションを作成
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデル定義で継承するベースクラス
Base = declarative_base()

#DBのテスト用
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
