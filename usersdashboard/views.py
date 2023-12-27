import json
import razorpay
from rest_framework.response import Response
from rest_framework import generics
from providerdashboard.models import CareHome,ProfessionalPerson
from providerdashboard.serializers import CareHomeSerializer,PersonSerializer
from .pagination import StandardResultsSetPagination
from providerdashboard.serializers import TimeSlotSerializer,BookingSerializer,BookingViewSerializer
from providerdashboard.models import TimeSlot,Booking
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status


# Create your views here.
class CareHomeListView(generics.ListAPIView):
    serializer_class = CareHomeSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset= CareHome.objects.filter(is_active=True)
        return queryset


class PersonsListView(generics.ListAPIView):
    serializer_class = PersonSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset= ProfessionalPerson.objects.filter(is_active=True)
        return queryset
    


class CareHomeSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CareHome.objects.all()
    serializer_class = CareHomeSerializer

class PersonSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProfessionalPerson.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]



class TimeSlotListAPIView(generics.ListAPIView):
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        professional_id = self.kwargs['professional_id']
        date = self.kwargs['date']
        return TimeSlot.objects.filter(professional__id=professional_id, date=date,is_booked=False)
    

class BookingCreateAPIView(generics.CreateAPIView):
   
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        professional_id = request.data.get('professional_id')
        user_id = request.data.get('user_id')
        date = request.data.get('date')
        time_slot_id = request.data.get('timeslot')
        payment_amount = request.data.get('payment_amount', 0)
        status=request.data.get('status')

        # Check if the time slot is available
        time_slot = TimeSlot.objects.get(id=time_slot_id)

        # Create a new booking
        booking_data = {
            'professional': professional_id,
            'user': user_id,
            'date': date,
            'timeslot': time_slot_id,
            'status': status,
            'payment_amount': payment_amount,
        }

        serializer = self.get_serializer(data=booking_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Mark the time slot as booked
        time_slot.is_booked = True
        time_slot.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
    
class UserBookingListView(generics.ListAPIView):
    serializer_class = BookingViewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the provider ID from the request data
        user_Id = self.request.query_params.get('user_id')

        # Assuming the logged-in user is a provider
        user_bookings = Booking.objects.filter(user_id=user_Id).order_by('-date', '-timeslot__start_time')
        return user_bookings
    

class UserBookingDestroyView(generics.RetrieveDestroyAPIView):
    queryset=Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]





class StartPaymentAPIView(APIView):
    def post(self,request,id):
        amount = request.data['fee']
        client = razorpay.Client(auth=("rzp_test_Fh0XmWHxDPIEAF", "Rl1rlAoJh3C8KC2T5wzZ6L5F"))

        payment = client.order.create({
        "amount": int(float(amount) * 100),  
        "currency": "INR",
        "payment_capture": "1"
         })
        try:
                data = {
                 "payment": payment,
             }
                print("startpayment dtaat:",data)
                return Response(data)
                
        except :
            return Response({'error': 'Professional with the provided ID does not exist'})

class HandlePaymentSuccessView(APIView):
    def post(self, request):
        try:
            response_data = json.loads(request.data["response"])
            print('haiiiiRijil',request.data)
            # Extract relevant data from the response
            razorpay_order_id = response_data.get('razorpay_order_id', '')
            razorpay_payment_id = response_data.get('razorpay_payment_id', '')
            razorpay_signature = response_data.get('razorpay_signature', '')
            time_slot_id =request.POST.get('timeslot')
            print('timeslotid:',time_slot_id)

            # Perform additional validations if needed
            professional_id = request.POST.get('professional_id')
            print('haiii',time_slot_id)
          
            # Create a new Booking instance
            booking_data = {
                'professional': professional_id,
                'user': request.POST.get('user_id', ''),
                'date': request.POST.get('date', ''),
                'timeslot': request.POST.get('timeslot', ''),
                'status': request.POST.get('status', ''),
                'payment_amount': request.POST.get('payment_amount', ''),
                # Add other fields as needed
            }


            print('booking_data',booking_data)
            time_slot = TimeSlot.objects.get(id=time_slot_id)

            booking_serializer = BookingSerializer(data=booking_data)
            if booking_serializer.is_valid():
                booking_serializer.save()
                 # Mark the time slot as booked
                   
                time_slot.is_booked = True
                time_slot.save()

                return Response({'message': 'Booking created successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Invalid booking data'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
