import random
import calendar
from django.shortcuts import render
# Create your views here.
from .models import PurchaseModel, PurchaseStatusModel
from .serializers import PurchaseSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.http.request import QueryDict
from core.common import random_date


class PurchaseViewSet(viewsets.ViewSet):
    """
        A simple ViewSet for the Purchase.
    """
    model = PurchaseStatusModel
    serializer_class = PurchaseSerializer
    queryset = model.get_all()

    def list(self, request):
        """
            To show dashboard page and create records in the model
        """
        queryset = self.queryset.count()

        if queryset < 1:
            name_list = ["Name 1", "Name 2", "Name 3", "Name 4", "Name 5", "Name 6", "Name 7", "Name 8", "Name 9", "Name 10"]
            status_tuple = ('open', 'verified', 'dispatched', 'delivered')
            for i in range(5000):
                purchase_status = [
                    {"status": i, "created_at": random_date("2019-01-01T05:00:00Z", "2020-03-31T22:00:00Z", random.random())}
                    for i in status_tuple]
                data = {
                    "purchaser_name": random.choice(name_list),
                    "quantity": random.randrange(1, 10),
                    "purchase_status": purchase_status
                }
                serializer = self.serializer_class(data=data)

                if serializer.is_valid():
                    serializer.save()
        return render(request, 'purchase/index.html')

    def filter(self, request):
        """
            To filter the purchase model data
        """
        data = QueryDict.dict(request.data)

        if 'date' in data and data['date']:
            status = ['open', 'verified', 'dispatched', 'delivered']
            if self.model.get_latest().get_status() == 'dispatched':
                status = ['dispatched']
            elif self.model.get_latest().get_status() == 'delivered':
                dispatched_exist = self.model.check_dispatched_status_exist()
                if dispatched_exist:
                    status = ['dispatched']
                else:
                    status = ['delivered']

            queryset = self.model.get_filter_data(data['date'], status)
        else:
            queryset = self.model.get_filter_data()

        queryset = sorted(queryset, key=lambda x: x['month'])
        data = {
            'xAxis': list(map(lambda x: calendar.month_name[int(x['month'])], queryset)),
            'yAxis': list(map(lambda x: x['count'], queryset))
        }
        return Response(data)