# seed_db.py

import os
import django
from django.utils import timezone

# === Setup Django Environment ===
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx-backend-graphql_crm.settings')
django.setup()

from crm.models import Customer, Product, Order

# === Wipe and Seed Database ===

def run():
    print("🚨 Seeding database...")

    # Clear old data
    Customer.objects.all().delete()
    Product.objects.all().delete()
    Order.objects.all().delete()

    # Create customers
    c1 = Customer.objects.create(name="Alice", email="alice@example.com", phone="+123456789")
    c2 = Customer.objects.create(name="Bob", email="bob@example.com", phone="123-456-7890")

    # Create products
    p1 = Product.objects.create(name="Laptop", price=1500.00, stock=5)
    p2 = Product.objects.create(name="Mouse", price=25.50, stock=50)
    p3 = Product.objects.create(name="Keyboard", price=45.00, stock=30)

    # Create orders
    order1 = Order.objects.create(
        customer=c1,
        order_date=timezone.now(),
        total_amount=p1.price + p2.price
    )
    order1.products.set([p1, p2])

    order2 = Order.objects.create(
        customer=c2,
        order_date=timezone.now(),
        total_amount=p3.price
    )
    order2.products.set([p3])

    print("✅ Database seeded successfully.")


if __name__ == '__main__':
    run()
