import json
import random

from django.http import JsonResponse
from django.views import View

from product.models import (
    MainCategory, 
    SubCategory,
    Product,
    ProductInformation,
    ProductTag,
)

class Category(View):
    def get(self, request):
        try:
            category_version = request.GET.get('main', None)
            if category_version:
                if MainCategory.objects.all().exists():
                    categories = []
                    for index, main_category in enumerate(MainCategory.objects.all()):
                        if index == 16:
                            break
                        categories.append({ 
                            "id"             : main_category.id,
                            "name"           : main_category.name,
                            "imageUrl"       : main_category.image_url,
                            "imageActiveUrl" : main_category.image_active_url,
                            "sub_categories" : []
                        })

                        for sub_category in SubCategory.objects.filter(main_category_id=main_category.id):
                            categories[index]["sub_categories"].append({
                                "id"    : sub_category.id,
                                "name"  : sub_category.name
                            })
                else:
                    return JsonResponse({'message':'This category does not exist.'}, status=400)
        except ValueError:
            return JsonResponse({'message':'ValueError'}, status=400)
        return JsonResponse({'message':'SUCCESS', "categories":categories}, status=200)


class ProductList(View):
    def get(self, request):
        try:
            category_check   = request.GET.get('check', None)
            main_category_id = request.GET.get('main', None)
            sub_category_id  = request.GET.get('sub', None) 
            sort_type        = request.GET.get('sort_type', None) 
            
            categories = [sub_category.name for sub_category in SubCategory.objects.filter(main_category_id=main_category_id)]
     
            sort_type_set = {
                '0' : 'id',
                '1' : '-create_time',
                '2' : 'sales_count',
                '3' : 'price',
                '4' : '-price'    
            }
            
            sortings = [
                '추천순',
                '신상품순',
                '인기상품순',
                '낮은 가격순',
                '높은 가격순'   
            ]
         
            if int(category_check):
                sub_categories = [sub_category.id for sub_category in SubCategory.objects.filter(main_category_id=main_category_id)]
            else:
                sub_categories = [sub_category.id for sub_category in SubCategory.objects.filter(id=sub_category_id)]
            products = []
            
            for product in Product.objects.filter(sub_category__id__range=[min(sub_categories),max(sub_categories)]).order_by(sort_type_set[sort_type]):
                if product.discount.exists():
                    discount_product = product.discount.get()
                else:
                    discount_product = False
                products.append({
                    "id"               : product.id,
                    "name"             : product.name,
                    "content"          : product.content,
                    "imageUrl"         : product.image_url,
                    "discountPercent"  : discount_product.discount_percent if discount_product else 0,
                    "discountName"     : discount_product.name if discount_product else 0,
                    "discountContent"  : discount_product.discount_content if discount_product else "",
                    "discountPrice"    : product.price - product.price * discount_product.discount_percent * 0.01 if discount_product else 0,
                    "originalPrice"    : product.price
                })

        except ValueError:
            return JsonResponse({'message':'ValueError'}, status=400)
        return JsonResponse({'message':'SUCCESS', "categories":categories, "sortings":sortings, "products":products}, status=200)


class MdChoice(View):
    def get(self, request):
        try:
            main_category_id = request.GET.get('category', None)
            products = []
            for sub_category in SubCategory.objects.filter(main_category_id=main_category_id):
                for product in sub_category.product_set.filter()[:3]:
                    if product.discount.exists():
                        discount_product = product.discount.get()
                    else:
                        discount_product = False
                    products.append({
                        "id"               : product.id,
                        "name"             : product.name,
                        "content"          : product.content,
                        "imageUrl"         : product.image_url,
                        "discountPercent"  : discount_product.discount_percent if discount_product else 0,
                        "discountName"     : discount_product.name if discount_product else 0,
                        "discountContent"  : discount_product.discount_content if discount_product else "",
                        "discountPrice"    : product.price - product.price * discount_product.discount_percent * 0.01 if discount_product else 0,
                        "originalPrice"    : product.price
                    })

        except ValueError:
            return JsonResponse({'message':'ValueError'}, status=400)
        return JsonResponse({'message':'SUCCESS', "products":products}, status=200)


class ProductDetail(View):
    def get(self, request):
        try:
            product_id  = request.GET.get('product_item', None)
            if Product.objects.filter(id=product_id).exists():
                product = Product.objects.get(id=product_id)
                if product.discount.exists():
                    discount_product = product.discount.get()
                else:
                    discount_product = False
                if product.productinformation_set.exists():
                    product_information = product.productinformation_set.get()
                else:
                    product_information = False

                product_detail = {
                    "id"               : product.id,
                    "name"             : product.name,
                    "content"          : product.content,
                    "imageUrl"         : product.image_url,
                    "discountPercent"  : discount_product.discount_percent if discount_product else 0,
                    "discountName"     : discount_product.name if discount_product else 0,
                    "discountContent"  : discount_product.discount_content if discount_product else "",
                    "discountPrice"    : product.price - product.price * discount_product.discount_percent * 0.01 if discount_product else 0,
                    "originalPrice"    : product.price,
                    "salesUnit"        : product_information.sales_unit if product_information else "",
                    "size"             : product_information.size if product_information else "",
                    "productShipping"  : '/'.join([shipping.shipping_classification.name for shipping in product_information.productshipping_set.all()]) if product_information else "",
                    "origin"           : product_information.origin if product_information else "",
                    "pakingType"       : product_information.packing_type.name if product_information else "",
                    "shelfLife"        : product_information.shelf_life if product_information else "",
                    "information"      : product_information.information if product_information else "",
                }
                
        except ValueError:
            return JsonResponse({'message':'ValueError'}, status=400)
        return JsonResponse({'message':'SUCCESS', "product_detail":product_detail}, status=200)