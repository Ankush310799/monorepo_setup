from django.apps import AppConfig
from django.db.models.signals import post_save


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from .signals import add_default_admin_group_to_new_regi_user

        model = self.get_model('User')

        post_save.connect(add_default_admin_group_to_new_regi_user, sender=model,
                          dispatch_uid='set_default_admin_group_to_new_user')
