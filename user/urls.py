from django.urls import path

from user.views  import (
    SignUp, 
    SignIn, 
    CheckEmail, 
    CheckID, 
    ShoppingBasketView, 
    ShoppingBasketCheckView,
    FrequentlyProductView,
    UserReview,
    ProductReview,
    )

urlpatterns = [
    path('signup', SignUp.as_view()),
    path('signin', SignIn.as_view()),
    path('checkid', CheckID.as_view()),
    path('checkemail', CheckEmail.as_view()),
    path('shoppingbasket', ShoppingBasketView.as_view()),
    path('shoppingbasket_check', ShoppingBasketCheckView.as_view()),
    path('frequentlyproduct', FrequentlyProductView.as_view()),
    path('user_review', UserReview.as_view()),
    path('product_review', ProductReview.as_view()),
]