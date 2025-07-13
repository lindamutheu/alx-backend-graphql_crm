from datetime import datetime
import requests
from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client

def update_low_stock():
    graphql_url = "http://localhost:8000/graphql"
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

    try:
        response = requests.post(
            graphql_url,
            json={"query": mutation},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        updates = data["data"]["updateLowStockProducts"]
        message = updates["message"]
        updated_products = updates["updatedProducts"]

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
            log_file.write(f"[{timestamp}] {message}\n")
            for product in updated_products:
                log_file.write(f"- {product['name']}: {product['stock']} units\n")
            log_file.write("\n")

        print("Low stock update completed.")

    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
            log_file.write(f"[{timestamp}] ERROR: {e}\n")
        print(f"Error updating low-stock products: {e}")