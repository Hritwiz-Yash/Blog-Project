
# --------------------------------------

# urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import BlogListCreateView, BlogRetrieveUpdateDestroyView,UserRegistrationView,UserBlogsView,CommentListCreateView, BlogFilterSearchView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('blogs/', BlogListCreateView.as_view(), name='blog-list-create'),
    path('blogs/<int:pk>/', BlogRetrieveUpdateDestroyView.as_view(), name='blog-detail'),
    path('auth/register/', UserRegistrationView.as_view(), name='user_register'),
    path('blogs/<int:pk>/restore/', BlogRetrieveUpdateDestroyView.as_view(), name='blog-restore'),
    path('blogs/<int:blog_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('blogs/myblogs/', UserBlogsView.as_view(), name='user-blogs'),
    path('blogs/filter-search/', BlogFilterSearchView.as_view(), name='blog-filter-search'),

]


