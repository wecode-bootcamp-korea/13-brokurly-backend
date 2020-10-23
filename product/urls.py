from django.urls   import path

from product.views import (
    Category,
    ProductList,
    MdChoice
)

urlpatterns = [
    path('category', Category.as_view()),
    path('product', ProductList.as_view()),
    path('home/md_choice', MdChoice.as_view())
]