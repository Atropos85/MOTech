from django.urls import path, include
from rest_framework import routers
from APIRest import views

router = routers.DefaultRouter()
router.register(r'customers',views.customerViewSet) 
router.register(r'loans',views.loanViewSet) 
router.register(r'payment',views.paymentViewSet) 
router.register(r'paymentdetail',views.paymentdetailViewSet) 

urlpatterns = [
    path('', include(router.urls))
]