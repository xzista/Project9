from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

USERS = [
    {
        "username": "admin",
        "password": "admin123",
        "is_staff": True,
        "is_active": True,
        "is_superuser": True,
    },
    {
        "username": "employee",
        "password": "employee123",
        "is_staff": True,
        "is_active": True,
        "is_superuser": False,
    },
    {
        "username": "inactive_employee",
        "password": "inactive123",
        "is_staff": True,
        "is_active": False,
        "is_superuser": False,
    },
    {
        "username": "regular_user",
        "password": "user123",
        "is_staff": False,
        "is_active": True,
        "is_superuser": False,
    },
]


class Command(BaseCommand):
    help = "Создаёт тестовых пользователей с разными правами доступа"

    def handle(self, *args, **options):
        self.stdout.write("Создание тестовых пользователей\n")

        for data in USERS:
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "is_staff": data["is_staff"],
                    "is_active": data["is_active"],
                    "is_superuser": data["is_superuser"],
                },
            )

            if created:
                user.set_password(data["password"])
                user.save()
                status = self.style.SUCCESS("CREATED")
            else:
                status = self.style.WARNING("EXISTS")

            self.stdout.write(
                f"{status} "
                f"user='{user.username}', "
                f"is_staff={user.is_staff}, "
                f"is_active={user.is_active}, "
                f"is_superuser={user.is_superuser}"
            )

        self.stdout.write("\nПользователи созданы")
