from django.shortcuts import render
from rest_framework import generics

from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer


class PostAPIViews(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
