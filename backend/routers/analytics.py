from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import get_db
import models
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    
    # Orders today
    today = datetime.now().date()
    orders_today = db.query(models.Order).filter(
        func.date(models.Order.created_at) == today
    ).count()
    
    # Total revenue
    total_revenue = db.query(func.sum(models.Order.total_amount)).scalar() or 0
    
    # Total orders
    total_orders = db.query(models.Order).count()
    
    # Total customers
    total_customers = db.query(models.Customer).count()
    
    # Total products
    total_products = db.query(models.Product).count()
    
    # Low stock count (less than 10)
    low_stock_count = db.query(models.Product).filter(
        models.Product.stock_quantity < 10
    ).count()
    
    # Top 5 products by order count
    top_products = db.query(
        models.Product.name,
        func.count(models.OrderItem.id).label('order_count'),
        func.sum(models.OrderItem.quantity).label('total_quantity')
    ).join(
        models.OrderItem
    ).group_by(
        models.Product.name
    ).order_by(
        func.count(models.OrderItem.id).desc()
    ).limit(5).all()
    
    return {
        "orders_today": orders_today,
        "total_revenue": float(total_revenue),
        "total_orders": total_orders,
        "total_customers": total_customers,
        "total_products": total_products,
        "low_stock_count": low_stock_count,
        "top_products": [
            {
                "name": p.name,
                "order_count": p.order_count,
                "total_quantity": p.total_quantity
            }
            for p in top_products
        ]
    }


@router.get("/revenue-by-day")
def get_revenue_by_day(days: int = 7, db: Session = Depends(get_db)):
    """Get revenue for last N days"""
    
    start_date = datetime.now() - timedelta(days=days)
    
    revenue_by_day = db.query(
        func.date(models.Order.created_at).label('date'),
        func.sum(models.Order.total_amount).label('revenue'),
        func.count(models.Order.id).label('order_count')
    ).filter(
        models.Order.created_at >= start_date
    ).group_by(
        func.date(models.Order.created_at)
    ).all()
    
    return [
        {
            "date": str(r.date),
            "revenue": float(r.revenue or 0),
            "order_count": r.order_count
        }
        for r in revenue_by_day
    ]
