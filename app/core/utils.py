from config.wsgi import *
import json
import random
from random import randint

from core.pos.models import *


def insert_products():
    with open('../deploy/productos.json', encoding='utf8') as json_file:
        data = json.load(json_file)
        for p in data['rows'][0:80]:
            row = p['value']
            category = Category.objects.filter(name=row['marca'])
            if not category.exists():
                category = Category()
                category.name = row['marca']
                category.save()
            else:
                category = category[0]
            p = Product()
            p.name = row['nombre']
            p.category_id = category.id
            p.price = randint(1, 10)
            p.pvp = (float(p.price) * 0.12) + float(p.price)
            p.save()
            print(p.name)


def insert_purchase():
    provider = Provider()
    provider.name = 'EXPALSA S.A.'
    provider.ruc = '03026622102'
    provider.email = 'expalsa@gmail.com'
    provider.mobile = '0979021212'
    provider.address = 'Duran'
    provider.save()

    for i in range(1, 5):
        purchase = Purchase()
        purchase.provider_id = 1
        purchase.save()

        for d in range(1, 20):
            det = PurchaseDetail()
            det.purchase_id = purchase.id
            det.product_id = randint(1, Product.objects.all().count())
            while purchase.purchasedetail_set.filter(product_id=det.product_id).exists():
                det.product_id = randint(1, Product.objects.all().count())
            det.cant = randint(1, 50)
            det.price = det.product.pvp
            det.subtotal = float(det.price) * det.cant
            det.save()
            det.product.stock += det.cant
            det.product.save()

        purchase.calculate_invoice()
        print(i)


def insert_sale():
    for i in range(1, 11):
        sale = Sale()
        sale.client_id = 1
        sale.iva = 0.12
        sale.save()
        for d in range(1, 8):
            numberList = list(Product.objects.filter(stock__gt=0).values_list(flat=True))
            det = SaleDetail()
            det.sale_id = sale.id
            det.product_id = random.choice(numberList)
            while sale.saledetail_set.filter(product_id=det.product_id).exists():
                det.product_id = random.choice(numberList)
            det.cant = randint(1, det.product.stock)
            det.price = det.product.pvp
            det.subtotal = float(det.price) * det.cant
            det.save()
            det.product.stock -= det.cant
            det.product.save()

        sale.calculate_invoice()
        sale.cash = sale.total
        sale.save()
        print(i)


# insert_sale()
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u',
          'v', 'w', 'x', 'y', 'z']
data = numbers + letter
result = ''.join(random.choices(data, k=5))
print('pegasus{}'.format(result))
