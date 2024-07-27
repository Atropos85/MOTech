from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

# router.register(r'payment',views.paymentViewSet) 
# router.register(r'paymentdetail',views.paymentdetailViewSet) 

# urlpatterns = [
#     path('', include(router.urls))
# ]

app_name = 'APIRest'
urlpatterns = [
    path(r'customer', customerView.as_view()), 
    path(r'customerBalance/<id>/', CustomerBalanceView.as_view()), 
    path(r'loan/<id>/', loanView.as_view()), 

]
    
