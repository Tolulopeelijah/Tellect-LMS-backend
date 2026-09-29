from django.core.management.base import BaseCommand

from apps.authentication.models import User

# Dev/test login accounts. Run: python manage.py seed_login_users
# Local dev password for all three is Tellect123! (change in production).
USERS = [
    {
        "email": "tolulopee90@gmail.com",
        "full_name": "Tolulope Ayanfe",
        "role": "STUDENT",
        "is_staff": True,
        "is_superuser": True,
    },
    {
        "email": "instructor-01@ex.am",
        "full_name": "Instructor 1",
        "role": "STUDENT",
    },
    {
        "email": "janep@ex.am",
        "full_name": "Jane Plutha",
        "role": "STUDENT",
    },
]

PASSWORD = "Tellect123!"


class Command(BaseCommand):
    help = "Seed known dev login users with password Tellect123!"

    def handle(self, *args, **options):
        for data in USERS:
            user, created = User.objects.get_or_create(
                email=data["email"],
                defaults={
                    "full_name": data["full_name"],
                    "role": data.get("role", "STUDENT"),
                    "is_staff": data.get("is_staff", False),
                    "is_superuser": data.get("is_superuser", False),
                },
            )
            user.set_password(PASSWORD)
            user.is_verified = True
            user.is_active = True
            user.save()
            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{action} {user.email}"))
