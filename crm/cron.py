from datetime import datetime
import requests


def log_crm_heartbeat():
    # Log timestamp
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_message = f"{timestamp} CRM is alive\n"

    # Append to heartbeat log file
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(log_message)

    # Optional: Check GraphQL hello field
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.ok:
            print("GraphQL hello response:", response.json())
        else:
            print("GraphQL endpoint not responsive.")
    except requests.RequestException as e:
        print(f"Error contacting GraphQL endpoint: {e}")


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
        # Send mutation request
        response = requests.post(
            graphql_url,
            json={"query": mutation},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        # Extract data
        updates = data["data"]["updateLowStockProducts"]
        message = updates["message"]
        updated_products = updates["updatedProducts"]

        # Log results
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
