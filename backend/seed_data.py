import sys
sys.path.append('..')

from database import SessionLocal
import models

def seed_data():
    db = SessionLocal()
    
    # Check if data already exists
    existing = db.query(models.Product).first()
    if existing:
        print("Database already has data. Skipping seed.")
        db.close()
        return
    
    print("Seeding database...")
    
    # Create sample products
    products = [
        models.Product(
            name="Professional Shampoo 500ml",
            sku="SHAMP-001",
            description="Professional grade shampoo for all hair types",
            category="Hair Care",
            current_price=15.99,
            stock_quantity=100,
            keywords="shampoo hair professional loreal"
        ),
        models.Product(
            name="Hair Color Cream - Brown",
            sku="COLOR-001",
            description="Permanent hair color cream",
            category="Hair Color",
            current_price=8.50,
            stock_quantity=50,
            keywords="color dye brown hair permanent"
        ),
        models.Product(
            name="Face Cream SPF50",
            sku="CREAM-001",
            description="Daily moisturizing face cream with SPF50",
            category="Skin Care",
            current_price=22.00,
            stock_quantity=75,
            keywords="cream face spf skin moisturizer"
        ),
        models.Product(
            name="Conditioner 500ml",
            sku="COND-001",
            description="Deep conditioning treatment",
            category="Hair Care",
            current_price=16.99,
            stock_quantity=80,
            keywords="conditioner hair treatment"
        ),
        models.Product(
            name="Hair Gel Strong Hold",
            sku="GEL-001",
            description="Extra strong hold hair gel",
            category="Hair Styling",
            current_price=9.99,
            stock_quantity=60,
            keywords="gel styling hair hold"
        ),
    ]
    
    db.add_all(products)
    
    # Create sample customers
    customers = [
        models.Customer(
            name="Grand Hotel Plaza",
            type="hotel",
            email="contact@grandhotel.com",
            phone="+1234567890",
            address="123 Main St, City Center",
            tax_id="TAX-HOTEL-001"
        ),
        models.Customer(
            name="Elite Hair Salon",
            type="hairdresser",
            email="info@elitehair.com",
            phone="+1234567891",
            address="456 Beauty Ave, Shopping District",
            tax_id="TAX-SALON-001"
        ),
        models.Customer(
            name="HealthPlus Pharmacy",
            type="pharmacy",
            email="orders@healthplus.com",
            phone="+1234567892",
            address="789 Medical Blvd, Health Quarter",
            tax_id="TAX-PHARM-001"
        ),
    ]
    
    db.add_all(customers)
    
    # Create a sample user (admin)
    from routers.auth import get_password_hash
    admin_user = models.User(
        email="admin@example.com",
        hashed_password=get_password_hash("admin123"),
        role="admin",
        is_active=True
    )
    
    db.add(admin_user)
    
    db.commit()
    
    print("✓ Created 5 products")
    print("✓ Created 3 customers")
    print("✓ Created admin user (email: admin@example.com, password: admin123)")
    print("Database seeded successfully!")
    
    db.close()

if __name__ == "__main__":
    seed_data()
