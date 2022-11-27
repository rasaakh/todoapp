from django.core.management.base import BaseCommand
from faker import Faker
from datetime import datetime
from accounts.models import User, Profile
from todolist.models import Task


class Command(BaseCommand):
    help = "inserting dummy data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        user = User.objects.create_user(email=self.fake.email(), password="Test@123456")
        profile = Profile.objects.get(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.description = self.fake.paragraph(nb_sentences=5)
        profile.save()
        for _ in range(10):
            Task.objects.create(
                user_id=user.id,
                title=self.fake.paragraph(nb_sentences=1),
                created_date=datetime.now(),
            )
