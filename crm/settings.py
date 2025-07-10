INSTALLED_APPS = [
    # other apps
    'django_crontab',
]
CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
]

CRONJOBS = [
    ('0 */12 * * *', 'crm.cron.update_low_stock'),
]