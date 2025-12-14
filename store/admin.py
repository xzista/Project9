from django.contrib import admin
from django.utils.html import format_html
from .models import NetworkNode, Product
from decimal import Decimal


@admin.action(description="Очистить задолженность перед поставщиком")
def clear_debt_action(modeladmin, request, queryset):
    queryset.update(debt=Decimal('0.00'))


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "level", "country", "city", "email", "debt", "created_at", "supplier_link")
    list_filter = ("country", "city", "level")
    search_fields = ("name", "city", "country", "email")
    actions = [clear_debt_action]
    readonly_fields = ("created_at", "level")
    raw_id_fields = ("supplier",)

    def supplier_link(self, obj):
        if obj.supplier:
            url = f"/admin/{obj._meta.app_label}/{obj.supplier._meta.model_name}/{obj.supplier.pk}/change/"
            return format_html('<a href="{}">{}</a>', url, obj.supplier)
        return "-"

    supplier_link.short_description = "Поставщик (ссылка)"

    inlines = []


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "model", "node", "release_date")
    list_filter = ("release_date", "node__country")
    search_fields = ("name", "model")