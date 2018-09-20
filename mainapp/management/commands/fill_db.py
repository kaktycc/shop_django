import os, json
from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
from authapp.models import ShopUser

JSON_PATH = 'mainapp/json'

def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r',encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):

    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ProductCategory.objects.all().delete()

        for category in categories:
            new_category = ProductCategory(**category)
            new_category.save()

        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:
            category_name = product['category']
            _category = ProductCategory.objects.get(name=category_name)
            product['category'] = _category
            new_prod = Product(**product)
            new_prod.save()


    super_user = ShopUser.objects.create_superuser('django','django@django.com','geekbrains', age='18')
    user1 = ShopUser.objects.create_user('user1', 'user1@123.com', 'user1', age='42')
    user2 = ShopUser.objects.create_user('user2', 'user2@123.com', 'user2', age='44')
    user3 = ShopUser.objects.create_user('user3', 'user3@123.com', 'user3', age='22')