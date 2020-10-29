from django.urls   import path

from product.views import (
    MainPageSectionView,
    CategoryView,
    ProductListView,
    ProductDetailView,
    MdChoiceView,
    RelatedProductView,
    HomeProductView,
    SaleProductView
)

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/category', CategoryView.as_view()),
    path('/home/section', MainPageSectionView.as_view()),
    path('/home/md-choice', MdChoiceView.as_view()),
    path('/<int:product_id>/related-products', RelatedProductView.as_view()),
    path('/home', HomeProductView.as_view()),
    path('/sales', SaleProductView.as_view())
]