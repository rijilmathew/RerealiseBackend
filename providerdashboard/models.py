from django.db import models
from authentification.models import User
from django.db.models import Sum


# Create your models here.

class CareHome(models.Model):
      provider = models.ForeignKey(User, on_delete=models.CASCADE)
      carehomename=models.CharField(max_length=20)
      address_1 = models.TextField(max_length=20)
      address_2 = models.TextField(max_length=20,null=True,blank=True)
      address_3 = models.TextField(max_length=20,null=True,blank=True)
      imageone=models.ImageField(upload_to='care_home_images/')
      type_of_service=models.TextField()
      facilities=models.TextField(null=True,blank=True)
      phone_number=models.CharField(max_length=12)
      email=models.EmailField()
      website_link=models.URLField(null=True,blank=True)
      is_active = models.BooleanField(default=False)
      latitude = models.DecimalField(max_digits=50, decimal_places=30, null=True)
      longitude = models.DecimalField(max_digits=50, decimal_places=30, null=True)
    
      def __str__(self):
         return self.provider.username
      
      def get_average_rating(self):
        total_reviews = CareHomeReview.objects.filter(CareHome=self).count()
        if total_reviews == 0:
            return 0
        total_ratings = CareHomeReview.objects.filter(CareHome=self).aggregate(Sum('rating'))['rating__sum']
        average_rating = total_ratings / total_reviews
        return round(average_rating, 2)

      def get_total_reviews(self):
        return CareHomeReview.objects.filter(CareHome=self).count()


class ProfessionalPerson(models.Model):
     provider = models.ForeignKey(User, on_delete=models.CASCADE)
     name=models.TextField()
     profileimage=models.ImageField(upload_to='person_images/')
     profession=models.CharField(max_length=20)
     add_info = models.TextField()
     payment = models.IntegerField(default=0) 
     is_active = models.BooleanField(default=False)
     phone_number=models.CharField(max_length=12)
     email=models.EmailField(null=True,blank=True)
     website_link=models.URLField(null=True,blank=True)

     def __str__(self):
         return self.name
     def get_average_rating(self):
         total_reviews=ProfessionalPersonReview.objects.filter(ProfessionalPerson=self).count()
         if total_reviews==0:
             return 0
         total_ratings = ProfessionalPersonReview.objects.filter(ProfessionalPerson=self).aggregate(Sum('rating'))['rating__sum']
         average_rating = total_ratings / total_reviews
         return round(average_rating, 2)
     
     def get_total_reviews(self):
        return ProfessionalPersonReview.objects.filter(ProfessionalPerson=self).count()


     
     
class TimeSlot(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    professional = models.ForeignKey(ProfessionalPerson, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)


class Booking(models.Model):
    professional = models.ForeignKey(ProfessionalPerson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')])
    payment_amount = models.IntegerField(default=0)


class BookingNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notifications')
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='provider_notifications')
    professional = models.ForeignKey(ProfessionalPerson, on_delete=models.CASCADE)
    read_status = models.BooleanField(default=False)


class CareHomeReview(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_review')
    CareHome = models.ForeignKey(CareHome,on_delete=models.CASCADE,related_name='carehome_review')
    rating=models.IntegerField()
    review=models.CharField()
    add_time=models.DateTimeField(auto_now_add=True)
    is_block=models.BooleanField(default=False)

class ProfessionalPersonReview(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='userprofessional_review')
    ProfessionalPerson = models.ForeignKey(ProfessionalPerson,on_delete=models.CASCADE,related_name='ProfessionalPerson_review')
    rating=models.IntegerField()
    review=models.CharField()
    add_time=models.DateTimeField(auto_now_add=True)
    is_block=models.BooleanField(default=False)

            
    