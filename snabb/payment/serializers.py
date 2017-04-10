from rest_framework import serializers
from .models import Card


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        read_only_fields = (
            'card_id', 'user_id', 'fingerprint', 'card_info',
            'created_at', 'updated_at'
        )
        fields = (
            'card_id',
            'user_id',
            'fingerprint', 'default_card', 'card_info',
            'created_at', 'updated_at'
        )
