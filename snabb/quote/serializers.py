from rest_framework import serializers
from .models import Quote, Task, Place
from snabb.address.serializers import AddressSerializer
from snabb.contact.serializers import ContactSerializer


class QuoteSerializer(serializers.ModelSerializer):
    tasks_info = serializers.SerializerMethodField('tasks')

    def tasks(self, obj):
        if obj.tasks:
            items = obj.tasks
            serializer = TaskSerializer(
                items, many=True, read_only=True)
            return serializer.data
        else:
            return None

    class Meta:
        model = Quote
        fields = (
            'quote_id',
            'quote_user',
            'tasks_info',
            'created_at', 'updated_at'
        )


class TaskSerializer(serializers.ModelSerializer):
    place_info = serializers.SerializerMethodField('place')
    contact_info = serializers.SerializerMethodField('contact')

    def place(self, obj):
        if obj.task_place:
            items = obj.task_place
            serializer = PlaceSerializer(
                items, many=False, read_only=True)
            return serializer.data
        else:
            return None

    def contact(self, obj):
        if obj.task_contact:
            items = obj.task_contact
            serializer = ContactSerializer(
                items, many=False, read_only=True)
            return serializer.data
        else:
            return None

    class Meta:
        model = Task
        fields = (
            'task_id',
            'place_info',
            'contact_info'
        )


class PlaceSerializer(serializers.ModelSerializer):
    address_info = serializers.SerializerMethodField('address')

    def address(self, obj):
        if obj.place_address:
            items = obj.place_address
            serializer = AddressSerializer(
                items, many=False, read_only=True)
            return serializer.data
        else:
            return None

    class Meta:
        model = Place
        fields = (
            'place_id',
            'description',
            'address_info'
        )
