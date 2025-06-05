# ###バックエンドで取引合計の計算

# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app import models, schemas, database

# router = APIRouter()
# get_db = database.get_db

# # -------------------------------
# # 1. 商品マスタ登録
# # -------------------------------
# @router.post("/products", response_model=schemas.Product)
# def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
#     existing = db.query(models.Product).filter(models.Product.CODE == product.CODE).first()
#     if existing:
#         raise HTTPException(status_code=400, detail="この商品コードはすでに登録されています")

#     db_product = models.Product(**product.model_dump())
#     db.add(db_product)
#     db.commit()
#     db.refresh(db_product)
#     return db_product

# # -------------------------------
# # 2. 商品コードで商品を取得
# # -------------------------------
# @router.get("/products/{code}", response_model=schemas.Product)
# def get_product(code: str, db: Session = Depends(get_db)):
#     product = db.query(models.Product).filter(models.Product.CODE == code).first()
#     if not product:
#         raise HTTPException(status_code=404, detail="商品マスタが未登録です")
#     return product

# # -------------------------------
# # 3. 取引新規登録（明細なし）
# # -------------------------------
# @router.post("/trades", response_model=schemas.Trade)
# def create_trade(trade_data: schemas.TradeCreate, db: Session = Depends(get_db)):
#     db_trade = models.Trade(
#         EMP_CD=trade_data.EMP_CD,
#         STORE_CD=trade_data.STORE_CD,
#         POS_NO=trade_data.POS_NO,
#         TOTAL_AMT=trade_data.TOTAL_AMT,
#     )
#     db.add(db_trade)
#     db.flush()  # TRD_ID を取得（commit しなくても使えるように）

#     db.commit()
#     db.refresh(db_trade)
#     return db_trade

# # -------------------------------
# # 4. 明細追加（商品コードから）
# # -------------------------------
# @router.post("/trades/{trd_id}/details", response_model=schemas.Detail)
# def add_detail_to_trade(trd_id: int, detail_data: schemas.DetailCreate, db: Session = Depends(get_db)):
#     trade = db.query(models.Trade).filter(models.Trade.TRD_ID == trd_id).first()
#     if not trade:
#         raise HTTPException(status_code=404, detail="取引が見つかりません")

#     product = db.query(models.Product).filter(models.Product.CODE == detail_data.PRD_CODE).first()
#     if not product:
#         raise HTTPException(status_code=404, detail="商品マスタが未登録です")

#     max_dtl_id = db.query(models.Detail)\
#         .filter(models.Detail.TRD_ID == trd_id)\
#         .order_by(models.Detail.DTL_ID.desc())\
#         .with_entities(models.Detail.DTL_ID)\
#         .first()

#     new_dtl_id = 1 if max_dtl_id is None else max_dtl_id[0] + 1

#     db_detail = models.Detail(
#         TRD_ID=trd_id,
#         DTL_ID=detail_data.DTL_ID,
#         PRD_ID=product.PRD_ID,
#         PRD_CODE=product.CODE,
#         PRD_NAME=product.NAME,
#         PRD_PRICE=product.PRICE,
#     )

#     db.add(db_detail)
#     db.commit()
#     db.refresh(db_detail)
#     return db_detail

# # -------------------------------
# # 5. 取引取得（明細含む）
# # -------------------------------
# @router.get("/trades/{trd_id}", response_model=schemas.Trade)
# def get_trade(trd_id: int, db: Session = Depends(get_db)):
#     trade = db.query(models.Trade).filter(models.Trade.TRD_ID == trd_id).first()
#     if not trade:
#         raise HTTPException(status_code=404, detail="取引が見つかりません")
#     return trade

# # -------------------------------
# # 6. 明細一覧取得（取引ごと）
# # -------------------------------
# @router.get("/trades/{trd_id}/details", response_model=list[schemas.Detail])
# def get_trade_details(trd_id: int, db: Session = Depends(get_db)):
#     details = db.query(models.Detail).filter(models.Detail.TRD_ID == trd_id).all()
#     return details

# # -------------------------------
# # 7. 合計金額の再計算
# # -------------------------------
# @router.put("/trades/{trd_id}/recalculate", response_model=schemas.Trade)
# def recalculate_total_amount(trd_id: int, db: Session = Depends(get_db)):
#     trade = db.query(models.Trade).filter(models.Trade.TRD_ID == trd_id).first()
#     if not trade:
#         raise HTTPException(status_code=404, detail="取引が見つかりません")

#     details = db.query(models.Detail).filter(models.Detail.TRD_ID == trd_id).all()
#     total = sum(detail.PRD_PRICE for detail in details)

#     trade.TOTAL_AMT = total
#     db.commit()
#     db.refresh(trade)
#     return trade








from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter()
get_db = database.get_db

# 1. 商品マスタ登録
@router.post("/products", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Product).filter(models.Product.CODE == product.CODE).first()
    if existing:
        raise HTTPException(status_code=400, detail="この商品コードはすでに登録されています")
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# 2. 商品コードで商品を取得
@router.get("/products/{code}", response_model=schemas.Product)
def get_product(code: str, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.CODE == code).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品マスタが未登録です")
    return product

# 3. 取引新規登録（明細含めて一括で受け取り）
@router.post("/trades", response_model=schemas.Trade)
def create_trade(trade_data: schemas.TradeCreate, db: Session = Depends(get_db)):
    db_trade = models.Trade(
        EMP_CD="99999",         #trade_data.EMP_CD,
        STORE_CD="30",         #trade_data.STORE_CD,
        POS_NO="90",           #trade_data.POS_NO,
        TOTAL_AMT=trade_data.TOTAL_AMT,
    )
    db.add(db_trade)
    db.flush()  # TRD_ID を取得

    # 明細を一括登録
    for i, detail in enumerate(trade_data.details, start=1):
        product = db.query(models.Product).filter(models.Product.CODE == detail.PRD_CODE).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"商品コード {detail.PRD_CODE} が未登録です")

        db_detail = models.Detail(
            TRD_ID=db_trade.TRD_ID,
            DTL_ID=i,
            PRD_ID=product.PRD_ID,
            PRD_CODE=product.CODE,
            PRD_NAME=product.NAME,
            PRD_PRICE=product.PRICE
        )
        db.add(db_detail)

    db.commit()
    db.refresh(db_trade)
    return db_trade

# 4. 取引取得（明細含む）
@router.get("/trades/{trd_id}", response_model=schemas.Trade)
def get_trade(trd_id: int, db: Session = Depends(get_db)):
    trade = db.query(models.Trade).filter(models.Trade.TRD_ID == trd_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="取引が見つかりません")
    return trade

# 5. 明細一覧取得（取引ごと）
@router.get("/trades/{trd_id}/details", response_model=list[schemas.Detail])
def get_trade_details(trd_id: int, db: Session = Depends(get_db)):
    details = db.query(models.Detail).filter(models.Detail.TRD_ID == trd_id).all()
    return details

# 6. 合計金額の再計算
@router.put("/trades/{trd_id}/recalculate", response_model=schemas.Trade)
def recalculate_total_amount(trd_id: int, db: Session = Depends(get_db)):
    trade = db.query(models.Trade).filter(models.Trade.TRD_ID == trd_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="取引が見つかりません")
    details = db.query(models.Detail).filter(models.Detail.TRD_ID == trd_id).all()
    trade.TOTAL_AMT = sum(detail.PRD_PRICE for detail in details)
    db.commit()
    db.refresh(trade)
    return trade
