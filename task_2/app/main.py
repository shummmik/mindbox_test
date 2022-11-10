from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session, joinedload
import database
import models
import schemas

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/products', response_model=list[schemas.ProductOut])
def get_products(skip: int = 1, limit: int = 100, db: Session = Depends(get_db)):
    if 100 < limit < 1:
        limit = 100
    if skip < 1:
        skip = 1
    products = db.query(models.Product).options(joinedload(models.Product.categories)) \
        .offset((skip - 1) * limit).limit(limit).all()
    return products


@app.get('/categories', response_model=list[schemas.CategoryOut])
def get_categories(skip: int = 1, limit: int = 100, db: Session = Depends(get_db)):
    if 100 < limit < 1:
        limit = 100
    if skip < 1:
        skip = 1
    categories = db.query(models.Category).options(joinedload(models.Category.products)) \
        .offset((skip - 1) * limit).limit(limit).all()
    return categories


@app.get('/pairs', response_model=list[schemas.Pairs])
def get_pairs(skip: int = 1, limit: int = 100, db: Session = Depends(get_db)):
    if 100 < limit < 1:
        limit = 100
    if skip < 1:
        skip = 1
    pairs = db.query(models.ProductCategory).join(models.ProductCategory.category).join(
        models.ProductCategory.product).offset((skip - 1) * limit).limit(limit).all()
    print(schemas.Pairs.from_orm(pairs[0]))
    return pairs
