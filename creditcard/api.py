
from rest_framework import serializers, viewsets
from rest_framework.pagination import PageNumberPagination
from creditcard.models import Creditcard
from rest_framework import permissions

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 50

class CreditcardSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['exp_date', 'holder', 'number', 'cvv']
        model = Creditcard

class CreditcardViewSet(viewsets.ModelViewSet):
    queryset = Creditcard.objects.all()
    serializer_class = CreditcardSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]