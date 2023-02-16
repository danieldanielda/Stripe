from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.name) + "\n" + str(self.description) + "\n" + str(self.price)