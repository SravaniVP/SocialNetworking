from django.urls import path

from . import views

urlpatterns = [
    path('index',views.index, name='index'),
    path('',views.signup,name='signup'),
    path('mystatus/', views.status_view, name = 'mystatus'),
    path('success/', views.success, name = 'success'),
    path('status/<int:pk>/delete/', views.StatusDeleteView.as_view(), name='StatusDeleteView'),
    path('status/detail/<int:id>/',views.detail_status, name='detail_status'),
    path('status/like',views.like_status,name="like_status"),
    ]