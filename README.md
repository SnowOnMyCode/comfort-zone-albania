# Beauty Products Order Management System

A full-stack web application for managing beauty product orders for hotels, hairdressers, and pharmacies.

![Dashboard Preview](https://via.placeholder.com/800x400?text=Add+Screenshot+Here)

## 🌟 Features

### Admin Features
- 📊 **Dashboard** with real-time analytics and charts
- 🛍️ **Product Management** - CRUD operations for products
- 💰 **Bulk Price Updates** - Update prices by keyword search
- 📦 **Order Management** - Track and manage orders
- 👥 **Customer Management** - Manage hotels, hairdressers, and pharmacies
- 📈 **Analytics** - Revenue tracking and top products

### Key Capabilities
- Search products by name, SKU, or keywords
- Filter customers by type (hotel, hairdresser, pharmacy)
- Order status tracking (pending → processing → shipped → delivered)
- Stock management with automatic updates
- Responsive design for desktop and mobile

## 🛠️ Tech Stack

**Backend:**
- Python 3.9+
- FastAPI (REST API)
- SQLAlchemy (ORM)
- PostgreSQL / SQLite (Database)
- JWT Authentication

**Frontend:**
- HTML5 / CSS3 / JavaScript
- Tailwind CSS (Styling)
- Chart.js (Data Visualization)

## 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Web browser (Chrome, Firefox, Safari, etc.)

Optional:
- PostgreSQL (or use SQLite by default)
- Docker (for PostgreSQL container)

## 🚀 Quick Start

### 1. Clone the Repository

\`\`\`bash
git clone <your-repo-url>
cd beauty-products-system
\`\`\`

### 2. Backend Setup

\`\`\`bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\\Scripts\\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Seed the database with sample data
python scripts/seed_data.py

# Run the server
python main.py
\`\`\`

The backend will be running at **http://localhost:8000**

### 3. Frontend Setup

\`\`\`bash
# Open a new terminal
cd frontend

# Open index.html in your browser
# You can use a simple HTTP server:
python -m http.server 3000

# Or just open the file directly in your browser
\`\`\`

The frontend will be accessible at **http://localhost:3000**

## 📖 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🗄️ Database Configuration

### Using SQLite (Default)
No setup needed! The database file will be created automatically.

### Using PostgreSQL

1. **Option A: Install PostgreSQL**
   - Download from [postgresql.org](https://www.postgresql.org/download/)
   - Create a database: `CREATE DATABASE beauty_products;`

2. **Option B: Use Docker**
   \`\`\`bash
   docker run --name beauty-db \\
     -e POSTGRES_PASSWORD=admin123 \\
     -e POSTGRES_DB=beauty_products \\
     -p 5432:5432 \\
     -d postgres:15
   \`\`\`

3. **Update database.py**
   \`\`\`python
   SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin123@localhost/beauty_products"
   \`\`\`

## 👤 Default Login Credentials

After running the seed script:
- **Email**: admin@example.com
- **Password**: admin123

## 📁 Project Structure

\`\`\`
beauty-products-system/
├── backend/
│   ├── routers/
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── products.py      # Product CRUD
│   │   ├── orders.py        # Order management
│   │   ├── customers.py     # Customer management
│   │   └── analytics.py     # Dashboard stats
│   ├── scripts/
│   │   └── seed_data.py     # Database seeding
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── main.py              # FastAPI app
│   └── requirements.txt     # Python dependencies
└── frontend/
    ├── index.html           # Main HTML
    └── app.js               # JavaScript logic
\`\`\`

## 🔑 Key Features Explained

### Bulk Price Update
Search for products by keyword and update their prices:
- **Percentage change**: Increase/decrease by X%
- **Fixed price**: Set all matching products to a specific price

Example: Update all "shampoo" products by +10%

### Order Management
- Create orders with multiple products
- Automatic stock deduction
- Order status workflow
- Calculate totals automatically

### Customer Types
- **Hotels**: Bulk orders for guest amenities
- **Hairdressers**: Professional hair care products
- **Pharmacies**: Retail beauty and skin care

## 🧪 Testing

### Test the API
1. Visit http://localhost:8000/docs
2. Try the endpoints:
   - GET /api/products - List all products
   - POST /api/products/bulk-price-update - Test bulk updates
   - GET /api/analytics/dashboard - View dashboard stats

### Sample Data
The seed script creates:
- 5 sample products
- 3 sample customers (one of each type)
- 1 admin user

## 📝 Common Tasks

### Add a New Product
\`\`\`bash
curl -X POST "http://localhost:8000/api/products/" \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "New Product",
    "sku": "PROD-001",
    "category": "Hair Care",
    "current_price": 19.99,
    "stock_quantity": 50
  }'
\`\`\`

### Update Prices by Keyword
\`\`\`bash
curl -X POST "http://localhost:8000/api/products/bulk-price-update?keyword=shampoo&price_change_type=percentage&value=10"
\`\`\`

## 🚀 Deployment

### Backend Deployment (Render/Railway)
1. Push code to GitHub
2. Connect your repository
3. Set environment variables:
   - `DATABASE_URL`: Your PostgreSQL connection string
4. Deploy!

### Frontend Deployment (Vercel/Netlify)
1. Push code to GitHub
2. Connect repository
3. Set build directory to `frontend`
4. Deploy!

## 🤝 Contributing

This is a portfolio project, but suggestions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

MIT License - feel free to use this for your own projects!

## 👨‍💻 Author

Created as a portfolio project by [Your Name]

- Portfolio: [your-portfolio-url]
- LinkedIn: [your-linkedin]
- GitHub: [your-github]

## 🙏 Acknowledgments

- FastAPI for the amazing framework
- Tailwind CSS for the styling utilities
- Chart.js for data visualization

---

**Note**: This is a demonstration project. For production use, implement additional security measures, error handling, and testing.
