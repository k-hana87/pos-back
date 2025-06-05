from sqlalchemy.orm import Session
from your_database_file import SessionLocal
from models import Product

def fetch_and_print_products():
    db: Session = SessionLocal()
    try:
        products = db.query(Product).all()
        for product in products:
            print(f"ID: {product.id}, Code: {product.code}, Name: {product.name}, Price: {product.price}")
    finally:
        db.close()

if __name__ == "__main__":
    fetch_and_print_products()
