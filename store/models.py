from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class NetworkNode(models.Model):
    """
    Модель звена сети: завод / розничная сеть / индивидуальный предприниматель.
    Уровень (level) вычисляется при сохранении как расстояние до ближайшего 'завода' (поставщика=None).
    """
    name = models.CharField(max_length=255)

    # контакты
    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, db_index=True)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=50)

    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients",
        help_text="Поставщик оборудования (предыдущее звено по цепочке)"
    )

    # задолженность перед поставщиком
    debt = models.DecimalField(
        max_digits=14, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=Decimal('0.00')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    level = models.PositiveSmallIntegerField(
        default=0,
        help_text="Уровень в иерархии (0 — завод, 1 — розничная сеть, 2 — ИП)",
        db_index=True
    )

    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"
        ordering = ("level", "name")

    def __str__(self):
        return f"{self.name} (ур. {self.level})"

    def compute_level(self, max_depth=100):
        """
        Вычисляет расстояние до ближайшего 'завода' (supplier == None).
        Если self.supplier is None -> level 0.
        Если циклы — остановимся на max_depth.
        """
        node = self
        depth = 0
        visited = set()
        while node.supplier is not None and depth < max_depth:
            if node.supplier_id in visited:
                break
            visited.add(node.supplier_id)
            depth += 1
            node = node.supplier
        return depth

    def save(self, *args, **kwargs):
        # автоматически устанавливаем level
        try:
            self.level = self.compute_level()
            if self.level > 2:
                self.level = 2
        except Exception:
            self.level = 0
        super().save(*args, **kwargs)


class Product(models.Model):
    """
    Продукт, привязанный к конкретному звену сети.
    """
    node = models.ForeignKey(NetworkNode, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    release_date = models.DateField()

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("-release_date", "name")

    def __str__(self):
        return f"{self.name} {self.model}"