import os
import django
import csv
import sys
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brokurly.settings')
django.setup()


from product.models import *
from faker import Faker

fake = Faker()

# main_categories
# csv_path = './main_category.csv'
# with open(csv_path) as f:
#     rows = csv.reader(f, delimiter = ',')
#     next(f, None)

#     for row in rows:
#         if row[0]:
#             MainCategory.objects.create(name=row[0], image_url=row[1], image_active_url=row[2])

# sub_categories
# csv_path = './sub_category.csv'
# with open(csv_path) as f:
#     rows = csv.reader(f, delimiter = ',')
#     next(f, None)

#     for row in rows:
#         if row[0]:
#             main_category_id = MainCategory.objects.get(name=row[0]).id
#         SubCategory.objects.create(name=row[1], main_category_id=main_category_id)


# morning_delivery_areas
# csv_path = './morning_delivery_areas.csv'
# with open(csv_path) as f:
#     rows = csv.reader(f, delimiter = ',')
#     next(f, None)
#     for row in rows:
#         MorningDeliveryArea.objects.create(name=row[0])

# shipping_classifications

# ShippingClassification.objects.create(name="샛별배송")
# ShippingClassification.objects.create(name="택배배송")


# product
# csv_path = './product.csv'
# with open(csv_path) as f:
#     rows = csv.reader(f, delimiter = ',')
#     next(f, None)

#     for row in rows:
#         if row[1]:
#             sub_category_id = SubCategory.objects.get(name=row[1]).id

#         is_sold_out = random.randint(0,1)

#         tmp = True
#         if is_sold_out == 1:
#             tmp = True
#         else:
#             tmp = False

#         Product.objects.create(       
#             name=row[2],
#             price=row[3],
#             content=row[4], 
#             is_sold_out=tmp,
#             image_url=row[5], 
#             sales_count=random.randint(1,5000),
#             create_time=fake.date_time_this_decade(),
#             sub_category_id=sub_category_id,
#             )



# discounts

# csv_path = './discount.csv'
# with open(csv_path) as f:
#     rows = csv.reader(f, delimiter = ',')
#     next(f, None)

#     for row in rows:
#         Discount.objects.create(
#             name=row[1],
#             discount_content=row[2],
#             discount_percent=row[0]
#         )


# discount_products

# for product in Product.objects.all():
#     sale_random = random.randint(0,1)

#     if sale_random:
        
#         discount = Discount.objects.all()
#         discount_id = discount[random.randint(0, len(discount)-1)].id
        
#         discount_start = fake.date_time_this_decade()
#         discount_end = fake.date_time_this_decade()

#         if discount_start < discount_end:
#             DiscountProduct.objects.create(
#                 discount_start=discount_start,
#                 discount_end=discount_end,
#                 discount_id=discount_id,
#                 product_id=product.id,
#                 )


# packing_types
# PackingType.objects.create(name="냉장/종이포장")
# PackingType.objects.create(name="상온/종이포장")


# product_informations
# csv_path = './product.csv'
# with open(csv_path) as f:
#     rows = csv.reader(f, delimiter = ',')
#     next(f, None)

#     for row in rows:
#         if row[2]:
#             product_id = Product.objects.get(name=row[2]).id


#         packing_type_id  =random.randint(1,2)
    
#         ProductInformation.objects.create(       
#             sales_unit=row[6],
#             size=row[7],
#             origin=row[9],
#             shelf_life = "가급적 빨리 드시길 바랍니다.",
#             information=row[11],
#             packing_type_id=packing_type_id,
#             product_id=product_id
#             )

# Product_Shipping 

# for product_information in ProductInformation.objects.all():
#     ProductShipping.objects.create(
#         product_information_id=product_information.id,
#         shipping_classification_id=ShippingClassification.objects.get(id=1).id
#         )
#     ProductShipping.objects.create(
#         product_information_id=product_information.id,
#         shipping_classification_id=ShippingClassification.objects.get(id=2).id
#         )



# discount_product

# csv_path = './discount.csv'
# with open(csv_path) as f:
#     rows = csv.reader(f, delimiter = ',')
#     next(f, None)
#     new_rows= [] 
#     for row in rows:
#         new_rows.append(row)
    
#     for product in Product.objects.all():
#         tmp = random.randint(0,1)
#         row_index = random.randint(0, len(new_rows)-1)
#         row = new_rows[row_index]

#         if tmp:
#             product_id = product.id
#             discount_start = fake.date_time_this_decade()
#             discount_end = fake.date_time_this_decade()

#             if discount_start < discount_end:
#                 DiscountProduct.objects.create(     
#                     discount_start=discount_start,
#                     discount_end=discount_end,
#                     product_id=product_id,
#                     discount_id=random.randint(1, 16)
#                     )



