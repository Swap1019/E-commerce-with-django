from django.core.management.base import BaseCommand, CommandError
from base.models import Cart

class Command(BaseCommand):
    help = "Cleans the carts that are soft deleted"

    def handle(self, *args, **kwargs):
        try:
            deleted_count, _ = Cart.objects.filter(deleted=True).delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {deleted_count} soft-deleted cart(s)'))
        except Exception as e:
            raise CommandError(f'Failed to delete soft-deleted carts: {str(e)}')
