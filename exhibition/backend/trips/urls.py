# trips/urls.py
from django.urls import path

from .views import (
    QuestionDetailAPIView,
    UserProfileAPIView,
    PostUpdateAPIView,
    PostDetailAPIView,
    market_list,
    init_content2,
    ar_scan_view
)
from .views_market_questions import market_questions

urlpatterns = [
    path('api/user/', UserProfileAPIView.as_view(), name='user-create'),
    path(
        'api/question/<int:question_id>/',
        QuestionDetailAPIView.as_view(),
        name='question-detail'
    ),
    path(
        'api/post/<str:phone>/',
        PostUpdateAPIView.as_view(),
        name='post-update'
    ),
    path(
        'api/post-detail/<str:phone>/',
        PostDetailAPIView.as_view(),
        name='post-detail'
    ),
    path('api/markets/', market_list, name='market-list'),
    path(
        'api/market-questions/',
        market_questions,
        name='market-questions'
    ),
    path('api/init-content2/', init_content2, name='init-content2'),
    # AR 掃描動態路由（統一處理所有 level）
    path('arScan<int:level>/', ar_scan_view, name='ar-scan'),
]
