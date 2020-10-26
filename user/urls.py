from user.models import Order
from django.urls import path

from user.views  import (
    SignUp, 
    SignIn, 
    CheckEmail, 
    CheckID,
    FindID,
    ShoppingBasketView, 
    ShoppingBasketCheckView,
    FrequentlyProductView,
    ProductReview,
    UserDataView,
    UserReview,
    OrderHistory,
    )

urlpatterns = [
    path('/signup', SignUp.as_view()),
    path('/signin', SignIn.as_view()),
    path('/checkid', CheckID.as_view()),
    path('/checkemail', CheckEmail.as_view()),
    path('/findid', FindID.as_view()),
    path('/shoppingbasket', ShoppingBasketView.as_view()),
    path('/shoppingbasket-check', ShoppingBasketCheckView.as_view()),
    path('/frequentlyproduct', FrequentlyProductView.as_view()),
    path('/product-review', ProductReview.as_view()),
    path('/user-data', UserDataView.as_view()),
    path('/myreview', UserReview.as_view()),
    path('/orderhistory', OrderHistory.as_view()),
]