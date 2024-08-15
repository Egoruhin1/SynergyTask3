from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        # Импортируем и регистрируем сигналы, чтобы они работали при запуске приложения
        import blog.signals
