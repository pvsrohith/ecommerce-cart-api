from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ecommerce Cart API")

def compute_total(cart: models.Cart) -> float:
    return sum(item.product.price * item.quantity for item in cart.items)

@app.get("/")
def root():
    return {"status": "ok", "service": "ecommerce-cart-api"}

@app.post("/products", response_model=schemas.ProductOut)
def create_product(payload: schemas.ProductCreate, db: Session = Depends(get_db)):
    product = models.Product(**payload.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@app.get("/products", response_model=list[schemas.ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@app.post("/carts", response_model=schemas.CartOut)
def create_cart(db: Session = Depends(get_db)):
    cart = models.Cart()
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return schemas.CartOut(id=cart.id, created_at=cart.created_at, items=[], total=0)

def get_cart_or_404(cart_id: int, db: Session) -> models.Cart:
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

@app.get("/carts/{cart_id}", response_model=schemas.CartOut)
def get_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = get_cart_or_404(cart_id, db)
    total = compute_total(cart)
    return schemas.CartOut(id=cart.id, created_at=cart.created_at, items=cart.items, total=total)

@app.post("/carts/{cart_id}/items", response_model=schemas.CartOut)
def add_item(cart_id: int, payload: schemas.CartItemCreate, db: Session = Depends(get_db)):
    cart = get_cart_or_404(cart_id, db)
    product = db.query(models.Product).filter(models.Product.id == payload.product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    item = models.CartItem(cart_id=cart.id, product_id=product.id, quantity=payload.quantity)
    db.add(item)
    db.commit()
    db.refresh(cart)
    total = compute_total(cart)
    return schemas.CartOut(id=cart.id, created_at=cart.created_at, items=cart.items, total=total)

@app.post("/carts/{cart_id}/checkout", response_model=schemas.OrderOut)
def checkout(cart_id: int, db: Session = Depends(get_db)):
    cart = get_cart_or_404(cart_id, db)
    if not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    for item in cart.items:
        if item.product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for {item.product.name}")

    total = compute_total(cart)
    for item in cart.items:
        item.product.stock -= item.quantity

    order = models.Order(cart_id=cart.id, total=total)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
