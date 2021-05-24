from django.contrib import admin
import stocks
from stocks import models


admin.register(stocks)
admin.site.register(models.Product)
