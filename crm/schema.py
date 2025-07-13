import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Customer, Product, Order
from .filters import CustomerFilter, ProductFilter, OrderFilter
from django.utils import timezone
from .models import Product

# === GraphQL Types ===

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        filterset_class = CustomerFilter
        interfaces = (graphene.relay.Node,)

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        filterset_class = ProductFilter
        interfaces = (graphene.relay.Node,)

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        filterset_class = OrderFilter
        interfaces = (graphene.relay.Node,)

# === Input Object Types ===

class CreateCustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

class BulkCustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

class CreateProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Decimal(required=True)
    stock = graphene.Int(default_value=0)

class CreateOrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.DateTime()

# === Mutations ===

class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CreateCustomerInput(required=True)

    customer = graphene.Field(CustomerType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, input):
        if Customer.objects.filter(email=input.email).exists():
            return CreateCustomer(success=False, message="Email already exists")
        customer = Customer(name=input.name, email=input.email, phone=input.phone)
        customer.save()
        return CreateCustomer(customer=customer, success=True, message="Customer created")


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(BulkCustomerInput, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, input):
        created = []
        errors = []

        for i, c in enumerate(input):
            if Customer.objects.filter(email=c.email).exists():
                errors.append(f"Row {i+1}: Email '{c.email}' already exists.")
                continue
            try:
                customer = Customer(name=c.name, email=c.email, phone=c.phone)
                customer.save()
                created.append(customer)
            except Exception as e:
                errors.append(f"Row {i+1}: {str(e)}")

        return BulkCreateCustomers(customers=created, errors=errors)


class CreateProduct(graphene.Mutation):
    class Arguments:
        input = CreateProductInput(required=True)

    product = graphene.Field(ProductType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, input):
        if input.price <= 0:
            raise Exception("Price must be positive.")
        if input.stock is not None and input.stock < 0:
            raise Exception("Stock cannot be negative.")

        product = Product(name=input.name, price=input.price, stock=input.stock or 0)
        product.save()
        return CreateProduct(product=product, success=True, message="Product created")


class CreateOrder(graphene.Mutation):
    class Arguments:
        input = CreateOrderInput(required=True)

    order = graphene.Field(OrderType)
    message = graphene.String()

    def mutate(self, info, input):
        try:
            customer = Customer.objects.get(pk=input.customer_id)
        except Customer.DoesNotExist:
            raise Exception("Invalid customer ID.")

        if not input.product_ids:
            raise Exception("At least one product must be selected.")

        products = Product.objects.filter(id__in=input.product_ids)
        if products.count() != len(input.product_ids):
            raise Exception("Some product IDs are invalid.")

        total = sum(p.price for p in products)
        order = Order(customer=customer, order_date=input.order_date or timezone.now(), total_amount=total)
        order.save()
        order.products.set(products)

        return CreateOrder(order=order, message="Order created successfully.")

# === Query and Mutation ===

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")

    all_customers = DjangoFilterConnectionField(CustomerType)
    all_products = DjangoFilterConnectionField(ProductType)
    all_orders = DjangoFilterConnectionField(OrderType)

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()


#=== StockProducts ===

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock")

        
class UpdateLowStockProducts(graphene.Mutation):
    class Output:
        updated_products = graphene.List(graphene.String)
        message = graphene.String()

    def mutate(self, info):
        updated_products = []

        # Query products with stock < 10
        low_stock_products = Product.objects.filter(stock__lt=10)

        for product in low_stock_products:
            product.stock += 10  # simulate restocking
            product.save()
            updated_products.append(f"{product.name} (new stock: {product.stock})")

        message = "Stock levels updated successfully." if updated_products else "No low-stock products found."
        return UpdateLowStockProducts(updated_products=updated_products, message=message)

# Add mutation to your schema
class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

    class Query(graphene.ObjectType):
     total_customers = graphene.Int()
    total_orders = graphene.Int()
    total_revenue = graphene.Float()

    def resolve_total_customers(root, info):
        from .models import Customer
        return Customer.objects.count()

    def resolve_total_orders(root, info):
        from .models import Order
        return Order.objects.count()

    def resolve_total_revenue(root, info):
        from .models import Order
        return Order.objects.aggregate(total=models.Sum('totalamount'))['total'] or 0
