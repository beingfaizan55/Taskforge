from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task  # Apne Task model ko import karein

@receiver(post_save, sender=Task)
def task_created_handler(sender, instance, created, **kwargs):
    if created:
        print(f"🔥 [SIGNAL TRIGGERED]: New Task Created -> '{instance.title}' (Priority: {instance.priority})")
    else:
        print(f"✏️ [SIGNAL TRIGGERED]: Task Updated -> '{instance.title}'")