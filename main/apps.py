from django.apps import AppConfig
from django.conf import settings

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from django.contrib.auth.models import User, Group # django app registry must be fully initialised
        from django.db.models.signals import post_save
        def add_to_default_group(sender, instance, created, **kwargs):
            if created:
                group, ok = Group.objects.get_or_create(name="default")
                group.user_set.add(instance)
        post_save.connect(add_to_default_group, sender=settings.AUTH_USER_MODEL)


