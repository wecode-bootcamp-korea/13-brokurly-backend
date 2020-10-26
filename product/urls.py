from django.urls   import path

from product.views import (
    MainPageSection,
    Category,
    ProductList,
    ProductDetail,
    MdChoice,
    ProductSearch,
    RelatedProduct,
    NewProduct,
    BestProduct
)

urlpatterns = [
    path('main/section', MainPageSection.as_view()),
    path('category', Category.as_view()),
    path('product', ProductList.as_view()),
    path('home/md_choice', MdChoice.as_view()),
    path('product/product_detail', ProductDetail.as_view()),
    path('search', ProductSearch.as_view()),
    path('related_product', RelatedProduct.as_view()),
    path('new_products', NewProduct.as_view()),
    path('best_products', BestProduct.as_view())
]