from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import models
from database import get_db

router = APIRouter()

@router.get("/", summary="Get all customers")
def get_all_customers(
    skip: int = 0,
    limit: int = 100,
    customer_type: Optional[str] = None,  # Filter by type: hotel, hairdresser, pharmacy
    db: Session = Depends(get_db)
):
    """
    Retrieve all customers with optional filtering.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **customer_type**: Filter by type (hotel, hairdresser, pharmacy)
    """
    query = db.query(models.Customer)
    
    if customer_type:
        query = query.filter(models.Customer.type == customer_type)
    
    customers = query.offset(skip).limit(limit).all()
    return customers


@router.get("/{customer_id}", summary="Get single customer")
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Get a single customer by ID.
    """
    customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return customer


@router.post("/", summary="Create new customer")
def create_customer(
    name: str,
    type: str,  # hotel, hairdresser, pharmacy
    email: str,
    phone: str,
    address: str,
    tax_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Create a new customer.
    
    - **name**: Customer business name
    - **type**: Type of business (hotel, hairdresser, pharmacy)
    - **email**: Contact email
    - **phone**: Contact phone
    - **address**: Business address
    - **tax_id**: Tax identification number (optional)
    
    Example:
    ```json
    {
        "name": "Grand Hotel Plaza",
        "type": "hotel",
        "email": "contact@grandhotel.com",
        "phone": "+1234567890",
        "address": "123 Main St, City",
        "tax_id": "TAX123456"
    }
    ```
    """
    # Validate customer type
    valid_types = ["hotel", "hairdresser", "pharmacy"]
    if type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Type must be one of: {', '.join(valid_types)}"
        )
    
    # Check if email already exists
    existing = db.query(models.Customer).filter(
        models.Customer.email == email
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Customer with this email already exists"
        )
    
    customer = models.Customer(
        name=name,
        type=type,
        email=email,
        phone=phone,
        address=address,
        tax_id=tax_id
    )
    
    db.add(customer)
    db.commit()
    db.refresh(customer)
    
    return customer


@router.put("/{customer_id}", summary="Update customer")
def update_customer(
    customer_id: int,
    name: Optional[str] = None,
    type: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    address: Optional[str] = None,
    tax_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Update customer information.
    Only provided fields will be updated.
    """
    customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Validate type if provided
    if type:
        valid_types = ["hotel", "hairdresser", "pharmacy"]
        if type not in valid_types:
            raise HTTPException(
                status_code=400,
                detail=f"Type must be one of: {', '.join(valid_types)}"
            )
        customer.type = type
    
    # Check email uniqueness if changing
    if email and email != customer.email:
        existing = db.query(models.Customer).filter(
            models.Customer.email == email
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Email already in use"
            )
        customer.email = email
    
    # Update other fields
    if name:
        customer.name = name
    if phone:
        customer.phone = phone
    if address:
        customer.address = address
    if tax_id is not None:  # Allow setting to empty string
        customer.tax_id = tax_id
    
    db.commit()
    db.refresh(customer)
    
    return customer


@router.delete("/{customer_id}", summary="Delete customer")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Delete a customer.
    Cannot delete if customer has existing orders.
    """
    customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Check if customer has orders
    has_orders = db.query(models.Order).filter(
        models.Order.customer_id == customer_id
    ).first()
    
    if has_orders:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete customer with existing orders"
        )
    
    db.delete(customer)
    db.commit()
    
    return {"deleted": True, "customer_id": customer_id}


@router.get("/{customer_id}/orders", summary="Get customer's orders")
def get_customer_orders(customer_id: int, db: Session = Depends(get_db)):
    """
    Get all orders for a specific customer.
    """
    customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    orders = db.query(models.Order).filter(
        models.Order.customer_id == customer_id
    ).all()
    
    return orders


@router.get("/{customer_id}/stats", summary="Customer purchase statistics")
def get_customer_stats(customer_id: int, db: Session = Depends(get_db)):
    """
    Get purchase statistics for a customer.
    """
    from sqlalchemy import func
    
    customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Get order stats
    order_stats = db.query(
        func.count(models.Order.id).label('total_orders'),
        func.sum(models.Order.total_amount).label('total_spent'),
        func.avg(models.Order.total_amount).label('average_order')
    ).filter(models.Order.customer_id == customer_id).first()
    
    # Get most ordered products
    top_products = db.query(
        models.Product.name,
        func.sum(models.OrderItem.quantity).label('total_quantity')
    ).join(models.OrderItem).join(models.Order).filter(
        models.Order.customer_id == customer_id
    ).group_by(models.Product.name).order_by(
        func.sum(models.OrderItem.quantity).desc()
    ).limit(5).all()
    
    return {
        "customer_id": customer_id,
        "customer_name": customer.name,
        "total_orders": order_stats.total_orders or 0,
        "total_spent": float(order_stats.total_spent or 0),
        "average_order": float(order_stats.average_order or 0),
        "top_products": [
            {"product": p.name, "quantity": p.total_quantity}
            for p in top_products
        ]
    }


@router.get("/stats/by-type", summary="Customer statistics by type")
def get_customers_by_type(db: Session = Depends(get_db)):
    """
    Get count of customers grouped by type.
    """
    from sqlalchemy import func
    
    stats = db.query(
        models.Customer.type,
        func.count(models.Customer.id).label('count')
    ).group_by(models.Customer.type).all()
    
    return [
        {"type": stat.type, "count": stat.count}
        for stat in stats
    ]


@router.get("/search/{search_term}", summary="Search customers")
def search_customers(search_term: str, db: Session = Depends(get_db)):
    """
    Search customers by name, email, or phone.
    """
    search_pattern = f"%{search_term}%"
    
    customers = db.query(models.Customer).filter(
        (models.Customer.name.ilike(search_pattern)) |
        (models.Customer.email.ilike(search_pattern)) |
        (models.Customer.phone.ilike(search_pattern))
    ).all()
    
    return customers
