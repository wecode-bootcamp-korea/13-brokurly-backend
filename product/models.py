from django.db   import models

class MainCategory(models.Model):
    name             = models.CharField(max_length=50)
    image_url        = models.CharField(max_length=200)
    image_active_url = models.CharField(max_length=200)

    class Meta:
        db_table = 'main_categories'


class SubCategory(models.Model):
    name          = models.CharField(max_length=50)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories'


class Product(models.Model):
    name             = models.CharField(max_length=50)
    price            = models.FloatField(default=0)
    content          = models.CharField(max_length=1000)
    is_sold_out      = models.BooleanField(null=True)
    image_url        = models.CharField(max_length=200)
    sales_count      = models.IntegerField(default=0)
    create_time      = models.DateTimeField(auto_now_add=True)
    sub_category     = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    product_question = models.ManyToManyField('user.User', through='ProductQuestion', related_name='product_questions')
    discount         = models.ForeignKey('Discount', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'products'


class Discount(models.Model):
    name             = models.CharField(max_length=50)
    discount_content = models.CharField(max_length=50)
    discount_percent = models.FloatField()

    class Meta:
        db_table = 'discounts'

        
class PackingType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'packing_types'


class ShippingClassification(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'shipping_classifications'


class ProductInformation(models.Model):
    sales_unit              = models.CharField(max_length=50, null=True, blank=True)
    size                    = models.CharField(max_length=100, null=True, blank=True)
    origin                  = models.CharField(max_length=50, null=True, blank=True)
    shelf_life              = models.CharField(max_length=50, null=True, blank=True)
    allergy_information     = models.CharField(max_length=200, null=True, blank=True)
    note                    = models.CharField(max_length=1000, null=True, blank=True)
    information             = models.CharField(max_length=1000, null=True, blank=True)
    shipping_classification = models.ManyToManyField('ShippingClassification', through='ProductShipping')
    packing_type            = models.ForeignKey(PackingType, on_delete=models.CASCADE)
    product                 = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_informations'


class ProductShipping(models.Model):
    product_information     = models.ForeignKey(ProductInformation, on_delete=models.CASCADE)
    shipping_classification = models.ForeignKey(ShippingClassification, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_shippings'


class ProductTag(models.Model):
    name    = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_tags'


class ProductQuestion(models.Model):
    name        = models.CharField(max_length=100)
    content     = models.CharField(max_length=1000)
    create_time = models.DateTimeField(auto_now_add=True)
    user        = models.ForeignKey('user.User', on_delete=models.CASCADE)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_questions'


class MorningDeliveryArea(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'morning_delivery_areas'