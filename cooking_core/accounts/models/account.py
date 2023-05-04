from django.db import models


class Account(models.Model):
    account_number = models.CharField(max_length=50, primary_key=True)
    balance = models.PositiveBigIntegerField()

    def __str__(self):
        return f'{self.account_number} | {self.balance}'
