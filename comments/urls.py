from django.urls import path

from . import views


urlpatterns = [
    path('', views.CommentListAPIView.as_view(), name='comment_list'),
    path('add/', views.CommentCreateAPIView.as_view(), name='add_comment'),
    path('captcha/', views.CaptchaAPIView.as_view()),
]
