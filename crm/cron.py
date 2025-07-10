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
    # GraphQL endpoint
    graphql_url = "http://localhost:8000/graphql"

    # GraphQL mutation
    mutation = """
    mutation {
        updateLowStockProducts {
            updatedProducts
            message
        }
    }
    """

    try:
        # Send mutation request
        response = requests.post(graphql_url, json={"query": mutation}, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Extract updated products
        updated = data["data"]["updateLowStockProducts"]["updatedProducts"]
        message = data["data"]["updateLowStockProducts"]["message"]

        # Log results
        timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
            log_file.write(f"{timestamp} - {message}\n")
            for product in updated:
                log_file.write(f"  - {product}\n")

        print("Low stock update completed.")

    except Exception as e:
        print(f"Error updating low-stock products: {e}")