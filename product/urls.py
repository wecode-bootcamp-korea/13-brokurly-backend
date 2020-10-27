from django.urls   import path

from product.views import (
    MainPageSection,
    Category,
    ProductList,
    ProductDetail,
    MdChoice,
    RelatedProduct,
    HomeProduct,
    SaleProduct
)

urlpatterns = [
    path('', ProductList.as_view()),
    path('/<int:product_id>', ProductDetail.as_view()),
    path('/category', Category.as_view()),
    path('/home/section', MainPageSection.as_view()),
    path('/home/md-choice', MdChoice.as_view()),
    path('/related-products/<int:product_id>', RelatedProduct.as_view()),
    path('/home', HomeProduct.as_view()),
    path('/sales', SaleProduct.as_view())
]