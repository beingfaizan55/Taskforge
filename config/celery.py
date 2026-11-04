import os
from celery import Celery

# Django settings ko Celery ke liye default set karein
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
# 'CELERY_' prefix wali settings ko settings.py se uthaye
app.config_from_object('django.conf:settings', namespace='CELERY')
# Har app ke andar 'tasks.py' ko khud dhoond le
app.autodiscover_tasks()