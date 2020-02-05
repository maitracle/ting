from django.shortcuts import render,redirect,get_object_or_404
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny

from users.models import User

def like_someone(request,user_id):
    likeduser = get_object_or_404(User,id=user_id)
    #user = request.user
    user= User.objects.get(username=request.user)

    if likeduser.likes


# Create your views here.
