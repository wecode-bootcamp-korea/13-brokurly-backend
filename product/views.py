import json
import random
import datetime

from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Q
from dateutil.relativedelta import relativedelta

from product.models         import (
    MainCategory, 
    SubCategory,
    Product,
    ProductInformation,
    ProductTag
)

class CategoryView(View):
    def get(self, request):
        try:
            main_categories = MainCategory.objects.prefetch_related('subcategory_set').all()
            if main_categories.exists():
                categories = [{ 
                    'id'             : main_category.id,
                    'name'           : main_category.name,
                    'imageUrl'       : main_category.image_url,
                    'imageActiveUrl' : main_category.image_active_url,
                    'sub_categories' : [{
                        'id'    : sub_category.id,
                        'name'  : sub_category.name
                    } for sub_category in main_category.subcategory_set.all()]
                } for main_category in main_categories]

                return JsonResponse({'message':'SUCCESS', 'categories':categories}, status=200)
            else:
                return JsonResponse({'message':'This category does not exist.'}, status=404)

        except ValueError:
            return JsonResponse({'message':'VALUE_ERROR'}, status=400)


class ProductListView(View):
    def get(self, request):
        try:
            main_category_id = request.GET.get('main')
            sub_category_id  = request.GET.get('sub') 
            ordering         = request.GET.get('ordering') 
            search           = request.GET.get('search')
            products         = Product.objects.select_related('sub_category', 'sub_category__main_category', 'discount')
            
            filters = {}

            if main_category_id:
                filters['sub_category__main_category__id'] = main_category_id
            
                product = products.first()

                main_category = {
                'id'       : product.sub_category.main_category.id,
                'name'     : product.sub_category.main_category.name,
                'imageUrl' : product.sub_category.main_category.image_active_url
                }

                sub_categories = [{
                'id'   : sub_category.id,
                'name' : sub_category.name
            } for sub_category in SubCategory.objects.filter(main_category_id=main_category_id)]

            if sub_category_id:
                filters['sub_category_id'] = sub_category_id

            sort_type_set = {
                '0' : 'id',
                '1' : '-create_time',
                '2' : '-sales_count',
                '3' : 'price',
                '4' : '-price'    
            }

            sortings = [
                {    
                    'id'   : 0, 
                    'name' : '추천순'
                },
                {   
                    'id'   : 1, 
                    'name' : '신상품순'
                },
                {
                    'id'   : 2, 
                    'name' : '인기상품순'
                },
                {
                    'id'   : 3, 
                    'name' : '낮은 가격순'
                },
                {
                    'id'   : 4, 
                    'name' : '높은 가격순'
                }   
            ]

            if ordering in sort_type_set:
                products = products.order_by('is_sold_out', sort_type_set[ordering])

            q = Q()

            if search:
                q &= Q(name__contains=search) | Q(content__contains=search) | Q(productinformation__information__contains=search)

            products = [{
                'id'              : product.id,
                'name'            : product.name,
                'content'         : product.content,
                'imageUrl'        : product.image_url,
                'isSoldOut'       : product.is_sold_out,
                'discountPercent' : product.discount.discount_percent,
                'discountName'    : product.discount.name,
                'discountContent' : product.discount.discount_content,
                'discountPrice'   : product.price - int(product.price * product.discount.discount_percent * 0.01),
                'originalPrice'   : product.price
            } for product in products.filter(q, **filters)]
            
            if search:  
                return JsonResponse({'message':'SUCCESS', 'products':products}, status=200)

        except ValueError:
            return JsonResponse({'message':'VALUE_ERROR'}, status=400)
        return JsonResponse({'message':'SUCCESS', 'mainCategories':main_category, 'subCategories':sub_categories, 'sortings':sortings,'products':products}, status=200)


class MdChoiceView(View):
    def get(self, request):
        try:
            main_category_id = request.GET.get('category', None)
            products         = Product.objects.select_related('sub_category', 'sub_category__main_category', 'discount')

            products = [{
                'id'              : product.id,
                'name'            : product.name,
                'content'         : product.content,
                'imageUrl'        : product.image_url,
                'isSoldOut'       : product.is_sold_out,
                'discountPercent' : product.discount.discount_percent,
                'discountName'    : product.discount.name,
                'discountContent' : product.discount.discount_content,
                'discountPrice'   : product.price - int(product.price * product.discount.discount_percent * 0.01),
                'originalPrice'   : product.price
            } for product in products.filter(Q(sub_category__main_category__id=main_category_id)).order_by('?', 'is_sold_out')[:random.randint(10,12)]]

        except ValueError:
            return JsonResponse({'message':'VALUE_ERROR'}, status=400)
        return JsonResponse({'message':'SUCCESS', 'products':products}, status=200)


class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.prefetch_related('productinformation_set').get(id=product_id)
            product.sales_count += 1
            product.save()

            if product.productinformation_set.exists():
                product_information = product.productinformation_set.get()
            else:
                product_information = False

            product_detail = {
                'id'               : product.id,
                'name'             : product.name,
                'content'          : product.content,
                'imageUrl'         : product.image_url,
                'discountPercent'  : product.discount.discount_percent,
                'discountName'     : product.discount.name,
                'discountContent'  : product.discount.discount_content,
                'discountPrice'    : product.price - int(product.price * product.discount.discount_percent * 0.01),
                'originalPrice'    : product.price,
                'salesUnit'        : product_information.sales_unit if product_information else '',
                'size'             : product_information.size if product_information else '',
                'otherInformation' : [
                    {
                        'category'  :'배송구분', 
                        'description':'/'.join([shipping.shipping_classification.name for shipping in product_information.productshipping_set.all()]) if product_information else ""
                    },
                    {
                        'category'  :'원산지', 
                        'description': product_information.origin if product_information else ''
                    },
                    {
                        'category'  :'포장타입', 
                        'description': product_information.packing_type.name if product_information else ''
                    },
                    {
                        'category'  :'유통기한', 
                        'description': product_information.shelf_life if product_information else ''
                    },
                    {
                        'category'  :'알레르기정보',
                        'description': product_information.allergy_information if product_information else ''
                    },
                    {
                        'category'  :'안내사항', 
                        'description': product_information.information if product_information else ''
                    }
                ]
            }
                
        except ValueError:
            return JsonResponse({'message':'VALUE_ERROR'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'message':'Product does not exist'}, status=404)
        return JsonResponse({'message':'SUCCESS', 'product_detail':product_detail}, status=200)


class MainPageSectionView(View):
    def get(self, request):
        try:

            section_types = [
                '?',
                '-create_time',
                'sales_count',
                '-discount__discount_percent',
                '?'
            ]

            section_list = [{
                    'products' : [{
                    'id'              : product.id,
                    'name'            : product.name,
                    'content'         : product.content,
                    'imageUrl'        : product.image_url,
                    'isSoldOut'       : product.is_sold_out,
                    'discountPercent' : product.discount.discount_percent,
                    'discountName'    : product.discount.name,
                    'discountContent' : product.discount.discount_content,
                    'discountPrice'   : product.price - int(product.price * product.discount.discount_percent * 0.01),
                    'originalPrice'   : product.price
                } for product in Product.objects.select_related('discount').filter(is_sold_out=False).order_by(section_type)[:random.randint(10,12)]]
            }for section_type in section_types]

        except ValueError:
            return JsonResponse({'message':'VALUE_ERROR'}, status=400)
        return JsonResponse({'message':'SUCCESS', 'section_list':section_list}, status=200)


class RelatedProductView(View):
    def get(self, request, product_id):
        try:
            sub_category_id = Product.objects.get(pk=product_id).sub_category.id
            related_products = [{
                'id'            : product.id,
                'name'          : product.name,
                'imageUrl'      : product.image_url,
                'originalPrice' : product.price
            } for product in Product.objects.filter(sub_category_id=sub_category_id, is_sold_out=False).order_by('?')]

        except ValueError:
            return JsonResponse({'message':'VALUE_ERROR'}, status=400)
        return JsonResponse({'message':'SUCCESS', 'related_products':related_products}, status=200)


class HomeProductView(View):
    def get(self, request):
        try:
            product_type = request.GET.get('type')
            ordering     = request.GET.get('ordering')
            products     = Product.objects.select_related('discount')

            if product_type == 'new':
                products = products.filter(create_time__gt=datetime.datetime.now() - relativedelta(months=1))

            if product_type == 'best':
                products = products.filter(sales_count__gt=3000)

            sort_type_set = {
                '0' : '-create_time',
                '1' : '-sales_count',
                '2' : 'price',
                '3' : '-price'    
            }
    
            sortings = [
                {    
                    'id' : 0, 
                    'name' : '신상품순',
                },
                {   
                    'id' : 1, 
                    'name' : '인기상품순',
                },
                {
                    'id' : 2, 
                    'name' : '낮은 가격순',
                },
                {
                    'id' : 3, 
                    'name' : '높은 가격순',
                } 
            ]

            new_products = [{
                'id'              : product.id,
                'name'            : product.name,
                'content'         : product.content,
                'imageUrl'        : product.image_url,
                'isSoldOut'       : product.is_sold_out,
                'discountPercent' : product.discount.discount_percent,
                'discountName'    : product.discount.name,
                'discountContent' : product.discount.discount_content,
                'discountPrice'   : product.price - int(product.price * product.discount.discount_percent * 0.01),
                'originalPrice'   : product.price
            } for product in products.order_by('is_sold_out', sort_type_set[ordering])]

        except ValueError:
            return JsonResponse({'message':'VALUE_ERROR'}, status=400)
        return JsonResponse({'message':'SUCCESS', 'sortings':sortings, 'new_products':new_products}, status=200)
            

class SaleProductView(View):
    def get(self, request):
        try:
            ordering = request.GET.get('ordering')

            sort_type_set = {
                '0' : '-discount__discount_percent',
                '1' : '-create_time',
                '2' : '-sales_count',
                '3' : 'price',
                '4' : '-price'
            }
            
            sortings = [
                {    
                    'id' : 0, 
                    'name' : '혜택순',
                },
                {   
                    'id' : 1, 
                    'name' : '신상품순',
                },
                {
                    'id' : 2, 
                    'name' : '인기상품순',
                },
                {
                    'id' : 3, 
                    'name' : '낮은 가격순',
                },
                {
                    'id' : 4, 
                    'name' : '높은 가격순'
                }   
            ]
            
            sale_products = [{
                'id'              : product.id,
                'name'            : product.name,
                'content'         : product.content,
                'imageUrl'        : product.image_url,
                'isSoldOut'       : product.is_sold_out,
                'discountPercent' : product.discount.discount_percent,
                'discountName'    : product.discount.name,
                'discountContent' : product.discount.discount_content,
                'discountPrice'   : product.price - int(product.price * product.discount.discount_percent * 0.01),
                'originalPrice'   : product.price
            } for product in Product.objects.select_related('discount').exclude(discount__discount_percent=0).order_by('is_sold_out', sort_type_set[ordering])]

        except ValueError:
            return JsonResponse({'message':'VALUE_ERROR'}, status=400)
        return JsonResponse({'message':'SUCCESS', 'sortings':sortings, 'sale_products':sale_products}, status=200)