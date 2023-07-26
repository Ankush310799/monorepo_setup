"""  Add default group types - add_default_user_groups"""

from django.core.management.base import BaseCommand, CommandError
from users.models import Group


class Command(BaseCommand):
    help = "Add default Group types list"

    def handle(self, *args, **options):

        groups_list=['Admin','Manager']

        for group in groups_list:

            try:
                group_type = Group.objects.create(name=group)
                group_type.save()

                self.stdout.write(
                    self.style.SUCCESS('Succesfully added new group type "%s"' % group)
                )
            except Exception as e:
                print(e)
