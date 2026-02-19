from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import models
from database import get_db

router = APIRouter()

@router.get("/", summary="Get all orders")
def get_all_orders(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Retrieve all orders with pagination.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    """
    orders = db.query(models.Order).offset(skip).limit(limit).all()
    return orders


@router.get("/{order_id}", summary="Get single order")
def get_order(order_id: int, db: Session = Depends(get_db)):
    """
    Get a single order by ID with all its items and customer info.
    """
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/", summary="Create new order")
def create_order(
    customer_id: int,
    items: List[dict],  # [{"product_id": 1, "quantity": 2}, ...]
    db: Session = Depends(get_db)
):
    """
    Create a new order with items.
    
    - **customer_id**: ID of the customer placing the order
    - **items**: List of items with product_id and quantity
    
    Example:
    ```json
    {
        "customer_id": 1,
        "items": [
            {"product_id": 1, "quantity": 2},
            {"product_id": 3, "quantity": 1}
        ]
    }
    ```
    """
    # Verify customer exists
    customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Create order
    order = models.Order(
        customer_id=customer_id,
        order_number=f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        status="pending",
        total_amount=0
    )
    db.add(order)
    db.flush()  # Get order.id before adding items
    
    # Add order items and calculate total
    total = 0
    for item_data in items:
        product = db.query(models.Product).filter(
            models.Product.id == item_data['product_id']
        ).first()
        
        if not product:
            raise HTTPException(
                status_code=404, 
                detail=f"Product {item_data['product_id']} not found"
            )
        
        # Check stock
        if product.stock_quantity < item_data['quantity']:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.name}"
            )
        
        subtotal = product.current_price * item_data['quantity']
        
        order_item = models.OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item_data['quantity'],
            unit_price=product.current_price,
            subtotal=subtotal
        )
        db.add(order_item)
        
        # Update stock
        product.stock_quantity -= item_data['quantity']
        
        total += subtotal
    
    # Update order total
    order.total_amount = total
    
    db.commit()
    db.refresh(order)
    
    return order


@router.put("/{order_id}/status", summary="Update order status")
def update_order_status(
    order_id: int, 
    status: str,  # pending, processing, shipped, delivered, cancelled
    db: Session = Depends(get_db)
):
    """
    Update the status of an order.
    
    Valid statuses: pending, processing, shipped, delivered, cancelled
    """
    valid_statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400, 
            detail=f"Status must be one of: {', '.join(valid_statuses)}"
        )
    
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = status
    db.commit()
    db.refresh(order)
    
    return order


@router.get("/customer/{customer_id}", summary="Get customer orders")
def get_customer_orders(
    customer_id: int, 
    db: Session = Depends(get_db)
):
    """
    Get all orders for a specific customer.
    """
    orders = db.query(models.Order).filter(
        models.Order.customer_id == customer_id
    ).all()
    return orders


@router.delete("/{order_id}", summary="Delete order")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """
    Delete an order (only if status is 'pending').
    This also restores product stock quantities.
    """
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status != "pending":
        raise HTTPException(
            status_code=400, 
            detail="Can only delete pending orders"
        )
    
    # Restore stock for all items
    for item in order.items:
        product = db.query(models.Product).filter(
            models.Product.id == item.product_id
        ).first()
        if product:
            product.stock_quantity += item.quantity
    
    # Delete order items first (foreign key constraint)
    db.query(models.OrderItem).filter(
        models.OrderItem.order_id == order_id
    ).delete()
    
    # Delete order
    db.delete(order)
    db.commit()
    
    return {"deleted": True, "order_id": order_id}


@router.get("/stats/by-status", summary="Order statistics by status")
def get_order_stats(db: Session = Depends(get_db)):
    """
    Get count of orders grouped by status.
    """
    from sqlalchemy import func
    
    stats = db.query(
        models.Order.status,
        func.count(models.Order.id).label('count'),
        func.sum(models.Order.total_amount).label('total_revenue')
    ).group_by(models.Order.status).all()
    
    return [
        {
            "status": stat.status,
            "count": stat.count,
            "total_revenue": float(stat.total_revenue or 0)
        }
        for stat in stats
    ]
