from django.core.management.base import BaseCommand
import requests
import json
from datetime import datetime


class Command(BaseCommand):
    help = "Runs the UpdateLowStockProducts GraphQL mutation to restock products"

    def handle(self, *args, **options):
        graphql_url = "http://localhost:8000/graphql/"  # Adjust if needed
        mutation = """
        mutation {
            updateLowStockProducts {
                message
                updatedProducts {
                    name
                    stock
                }
            }
        }
        """

        response = requests.post(
            graphql_url,
            json={'query': mutation},
            headers={'Content-Type': 'application/json'}
        )

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = "/tmp/low_stock_updates_log.txt"

        if response.status_code == 200:
            data = response.json()
            updates = data.get("data", {}).get("updateLowStockProducts", {})
            message = updates.get("message", "No message returned")
            updated_products = updates.get("updatedProducts", [])

            with open(log_file, "a") as f:
                f.write(f"[{now}] {message}\n")
                for product in updated_products:
                    f.write(f" - {product['name']}: {product['stock']} units\n")
                f.write("\n")
        else:
            with open(log_file, "a") as f:
                f.write(f"[{now}] ERROR: Status {response.status_code}\n")
