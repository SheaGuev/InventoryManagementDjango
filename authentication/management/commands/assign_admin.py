from django.core.management.base import BaseCommand, CommandError
from InventoryManagement.models import CustomUser, Role

class Command(BaseCommand):
    help = 'Assigns the admin role to a user'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='The email of the user to promote')

    def handle(self, *args, **kwargs):
        email = kwargs['email']
        try:
            user = CustomUser.objects.get(email=email)
            admin_role = Role.objects.get(role_name='admin')
            user.role = admin_role
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully assigned admin role to user {email}'))
        except CustomUser.DoesNotExist:
            raise CommandError('User does not exist')
        except Role.DoesNotExist:
            raise CommandError('Admin role does not exist')