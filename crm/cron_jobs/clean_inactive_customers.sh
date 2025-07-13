#!/bin/bash
#!/usr/bin/env bash

# Change directory to project root (relative to script location)
cd ../../

# Delete inactive customers using Django shell
deleted_count=$(python3 manage.py shell -c "
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(
    orders__isnull=True, created_at__lte=one_year_ago
)
count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

# Log number of deleted customers with timestamp
echo \"\$(date '+%Y-%m-%d %H:%M:%S') - Deleted \$deleted_count inactive customers\" >> /tmp/customer_cleanup_log.txt
