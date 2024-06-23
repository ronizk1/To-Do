# # tasks/serializers.py

# from rest_framework import serializers
# from .models import Task,BigTask

# class TaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = '__all__'

# class BigTaskSerializer(serializers.ModelSerializer):
#     subtasks = TaskSerializer(many=True, read_only=True)

#     class Meta:
#         model = BigTask
#         fields = '__all__'


# newwwwwwwwwww
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    subtasks = serializers.ListField(
        child=serializers.JSONField(), required=False
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'due_date', 'image', 'is_big_task', 'subtasks', 'user']
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        user = self.context['request'].user
        task = Task.objects.create(user=user, **validated_data)

        for subtask_data in subtasks_data:
            subtask = Task.objects.create(user=user, **subtask_data, big_task=task)
        
        return task

    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.image = validated_data.get('image', instance.image)
        instance.is_big_task = validated_data.get('is_big_task', instance.is_big_task)
        instance.save()

        # Clear existing subtasks
        instance.subtasks.all().delete()

        # Add new subtasks
        user = self.context['request'].user
        for subtask_data in subtasks_data:
            Task.objects.create(user=user, **subtask_data, big_task=instance)

        return instance

class BigTaskSerializer(serializers.ModelSerializer):
    subtasks = TaskSerializer(many=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'due_date', 'image', 'is_big_task', 'subtasks', 'user']
        
        
# # serializers.py
# from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import UserProfile

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ['bio', 'location', 'birth_date', 'profile_picture']

# class UserSerializer(serializers.ModelSerializer):
#     profile = UserProfileSerializer(required=False)
#     password = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'password', 'email', 'profile']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         profile_data = validated_data.pop('profile', {})
#         password = validated_data.pop('password')
#         user = User.objects.create_user(**validated_data)
#         user.set_password(password)
#         user.save()
#         UserProfile.objects.update_or_create(user=user, defaults=profile_data)
#         return user

# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['name', 'location', 'birth_date', 'profile_picture']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.update_or_create(user=user, defaults=profile_data)
        return user



    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.location)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        if 'profile_picture' in validated_data:
            instance.profile_picture = validated_data['profile_picture']
        instance.save()
        return instance