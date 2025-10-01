# trips/urls.py
from django.urls import path
from .views import QuestionDetailAPIView, UserProfileAPIView, PostUpdateAPIView,PostDetailAPIView

urlpatterns = [
    # API調用----------------------------------------------------------------------------------------------------
    # path('get_api/', views.get_api, name='get_api'),
    path('api/user/', UserProfileAPIView.as_view(), name='user-create'),
    path('api/question/<int:question_id>/', QuestionDetailAPIView.as_view(), name='question-detail'),
    path('api/post/<str:phone>/', PostUpdateAPIView.as_view(), name='post-update'),
    path('api/post-detail/<str:phone>/', PostDetailAPIView.as_view(), name='post-detail'),

    # path('api/check-status/<str:phone>/', CheckStatusAPIView.as_view(), name='check-status'),
]






