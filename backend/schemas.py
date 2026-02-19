from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# ============================================================================
# PRODUCT SCHEMAS
# ============================================================================

class ProductBase(BaseModel):
    name: str
    sku: str
    description: Optional[str] = None
    category: str
    current_price: float
    stock_quantity: int = 0
    keywords: Optional[str] = None

class ProductCreate(ProductBase):
    """Schema for creating a new product"""
    pass

class ProductUpdate(BaseModel):
    """Schema for updating a product (all fields optional)"""
    name: Optional[str] = None
    sku: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    current_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    keywords: Optional[str] = None

class Product(ProductBase):
    """Schema for returning a product"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # Allows reading from SQLAlchemy models


# ============================================================================
# CUSTOMER SCHEMAS
# ============================================================================

class CustomerBase(BaseModel):
    name: str
    type: str  # hotel, hairdresser, pharmacy
    email: EmailStr
    phone: str
    address: str
    tax_id: Optional[str] = None

class CustomerCreate(CustomerBase):
    """Schema for creating a new customer"""
    pass

class CustomerUpdate(BaseModel):
    """Schema for updating a customer (all fields optional)"""
    name: Optional[str] = None
    type: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    tax_id: Optional[str] = None

class Customer(CustomerBase):
    """Schema for returning a customer"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# ORDER ITEM SCHEMAS
# ============================================================================

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    """Schema for creating an order item"""
    pass

class OrderItem(OrderItemBase):
    """Schema for returning an order item"""
    id: int
    order_id: int
    unit_price: float
    subtotal: float
    product: Optional[Product] = None  # Include product details
    
    class Config:
        from_attributes = True


# ============================================================================
# ORDER SCHEMAS
# ============================================================================

class OrderBase(BaseModel):
    customer_id: int

class OrderCreate(BaseModel):
    """Schema for creating a new order"""
    customer_id: int
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    """Schema for updating an order"""
    status: Optional[str] = None

class Order(OrderBase):
    """Schema for returning an order"""
    id: int
    order_number: str
    status: str
    total_amount: float
    created_at: datetime
    customer: Optional[Customer] = None  # Include customer details
    items: List[OrderItem] = []  # Include order items
    
    class Config:
        from_attributes = True


# ============================================================================
# USER SCHEMAS (for authentication)
# ============================================================================

class UserBase(BaseModel):
    email: EmailStr
    role: str = "admin"

class UserCreate(UserBase):
    """Schema for user registration"""
    password: str

class UserUpdate(BaseModel):
    """Schema for updating user"""
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    """Schema for returning a user (no password!)"""
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for login"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token payload"""
    email: Optional[str] = None


# ============================================================================
# ANALYTICS SCHEMAS
# ============================================================================

class DashboardStats(BaseModel):
    """Schema for dashboard statistics"""
    orders_today: int
    total_revenue: float
    total_orders: int
    total_customers: int
    total_products: int
    low_stock_count: int
    top_products: List[dict]


class OrderStats(BaseModel):
    """Schema for order statistics"""
    status: str
    count: int
    total_revenue: float


class CustomerStats(BaseModel):
    """Schema for customer statistics"""
    customer_id: int
    customer_name: str
    total_orders: int
    total_spent: float
    average_order: float
    top_products: List[dict]


# ============================================================================
# BULK OPERATIONS SCHEMAS
# ============================================================================

class BulkPriceUpdate(BaseModel):
    """Schema for bulk price update"""
    keyword: str
    price_change_type: str  # "percentage" or "fixed"
    value: float
    product_ids: Optional[List[int]] = None  # If None, applies to all matching


class BulkPriceUpdateResponse(BaseModel):
    """Schema for bulk price update response"""
    updated: int
    keyword: str
    message: str


# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================

class Message(BaseModel):
    """Generic message response"""
    message: str


class DeleteResponse(BaseModel):
    """Generic delete response"""
    deleted: bool
    id: int


class PaginationParams(BaseModel):
    """Schema for pagination"""
    skip: int = 0
    limit: int = 100
