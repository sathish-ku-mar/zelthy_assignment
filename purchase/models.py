from django.db import models
from django.db.models import Avg, Count
# Create your models here.


class PurchaseModel(models.Model):
    purchaser_name = models.CharField(max_length=200, help_text='A person who buys something')
    quantity = models.IntegerField(help_text='A large quantity of goods bought at one time')

    def __str__(self):
        return '%s' % (self.id,)


class PurchaseStatusModel(models.Model):
    purchase = models.ForeignKey(PurchaseModel, related_name='purchase_status', on_delete=models.CASCADE,
                                 help_text='The status model related with purchase model')
    status = models.CharField(max_length=25,
                              choices=(
                                  ('open', 'Open'),
                                  ('verified', 'Verified'),
                                  ('dispatched', 'Dispatched'),
                                  ('delivered', 'Delivered'),
                              ), help_text='Classification of the status of a purchase')
    created_at = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return '%d: %s' % (self.purchase.id, self.status)

    @classmethod
    def get_all(cls):
        """
        Get all the purchase
        :param: None
        :return: Purchase object
        :rtype: django.db.models.query.QuerySet
        """
        return cls.objects.all()

    @classmethod
    def get_latest(cls):
        """
        Get the latest purchase
        :param: None
        :return: Purchase object
        :rtype: django.db.models.query.QuerySet
        """
        return cls.objects.latest('id')

    def get_status(self):
        """
        Get the status of the purchase
        :param: None
        :return: Purchase object
        :rtype: django.db.models.query.QuerySet
        """
        return self.status

    def get_purchase(self):
        """
        Get the status of the purchase
        :param: None
        :return: Purchase object
        :rtype: django.db.models.query.QuerySet
        """
        return self.purchase.id

    @classmethod
    def check_dispatched_status_exist(cls):
        """
        To check dispatched status exist in the Purchase
        :param: None
        :return: Purchase object
        :rtype: django.db.models.query.QuerySet
        """
        return cls.objects.filter(purchase_id=cls.get_latest().get_purchase(), status='dispatched').exists()

    @classmethod
    def get_filter_data(cls, date=None, status_list=None):
        """
        Get the filter data of the purchase
        :param date: get the date to filter
        :param status_list: get the status to filter
        :return: Purchase object
        :rtype: django.db.models.query.QuerySet
        """
        if date and status_list:
            queryset = cls.objects.filter(created_at__date=date, status__in=status_list).extra(select={
                'month': "EXTRACT(month FROM created_at)"}).values('month').annotate(count=Count('purchase__quantity'))
        else:
            queryset = cls.objects.all().extra(select={'month': '%s' % ("EXTRACT(month FROM created_at)",)}).values('month') \
                .annotate(count=Count('purchase__quantity'))

        return queryset
