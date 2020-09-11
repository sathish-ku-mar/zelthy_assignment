from rest_framework import serializers
from .models import PurchaseModel, PurchaseStatusModel


class PurchaseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseStatusModel
        fields = ['status', 'created_at']


class PurchaseSerializer(serializers.ModelSerializer):
    purchase_status = PurchaseStatusSerializer(many=True)

    class Meta:
        model = PurchaseModel
        fields = ['purchaser_name', 'quantity', 'purchase_status']

    def create(self, validated_data):
        purchase_status_datas = validated_data.pop('purchase_status')
        purchase = PurchaseModel.objects.create(**validated_data)
        for purchase_status_data in purchase_status_datas:
            PurchaseStatusModel.objects.create(purchase=purchase, **purchase_status_data)
        return purchase
