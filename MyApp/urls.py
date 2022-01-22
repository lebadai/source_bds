from django.urls import path
from MyApp import views


app_name = "sale"

urlpatterns = [
    path('payment_policy/', views.PaymentPolicyView.as_view({'get': 'list', 'post': 'create'})),
    path('payment_policy/get/', views.PaymentPolicyView.as_view({'get': 'get'})),
    path('payment_policy/', views.PaymentPolicyView.as_view({'delete': 'delete'})),
    path('payment_policy/delete_all/', views.PaymentPolicyView.as_view({'delete': 'delete_payment_policy'})),
    path('payment_policy/create_file/', views.PaymentPolicyFileView.as_view({'post': 'create_policy_file'})),
    path('payment_policy/update_file/', views.PaymentPolicyFileView.as_view({'put': 'put_policy_file'})),
    path('payment_policy/delete_file/', views.PaymentPolicyFileView.as_view({'delete': 'delete_policy_file'})),
    path('payment_policy/create_group_file/', views.PaymentPolicyFileView.as_view({'post': 'create_policy_group_file'})),
    path('payment_policy/delete_group_file/', views.PaymentPolicyFileView.as_view({'delete': 'delete_policy_group_file'})),
    path('payment_policy/create_group_detail_value_file/', views.PaymentPolicyFileView.as_view({'post': 'create_policy_group_detail_value_file'})),
    path('payment_policy/delete_group_detail_value_file/', views.PaymentPolicyFileView.as_view({'delete': 'delete_policy_group_detail_value_file'})),


]
