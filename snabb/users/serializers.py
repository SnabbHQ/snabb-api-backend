from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('profile_id', 'company_name', 'first_name', 'last_name',
                  'email', 'phone', 'verified', 'send_email_notifications',
                  'send_sms_notifications', 'user_lang', 'enterprise',
                  'created_at', 'updated_at')
                  
        read_only_fields = ('verified',)
