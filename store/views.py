from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import NetworkNode, Product
from .permissions import IsActiveEmployee
from .serializers import NetworkNodeSerializer, ProductSerializer


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    CRUD для модели поставщика (NetworkNode).
    Запрет на обновление поля debt реализован в сериализаторе.
    """

    queryset = NetworkNode.objects.select_related("supplier").prefetch_related("products")
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveEmployee]

    # фильтр: по country и поиск по name/city
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["country"]
    search_fields = ["name", "city", "country"]
    ordering_fields = ["created_at", "level", "name"]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("node")
    serializer_class = ProductSerializer
    permission_classes = [IsActiveEmployee]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["node__country", "node"]
    search_fields = ["name", "model"]
