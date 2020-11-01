from django.urls import path

from user.views  import (
    SignUpView,
    SignInView,
    CheckEmailView,
    CheckIdView,
    FindIdView,
    FindPasswordView,
    ShoppingBasketView, 
    ShoppingBasketCheckView,
    FrequentlyProductView,
    ProductReviewView,
    UserDataView,
    UserReviewView,
    OrderHistoryView,
    SendSmsView,
    CheckSmsView,
    )

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/checkid', CheckIdView.as_view()),
    path('/checkemail', CheckEmailView.as_view()),
    path('/findid', FindIdView.as_view()),
    path('/findpassword', FindPasswordView.as_view()),
    path('/shoppingbasket', ShoppingBasketView.as_view()),
    path('/shoppingbasket-check', ShoppingBasketCheckView.as_view()),
    path('/frequentlyproduct', FrequentlyProductView.as_view()),
    path('/product/<int:product_id>/reviews', ProductReviewView.as_view()),
    path('/user-data', UserDataView.as_view()),
    path('/user-review', UserReviewView.as_view()),
    path('/orderhistory', OrderHistoryView.as_view()),
    path('/sendsms', SendSmsView.as_view()),
    path('/checksms', CheckSmsView.as_view())
]