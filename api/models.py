from django.db import models


class Coin(models.Model):
    coin_name = models.CharField(max_length=100, null=False, blank=False)
    coin_ticker = models.CharField(max_length=4, null=False, blank=False)
    coin_image = models.TextField()
    signature = models.CharField(max_length=400, null=False, blank=False)
    description = models.TextField()
    request_datetime = models.DateTimeField(auto_now_add=True)

