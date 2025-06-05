from pydantic import BaseModel, Field, constr
from typing import List
from datetime import datetime

# 入力用：商品登録
class ProductCreate(BaseModel):
    CODE: constr(min_length=1, max_length=13)
    NAME: constr(min_length=1, max_length=50)
    PRICE: int = Field(gt=0, description="価格は0より大きくしてください")

# 出力用：商品取得
class Product(ProductCreate):
    PRD_ID: int

    model_config = {
        "from_attributes": True
    }

# 入力用：明細登録
class DetailCreate(BaseModel):
    DTL_ID: int
    PRD_ID: int
    PRD_CODE: constr(min_length=1, max_length=13)
    PRD_NAME: constr(min_length=1, max_length=50)
    PRD_PRICE: int = Field(gt=0)

# 出力用：明細取得
class Detail(DetailCreate):
    TRD_ID: int

    model_config = {
        "from_attributes": True
    }

# 入力用：取引登録
class TradeCreate(BaseModel):
    # EMP_CD: constr(min_length=1, max_length=10)
    # STORE_CD: constr(min_length=1, max_length=5)
    # POS_NO: constr(min_length=1, max_length=3)
    TOTAL_AMT: int = Field(ge=0)
    details: List[DetailCreate]

# 出力用：取引取得
class Trade(BaseModel):
    TRD_ID: int
    DATETIME: datetime
    EMP_CD: str
    STORE_CD: str
    POS_NO: str
    TOTAL_AMT: int
    details: List[Detail]

    model_config = {
        "from_attributes": True
    }
