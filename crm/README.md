# CRM Celery Report Scheduler

This project uses Celery with Celery Beat to generate weekly CRM reports.

## Setup

1. **Install Redis**
   ```bash
   sudo apt install redis-server
   sudo systemctl enable redis-server
   sudo systemctl start redis-server
