from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models, database
from app.api import router as api_router

# DBテーブルを作成
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# CORS設定（フロントエンドが別ドメインで動く場合）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app-step4-36.azurewebsites.net"],  # 本番は限定ドメインにするのが安全
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーティング
app.include_router(api_router)
