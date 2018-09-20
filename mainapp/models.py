from django.db import models

# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(verbose_name='имя', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', blank=True)
    is_active = models.BooleanField(verbose_name="активна", default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='name', max_length=64)
    image = models.ImageField(upload_to='prod_images', blank=True)
    short_desc = models.CharField(verbose_name='short_description', max_length=128, blank=True)
    description = models.TextField(verbose_name='long_description', blank=True)
    price = models.DecimalField(verbose_name='prod_price', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='остаток')
    is_active = models.BooleanField(verbose_name="активен", default=True)
