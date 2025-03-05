# from django.apps import AppConfig


# class MyapiConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'myapi'
from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

class AdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Admin'

    def ready(self):
        from django.db.models.signals import post_migrate
        from django.dispatch import receiver

        @receiver(post_migrate)
        def create_super_admin(sender, **kwargs):
          AdminUSer = get_user_model()
            if not AdminUSer.objects.filter(username='mamatha').exists():
                try:
                    admin_user = AdminUSer.objects.create_superuser(
                        username='mamatha',
                        email='mamatharani8143@gmail.com',
                        password='mamatha@123'
                    )
                    admin_user.role = 'admin'
                    admin_user.is_staff = True
                    admin_user.save()
                    print("✅ Superadmin 'mamatha' created successfully!")
                except IntegrityError:
                    print("⚠ Superadmin 'mamatha' already exists!")