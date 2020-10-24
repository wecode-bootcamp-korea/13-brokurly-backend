from django.db      import models

class Gender(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'genders'


class User(models.Model):
    user_id                      = models.CharField(max_length=50)
    password                     = models.CharField(max_length=200)
    user_name                    = models.CharField(max_length=50)
    email                        = models.EmailField(max_length=50)
    phone                        = models.CharField(max_length=50)
    address                      = models.CharField(max_length=50)
    gender                       = models.ForeignKey(Gender, on_delete=models.CASCADE)
    date_of_birth                = models.CharField(max_length=50, null=True)
    recommender                  = models.CharField(max_length=50, null=True)
    event                        = models.CharField(max_length=50, null=True)
    is_privacy_policy            = models.BooleanField(default=False)
    is_sms_agreed                = models.BooleanField(default=False)
    is_email_agreed              = models.BooleanField(default=False)
    shopping_basket              = models.ManyToManyField('product.Product', through='ShoppingBasket', related_name='shopping_baskets')
    orders                       = models.ManyToManyField('product.Product', through='Order', related_name='orders')
    frequently_purchased_product = models.ManyToManyField('product.Product', through='FrequentlyPurchasedProduct', related_name='frequently_purchased_products')
    reviews                      = models.ManyToManyField('product.Product', through='Review', related_name='reviews')

    class Meta:
        db_table = 'users'


class FrequentlyPurchasedProduct(models.Model):
    description = models.CharField(max_length=50)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    product     = models.ForeignKey('product.Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'frequently_purchased_products'


class Reserve(models.Model):
    date     = models.DateField(auto_now_add=True)
    content  = models.CharField(max_length=1000)
    validity = models.DateField(auto_now_add=True)
    price    = models.FloatField()
    user     = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'reserves'


class Order(models.Model):
    name         = models.CharField(max_length=100)
    order_number = models.IntegerField(default=0)
    price        = models.FloatField()
    create_time  = models.DateTimeField(auto_now_add=True)
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    product      = models.ForeignKey('product.Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'


class ShoppingBasket(models.Model):
    quantity = models.IntegerField(default=1)
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    product  = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    option   = models.IntegerField(default=0)
    checked  = models.BooleanField(default=True)

    class Meta:
        db_table = 'shopping_baskets'


class UserRank(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_ranks'    


class Review(models.Model):
    title       = models.CharField(max_length=50)
    create_time = models.DateField(auto_now_add=True)
    help_count  = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    content     = models.CharField(max_length=1000)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    product     = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    option      = models.IntegerField(default=0)

    class Meta:
        db_table = 'reviews'