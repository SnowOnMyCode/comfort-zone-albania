from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Product])
def get_all_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all products with pagination"""
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get single product by ID"""
    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product


@router.post("/", response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db)
):
    """Create new product"""
    # Check if SKU already exists
    existing = db.query(models.Product).filter(
        models.Product.sku == product.sku
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="SKU already exists")
    
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return db_product


@router.put("/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: int,
    product: schemas.ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update product"""
    db_product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()
    
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Update only provided fields
    update_data = product.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    
    return db_product


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete product"""
    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    
    return {"deleted": True, "id": product_id}


@router.post("/bulk-price-update")
def bulk_price_update(
    keyword: str,
    price_change_type: str,  # "percentage" or "fixed"
    value: float,
    db: Session = Depends(get_db)
):
    """
    Update prices for products matching keyword.
    
    - keyword: Search term (searches in name, sku, keywords)
    - price_change_type: "percentage" or "fixed"
    - value: Percentage change or fixed price
    """
    # Search products by keyword
    products = db.query(models.Product).filter(
        (models.Product.name.contains(keyword)) |
        (models.Product.sku.contains(keyword)) |
        (models.Product.keywords.contains(keyword))
    ).all()
    
    if not products:
        return {"updated": 0, "message": f"No products found matching '{keyword}'"}
    
    updated_count = 0
    for product in products:
        if price_change_type == "percentage":
            product.current_price = product.current_price * (1 + value / 100)
        elif price_change_type == "fixed":
            product.current_price = value
        else:
            raise HTTPException(
                status_code=400,
                detail="price_change_type must be 'percentage' or 'fixed'"
            )
        updated_count += 1
    
    db.commit()
    
    return {
        "updated": updated_count,
        "keyword": keyword,
        "message": f"Updated {updated_count} products"
    }


@router.get("/search/{search_term}")
def search_products(search_term: str, db: Session = Depends(get_db)):
    """Search products by name, SKU, or keywords"""
    search_pattern = f"%{search_term}%"
    
    products = db.query(models.Product).filter(
        (models.Product.name.ilike(search_pattern)) |
        (models.Product.sku.ilike(search_pattern)) |
        (models.Product.keywords.ilike(search_pattern))
    ).all()
    
    return products
