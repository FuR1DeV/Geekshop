from django.core.management import BaseCommand

from authapp.models import User, ShopUserProfile


class Command(BaseCommand):

    def handle(self, *args, **options):

        for user in User.objects.all():
            user_profile = ShopUserProfile.objects.create(user=user)
            user_profile.save()
