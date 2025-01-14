from django_filters import rest_framework as filters
from .models import Blog

class BlogFilter(filters.FilterSet):
    title=filters.CharFilter(lookup_expr='icontains')
    content=filters.CharFilter(lookup_expr='icontains')
    author_name=filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model=Blog
        fields = ['title', 'content', 'author_name']
