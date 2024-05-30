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
