from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product 
        fields = ('pk','name','description','quantity','unit_price','stock_level','created_by_id','created_at','updated_at')
