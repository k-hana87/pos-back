# バックエンド（FastAPI）構成

このディレクトリには FastAPI を使った API サーバーが含まれています。商品コードに応じた商品名と金額を取得する機能を提供します。

## ディレクトリ構成

back/
├── app/
│    ├── main.py  # FastAPIアプリ本体
│    ├── api.py # 商品に関するAPIルーター
│    ├── database.py # DB接続の設定
│    ├── models.py # 商品モデル（SQLAlchemy）
│    └── schemas.py # Pydanticスキーマ
├── .env # DB接続情報などの環境変数
├── requirements.txt # 使用ライブラリの一覧
└── README.md # この説明ファイル



【本来はこちらがベスト】
back/
├── app/
│ ├── api/
│ │ └── products.py 
│ ├── db/
│ │ ├── models.py 
│ │ └── database.py 
│ ├── schemas/
│ │ └── product.py 
│ └── main.py
├── .env # DB接続情報などの環境変数
├── requirements.txt # 使用ライブラリの一覧
└── README.md # この説明ファイル