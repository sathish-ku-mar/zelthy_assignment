from django.contrib import admin
from .models import PurchaseModel, PurchaseStatusModel

# Register your models here.
admin.site.register(PurchaseModel)
admin.site.register(PurchaseStatusModel)