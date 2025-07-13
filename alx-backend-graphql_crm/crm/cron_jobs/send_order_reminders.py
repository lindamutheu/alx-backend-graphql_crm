#!/usr/bin/env python3

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta

# Set up GraphQL client
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Calculate date range for last 7 days
end_date = datetime.now().date()
start_date = end_date - timedelta(days=7)

# GraphQL query
query = gql("""
query GetRecentOrders($startDate: Date!, $endDate: Date!) {
  allOrders(orderDate_Gte: $startDate, orderDate_Lte: $endDate, status: "PENDING") {
    edges {
      node {
        id
        customer {
          email
        }
      }
    }
  }
}
""")

variables = {
    "startDate": str(start_date),
    "endDate": str(end_date)
}

# Execute query
try:
    result = client.execute(query, variable_values=variables)
    orders = result['allOrders']['edges']

    with open("/tmp/order_reminders_log.txt", "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for edge in orders:
            order_id = edge['node']['id']
            customer_email = edge['node']['customer']['email']
            log_file.write(f"{timestamp} - Order ID: {order_id}, Customer Email: {customer_email}\n")

    print("Order reminders processed!")

except Exception as e:
    print(f"Error fetching orders: {e}")
