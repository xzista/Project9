from django.core.management.base import BaseCommand
from store.models import NetworkNode, Product
from decimal import Decimal
from datetime import date

class Command(BaseCommand):
    help = "Заполняет базу тестовыми данными для сети электроники"

    def handle(self, *args, **options):
        self.stdout.write("Очистка старых данных...")
        Product.objects.all().delete()
        NetworkNode.objects.all().delete()

        self.stdout.write("Создание завода в России...")
        factory = NetworkNode.objects.create(
            name="Завод Электроника",
            email="factory@electronics.ru",
            country="Russia",
            city="Москва",
            street="Промышленная",
            house_number="1",
            debt=Decimal("0.00")
        )

        self.stdout.write("Создание завода в США...")
        factory_usa = NetworkNode.objects.create(
            name="Electrical factory",
            email="factory-usa-ny@electronics.com",
            country="USA",
            city="New-York",
            street="st. prom-5",
            house_number="1",
            debt=Decimal("0.00")
        )

        self.stdout.write("Создание розничной сети...")
        retail = NetworkNode.objects.create(
            name="ТехноМаркет",
            email="retail@technomarket.ru",
            country="Russia",
            city="Санкт-Петербург",
            street="Невский проспект",
            house_number="10",
            supplier=factory,
            debt=Decimal("150000.50")
        )

        self.stdout.write("Создание ИП...")
        entrepreneur = NetworkNode.objects.create(
            name="ИП Иванов",
            email="ivanov@ip.ru",
            country="Russia",
            city="Казань",
            street="Баумана",
            house_number="5",
            supplier=retail,
            debt=Decimal("25000.00")
        )

        self.stdout.write("Создание продуктов...")
        Product.objects.bulk_create([
            Product(
                node=factory,
                name="Смартфон",
                model="XPhone 12",
                release_date=date(2023, 9, 1)
            ),
            Product(
                node=factory_usa,
                name="Iphone",
                model="Iphone 16 Pro",
                release_date=date(2024, 9, 1)
            ),
            Product(
                node=retail,
                name="Ноутбук",
                model="UltraBook Pro",
                release_date=date(2023, 6, 15)
            ),
            Product(
                node=entrepreneur,
                name="Планшет",
                model="Tab Mini",
                release_date=date(2024, 1, 10)
            ),
        ])

        self.stdout.write(self.style.SUCCESS("База успешно заполнена тестовыми данными!"))
