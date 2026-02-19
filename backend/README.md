# Backend - Beauty Products API

FastAPI-based REST API for the Beauty Products Order Management System.

## Setup

### 1. Create Virtual Environment
\`\`\`bash
python -m venv venv
\`\`\`

### 2. Activate Virtual Environment
\`\`\`bash
# Windows
venv\\Scripts\\activate

# Mac/Linux
source venv/bin/activate
\`\`\`

### 3. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Configure Database
Edit \`database.py\`:

**For SQLite (default):**
\`\`\`python
SQLALCHEMY_DATABASE_URL = "sqlite:///./beauty_products.db"
\`\`\`

**For PostgreSQL:**
\`\`\`python
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost/beauty_products"
\`\`\`

### 5. Seed Database
\`\`\`bash
python scripts/seed_data.py
\`\`\`

This creates:
- 5 sample products
- 3 sample customers
- 1 admin user (email: admin@example.com, password: admin123)

### 6. Run Server
\`\`\`bash
python main.py
\`\`\`

Server runs at: http://localhost:8000

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Endpoints

### Authentication
- POST `/api/auth/register` - Register new user
- POST `/api/auth/login` - Login (get JWT token)
- GET `/api/auth/me` - Get current user

### Products
- GET `/api/products/` - List all products
- GET `/api/products/{id}` - Get single product
- POST `/api/products/` - Create product
- PUT `/api/products/{id}` - Update product
- DELETE `/api/products/{id}` - Delete product
- POST `/api/products/bulk-price-update` - Bulk update prices
- GET `/api/products/search/{term}` - Search products

### Orders
- GET `/api/orders/` - List all orders
- GET `/api/orders/{id}` - Get single order
- POST `/api/orders/` - Create order
- PUT `/api/orders/{id}/status` - Update order status
- DELETE `/api/orders/{id}` - Delete order
- GET `/api/orders/customer/{customer_id}` - Get customer orders

### Customers
- GET `/api/customers/` - List all customers
- GET `/api/customers/{id}` - Get single customer
- POST `/api/customers/` - Create customer
- PUT `/api/customers/{id}` - Update customer
- DELETE `/api/customers/{id}` - Delete customer
- GET `/api/customers/{id}/stats` - Customer statistics

### Analytics
- GET `/api/analytics/dashboard` - Dashboard statistics
- GET `/api/analytics/revenue-by-day` - Revenue by day

## Database Models

### Product
- id, name, sku, description, category
- current_price, stock_quantity, keywords
- created_at, updated_at

### Customer
- id, name, type (hotel/hairdresser/pharmacy)
- email, phone, address, tax_id
- created_at

### Order
- id, customer_id, order_number, status
- total_amount, created_at, updated_at
- Relationships: customer, items

### OrderItem
- id, order_id, product_id
- quantity, unit_price, subtotal
- Relationships: order, product

### User
- id, email, hashed_password
- role (admin/sales), is_active
- created_at

## Development

### Add New Router
1. Create \`routers/newrouter.py\`
2. Add router in \`main.py\`:
   \`\`\`python
   from routers import newrouter
   app.include_router(newrouter.router, prefix="/api/new", tags=["New"])
   \`\`\`

### Database Migration
When changing models:
1. Drop tables (dev only): Delete \`beauty_products.db\`
2. Restart server to recreate tables
3. Re-run seed script

For production, use Alembic for migrations.

## Environment Variables

Create \`.env\` file:
\`\`\`
DATABASE_URL=postgresql://user:pass@localhost/dbname
SECRET_KEY=your-secret-key-here
\`\`\`

## Testing

Run server and test endpoints in Swagger UI at http://localhost:8000/docs

## Troubleshooting

### Port Already in Use
\`\`\`bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :8000
kill -9 <PID>
\`\`\`

### Database Connection Error
- Check PostgreSQL is running
- Verify connection string
- Try SQLite instead for development
