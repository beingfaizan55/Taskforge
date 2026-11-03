from django.apps import AppConfig

class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'  # Agar aapki app ka naam kuch aur hai (jaise 'api' ya 'todo'), toh woh likhein

    def ready(self):
        import tasks.signals  # Yahan app_name.signals hona chahiye