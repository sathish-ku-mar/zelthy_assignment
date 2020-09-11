from django.db import models

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