#!/bin/bash

# Navigate to your Django project root (adjust if needed)
cd "$(dirname "$0")/../.." || exit 1

# Run Django shell command to delete inactive customers
deleted_count=$(python3 manage.py shell -c "
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

# Get all customers with no orders since a year ago
one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(
    orders__isnull=True, created_at__lte=one_year_ago
)
count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

# Log the result with timestamp
echo \"\$(date '+%Y-%m-%d %H:%M:%S') - Deleted \$deleted_count inactive customers\" >> /tmp/customer_cleanup_log.txt
