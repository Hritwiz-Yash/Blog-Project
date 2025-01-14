#serializers.py
from rest_framework import serializers
from .models import Blog,Comment

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

from rest_framework import serializers
from .models import Comment, Blog

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'blog', 'parent', 'author_name', 'content', 'created_at', 'updated_at', 'replies']
        read_only_fields = ['author_name', 'blog']  # make author_name and blog read-only as they will be set automatically

    def get_replies(self, obj):
        child_comments = obj.replies.all()  # Retrieve replies
        return CommentSerializer(child_comments, many=True, context=self.context).data

    def create(self, validated_data):
        # Automatically set the author_name to the logged-in user's username
        request = self.context.get('request')
        validated_data['author_name'] = request.user.username
        
        # Automatically set the blog field using the blog_id passed in the URL
        blog_id = self.context.get('blog_id')
        blog = Blog.objects.get(pk=blog_id)
        validated_data['blog'] = blog
        
        return super().create(validated_data)
