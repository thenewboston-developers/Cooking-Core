from django.db import models

from cooking_core.general.models import CreatedModified


class Comment(CreatedModified):
    creator = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE)
    balance = models.PositiveBigIntegerField(default=0)
    text = models.TextField()

    def __str__(self):
        return str(self.id)
