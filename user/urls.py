from django.urls import path

from user.views  import (
    SignUp, 
    SignIn, 
    CheckEmail, 
    CheckID, 
    ShoppingBasket, 
    FrequentlyProduct,
    )

urlpatterns = [
    path('signup', SignUp.as_view()),
    path('signin', SignIn.as_view()),
    path('checkid', CheckID.as_view()),
    path('checkemail', CheckEmail.as_view()),
    path('shoppingbasket', ShoppingBasket.as_view()),
    path('frequentlyproduct', FrequentlyProduct.as_view()),
]