from rest_framework import serializers
from authentification.models import User

class UserBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_active']  # Only include the field you want to update
        read_only_fields = ['username', 'email', 'password']  # Exclude fields from being required in the update

    def update(self, instance, validated_data):
        # Update the is_active field
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_active = False
        instance.save()
        return instance
    



class UserUnblockSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_active']  # Only include the field you want to update
        read_only_fields = ['username', 'email', 'password']  # Exclude fields from being required in the update

    def update(self, instance, validated_data):
        # Update the is_active field
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_active = True
        instance.save()
        return instance
    


class UserCountSerializer(serializers.Serializer):
    user_count = serializers.IntegerField()
    provider_count = serializers.IntegerField() 

class ServicesCountSerializer(serializers.Serializer):
    carehome_count = serializers.IntegerField()
    person_count = serializers.IntegerField() 
    