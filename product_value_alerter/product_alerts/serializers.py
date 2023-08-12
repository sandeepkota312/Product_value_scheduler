from rest_framework import serializers
from .models import URLs_Feed

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=URLs_Feed
        fields=['Url','product_name','Original_price','Current_price','lowest_price','users','status',]



