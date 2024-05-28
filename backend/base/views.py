from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import TaskSerializer


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        
def myTasks(req):
    all_tasks = TaskSerializer(Task.objects.all(), many=True).data
    return JsonResponse(all_tasks, safe=False)

# login
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        # ...
        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# register
@api_view(['POST'])
def register(request):
    user = User.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password']
            )
    user.is_active = True
    user.is_staff = True
    user.save()
    return Response("new user born")

# logout
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    # Invalidate the token on the client side
    response = Response({"message": "Logged out successfully"}, status=200)
    response.delete_cookie('access_token')  # if you are storing JWT in cookies
    response.delete_cookie('refresh_token')  # if you are storing refresh token in cookies
    return response

#i’m protected
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def about(req):
    return Response("about")




@api_view(['GET'])
def index(req):
    return Response('hello')

@api_view(['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
def tasks(req, id=-1):
    if req.method == 'GET':
        if id > -1:
            try:
                temp_task = Task.objects.get(id=id)
                return Response(TaskSerializer(temp_task, many=False).data)
            except Task.DoesNotExist:
                return Response("Task not found", status=404)
        all_tasks = TaskSerializer(Task.objects.all(), many=True).data
        return Response(all_tasks)
    elif req.method == 'POST':
        tsk_serializer = TaskSerializer(data=req.data)
        if tsk_serializer.is_valid():
            tsk_serializer.save()
            return Response("Task created successfully", status=201)
        else:
            return Response(tsk_serializer.errors, status=400)
    elif req.method == 'PUT' or req.method == 'PATCH':
        task = get_object_or_404(Task, id=id)
        tsk_serializer = TaskSerializer(task, data=req.data, partial=req.method == 'PATCH')
        if tsk_serializer.is_valid():
            tsk_serializer.save()
            return Response("Task updated successfully")
        else:
            return Response(tsk_serializer.errors, status=400)
    elif req.method == 'DELETE':
        try:
            temp_task = Task.objects.get(id=id)
            temp_task.delete()
            return Response("Task deleted successfully")
        except Task.DoesNotExist:
            return Response("Task not found", status=404)