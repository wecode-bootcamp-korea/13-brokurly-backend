from django.urls import path

from user.views  import (
    SignUp, 
    SignIn, 
    CheckEmail, 
    CheckID, 
    RegisterShoppingBasket, 
    ViewShoppingBasket, 
    RegisterFrequentlyProduct, 
    UpdateBasketQuantity, 
    DeleteShoppingBasket, 
    ViewFrequentlyProduct,
    DeleteFrequentlyProduct
    )

urlpatterns = [
    path('signup', SignUp.as_view()),
    path('signin', SignIn.as_view()),
    path('checkid', CheckID.as_view()),
    path('checkemail', CheckEmail.as_view()),
    path('register_shoppingbasket', RegisterShoppingBasket.as_view()),
    path('view_shoppingbasket', ViewShoppingBasket.as_view()),
    path('register_frequentlyproduct', RegisterFrequentlyProduct.as_view()),
    path('update_basketquantity', UpdateBasketQuantity.as_view()),
    path('delete_shoppingbasket', DeleteShoppingBasket.as_view()),
    path('view_frequentlyproduct', ViewFrequentlyProduct.as_view()),
    path('delete_frequentlyproduct', DeleteFrequentlyProduct.as_view()),
]