from rest_framework import serializers
from providerdashboard.models import CareHome,ProfessionalPerson,TimeSlot,Booking,BookingNotification,CareHomeReview,ProfessionalPersonReview
from authentification.serializers import UserSerializer




class CareHomeSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()

    class Meta:
        model = CareHome
        fields='__all__'
    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_total_reviews(self, obj):
        return obj.get_total_reviews()

class CareHomeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareHome
        fields = '__all__'
        # Set 'required' to False for 'imageone' during updates
        extra_kwargs = {
            'imageone': {'required': False},
        }


class PersonSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    class Meta:
        model = ProfessionalPerson
        fields='__all__'
    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_total_reviews(self, obj):
        return obj.get_total_reviews()

class PersonUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalPerson
        fields = '__all__'
        # Set 'required' to False for 'imageone' during updates
        extra_kwargs = {
            'profileimage': {'required': False},
        }


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'provider', 'professional', 'date', 'start_time', 'end_time','is_booked']

class TimeSlotUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['is_booked']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['professional', 'user', 'date', 'timeslot', 'status', 'payment_amount']

class BookingViewSerializer(serializers.ModelSerializer):
    professional = PersonSerializer()
    user = UserSerializer()
    timeslot = TimeSlotSerializer()

    class Meta:
        model = Booking
        fields = ['id','professional', 'user', 'date', 'timeslot', 'status', 'payment_amount']



class BookingNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=BookingNotification
        fields='__all__'

class CareHomeReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=CareHomeReview
        fields='__all__'

class CareHomeReviewBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareHomeReview
        fields = ['is_block']  # Only include the field you want to update
        read_only_fields = ['user', 'CareHome', 'rating','review','add_time']  # Exclude fields from being required in the update

    def update(self, instance, validated_data):
        # Update the is_active field
        instance.is_block = validated_data.get('is_block', instance.is_block)
        instance.is_block = True
        instance.save()
        return instance
    
class CareHomeReviewUnblockSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareHomeReview
        fields = ['is_block']  # Only include the field you want to update
        read_only_fields = ['user', 'CareHome', 'rating','review','add_time']  # Exclude fields from being required in the update

    def update(self, instance, validated_data):
        # Update the is_active field
        instance.is_block = validated_data.get('is_block', instance.is_block)
        instance.is_block = False
        instance.save()
        return instance

class ProfessionalPersonReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProfessionalPersonReview
        fields='__all__'

class ProfessionalsReviewBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalPersonReview
        fields = ['is_block']  # Only include the field you want to update
        read_only_fields = ['user', 'ProfessionalPerson', 'rating','review','add_time']  # Exclude fields from being required in the update

    def update(self, instance, validated_data):
        # Update the is_active field
        instance.is_block = validated_data.get('is_block', instance.is_block)
        instance.is_block = True
        instance.save()
        return instance
    
class ProfessionalsReviewUnblockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalPersonReview
        fields = ['is_block']  # Only include the field you want to update
        read_only_fields = ['user', 'ProfessionalPerson', 'rating','review','add_time']  # Exclude fields from being required in the update

    def update(self, instance, validated_data):
        # Update the is_active field
        instance.is_block = validated_data.get('is_block', instance.is_block)
        instance.is_block = False
        instance.save()
        return instance

