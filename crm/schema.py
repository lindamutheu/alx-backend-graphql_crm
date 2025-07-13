import graphene
from crm.models import Product


class ProductType(graphene.ObjectType):
    name = graphene.String()
    stock = graphene.Int()


class UpdateLowStockProducts(graphene.Mutation):
    updated_products = graphene.List(ProductType)
    message = graphene.String()

    def mutate(self, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_products = []

        for product in low_stock_products:
            product.stock += 10  # Simulate restocking
            product.save()
            updated_products.append(ProductType(name=product.name, stock=product.stock))

        if updated_products:
            message = "Stock levels updated successfully"
        else:
            message = "No products needed restocking"

        return UpdateLowStockProducts(updated_products=updated_products, message=message)


class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()
