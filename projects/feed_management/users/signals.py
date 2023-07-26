from django.contrib.auth.models import Group


def add_default_admin_group_to_new_regi_user(sender, instance, **kwargs):

    if instance:
        group, _ = Group.objects.get_or_create(name='Admin')
        instance.groups.add(group)
