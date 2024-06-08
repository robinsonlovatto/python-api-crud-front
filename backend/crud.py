from sqlalchemy.orm import Session
from schemas import ProductUpdate, ProductCreate
from models import ProductModel

# get all
def get_products(db: Session):
    """ Returns all products """
    return db.query(ProductModel).all()

# get one
def get_product(db: Session, product_id: int):
    """ Returns the product that matches with the argument product_id """
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()

# insert one
def create_product(db: Session, product: ProductCreate):
    
    # transform schema (pydantic model) data to model data (sqlalchemy)
    db_product = ProductModel(**product.model_dump())

    db.add(db_product)
    db.commit()

    # refresh db_product with the values created in db (id and created_at)
    db.refresh(db_product)

    return db_product

# update one
def update_product(product_id: int, product: ProductUpdate, db: Session):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    
    if db_product is None:
        return None
    
    if product.name is not None:
        db_product.name = product.name

    if product.description is not None:
        db_product.description = product.description

    if product.price is not None:
        db_product.price = product.price

    if product.category is not None:
        db_product.category = product.category

    if product.supplier_email is not None:
        db_product.supplier_email = product.supplier_email
    
    db.commit()
    db.refresh(db_product)

    return db_product


# delete one
def delete_product(db: Session, product_id: int):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    db.delete(db_product)
    db.commit()

    return db_product