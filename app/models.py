from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

# 商品マスタテーブル
class Product(Base):
    __tablename__ = "products"

    PRD_ID = Column(Integer, primary_key=True, index=True)
    CODE = Column(String(13), unique=True, nullable=False)
    NAME = Column(String(50), nullable=False)
    PRICE = Column(Integer, nullable=False)

    details = relationship("Detail", back_populates="product")


# 取引テーブル
class Trade(Base):
    __tablename__ = "trades"

    TRD_ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    DATETIME = Column(DateTime, default=datetime.utcnow)
    EMP_CD = Column(String(10), nullable=False)
    STORE_CD = Column(String(5), nullable=False)
    POS_NO = Column(String(3), nullable=False)
    TOTAL_AMT = Column(Integer, nullable=False)

    details = relationship("Detail", back_populates="trade")


# 取引明細テーブル
class Detail(Base):
    __tablename__ = "details"

    TRD_ID = Column(Integer, ForeignKey("trades.TRD_ID"), primary_key=True)
    DTL_ID = Column(Integer, primary_key=True)
    PRD_ID = Column(Integer, ForeignKey("products.PRD_ID"))
    PRD_CODE = Column(String(13), nullable=False)
    PRD_NAME = Column(String(50), nullable=False)
    PRD_PRICE = Column(Integer, nullable=False)

    trade = relationship("Trade", back_populates="details")
    product = relationship("Product", back_populates="details")
