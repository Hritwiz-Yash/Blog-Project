
# views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Blog,Comment
from .serializers import BlogSerializer, User,CommentSerializer
from rest_framework.exceptions import NotFound
from rest_framework import generics
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import BlogFilter



class BlogListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve the list of all blogs with pagination
        """
        blogs = Blog.objects.active()
        paginator = PageNumberPagination()
        paginator.page_size = 4  # Set page size to 4

        result_page = paginator.paginate_queryset(blogs, request)
        serializer = BlogSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """
        Create a new blog
        """
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author_name=request.user.username)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated]

    # def get_object(self, pk):
    #     try:
    #         return Blog.objects.get(pk=pk)
    #     except Blog.DoesNotExist:
    #         raise NotFound(detail="Blog not found")
    def get_object(self,pk):
        try:
            blog=Blog.objects.get(pk=pk,is_deleted=False)
            return blog   
        except Blog.DoesNotExist:
            raise NotFound(detail='Blog not found')
    def get(self, request, pk):
        """
        Retrieve a specific blog by its ID
        """
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a specific blog by its ID (replace the whole blog)
        """
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Partially update a specific blog by its ID
        """
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a specific blog by its ID
        """
        blog = self.get_object(pk)
        blog.delete()
        return Response({"detail": "Blog soft-deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
 
    def post(self, request, pk):
        """
        Restore a soft-deleted blog by its ID
        """
        try:
            blog = Blog.objects.get(pk=pk, is_deleted=True)  # Find only soft-deleted records
            blog.restore()  # Restore the blog
            return Response({"detail": "Blog restored successfully."}, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            raise NotFound(detail="Soft-deleted blog not found")

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    
        
class UserBlogsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve all blogs created by the authenticated user
        """
        blogs = Blog.objects.filter(author_name=request.user.username, is_deleted=False)  # Filter by author and exclude deleted blogs
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, blog_id):
        """
        Retrieve all comments for a blog post with nested replies
        """
        try:
            blog = Blog.objects.get(pk=blog_id, is_deleted=False)
        except Blog.DoesNotExist:
            raise NotFound(detail="Blog not found")

        comments = Comment.objects.filter(blog=blog, parent=None)  # Get only top-level comments || For Comment
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, blog_id):
        """
        Create a new comment for a blog post
        """
        try:
            blog = Blog.objects.get(pk=blog_id, is_deleted=False)
        except Blog.DoesNotExist:
            raise NotFound(detail="Blog not found")

        # Pass the blog_id to the serializer context
        serializer = CommentSerializer(data=request.data, context={'request': request, 'blog_id': blog_id})
        if serializer.is_valid():
            serializer.save()  # The blog field is automatically set in the serializer
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogFilterSearchView(ListAPIView):
    """
    View to filter and search blogs
    """
    queryset=Blog.objects.active()
    serializer_class=BlogSerializer
    permission_classes=[IsAuthenticated]

    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class= BlogFilter
    search_fields=['title', 'content', 'author_name']
    ordering_fields=['created_at','updated_at']

    def get(self, request,*args,**kwargs):
        """
        Return the filtered and searched list of blogs
        """
        return super().get(request, *args, **kwargs)




