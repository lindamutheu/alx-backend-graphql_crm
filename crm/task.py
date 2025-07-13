from celery import shared_task
import requests
from datetime import datetime

@shared_task
def generate_crm_report():
    graphql_url = "http://localhost:8000/graphql/"  # Change if needed
    query = """
    query {
        totalCustomers
        totalOrders
        totalRevenue
    }
    """

    response = requests.post(
        graphql_url,
        json={"query": query},
        headers={"Content-Type": "application/json"}
    )

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = "/tmp/crm_report_log.txt"

    if response.status_code == 200:
        data = response.json().get("data", {})
        total_customers = data.get("totalCustomers", 0)
        total_orders = data.get("totalOrders", 0)
        total_revenue = data.get("totalRevenue", 0)

        with open(log_file, "a") as f:
            f.write(f"[{now}] Report: {total_customers} customers, {total_orders} orders, ${total_revenue} revenue\n")
    else:
        with open(log_file, "a") as f:
            f.write(f"[{now}] ERROR: Status {response.status_code} - {response.text}\n")
