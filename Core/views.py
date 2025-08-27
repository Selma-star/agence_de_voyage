from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import HotelForm, PackageForm, BookingForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from django.http import JsonResponse
from .models import *
from .models import Client, PasswordReset, Hotel, Booking, Payments,HotelRooms, Cities, Destination,Package ,PackageImage, Flight, FlightClasses,PromoCode
from django.conf import settings
import uuid
from django.http import HttpResponseForbidden
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.contrib import messages
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET
from django.db.models import Min
from django.db.models import Sum
from django.db.models import Q
from django.db.models import OuterRef, Subquery, DecimalField
from django.db.models.functions import Cast
from django.db.models import Count
from django.db.models.functions import TruncDay,TruncMonth
from .models import Booking,Payments

#@login_required
def Home(request):
    return render(request, 'index.html')
@login_required
def profile_view(request):
    client = request.user  # This is your custom Client user model

    notifications = get_client_notifications(request)
    # Get all bookings by this client
    bookings = Booking.objects.filter(client=client)

    # Fetch all related payments and map them to booking IDs
    payments = Payments.objects.filter(booking__in=bookings)
    payments_dict = {payment.booking_id: payment for payment in payments}

    # Attach payment to each booking (optional, makes template simpler)
    for booking in bookings:
        booking.payment = payments_dict.get(booking.id)

    context = {
        'client': client,
        'bookings': bookings,
         "notifications": notifications,
        # optional if you need to use payments directly in the template
        'payments': payments_dict,
    }
    return render(request, 'profile.html', context)

@login_required
def update_profile(request):
    client = request.user

    if request.method == 'POST':
        client.full_name = request.POST.get('name')
        client.email = request.POST.get('email')
        client.phone = request.POST.get('phone')
        client.age = request.POST.get('age')

        if 'profile_image' in request.FILES:
            client.image = request.FILES['profile_image']

        client.save()
        return redirect('profile')  # or render with success message

    return render(request, 'profile.html', {'client': client})

#@login_required
#def profile_view(request):
    client = request.user  

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()

        errors = []

        if not full_name:
            errors.append('Full name cannot be empty.')

        if email and Client.objects.exclude(id=client.id).filter(email=email).exists():
            errors.append('This email is already in use.')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'profile.html', {'client': client})  

        
        client.full_name = full_name
        client.email = email
        client.phone = phone
        client.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')   

    return render(request, 'profile.html', {'client': client})

#def update_profile(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        city = request.POST.get("city")
        return JsonResponse({"message": f"Profile updated! Welcome, {username}."})
    
#def update_avatar(request):
    if request.method == "POST" and request.FILES.get("profile_pic"):
        return JsonResponse({"avatar_url": "/static/new-avatar.jpg"})  # Fake URL for now
    
def best_things_to_do(request):
    return render(request, 'indexdes6.html')

def best_time_to_visit(request):
    return render(request, 'indexdes5.html')

def best_dishes(request):
    return render(request, 'indexdes3.html')

def best_places(request):
    return render(request, 'indexdes4.html')


def destination_view(request):
    return render(request, 'destination.html')

def constantine_detail(request):
    return render(request, 'indexdes2.html')

def RegisterView(request): 
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone_number = request.POST.get("phone_number")

        user_data_has_error = False

        if Client.objects.filter(full_name=full_name).exists():
            user_data_has_error = True
            messages.error(request, "Name already exists")

        if Client.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, "Email already exists")

        if len(password) < 5:
            user_data_has_error = True
            messages.error(request, "Password must be at least 5 characters")

        if user_data_has_error:
            return redirect('register')

        # Create the new client
        new_client = Client.objects.create_user(
            email=email,
            password=password,
            full_name=full_name,
            phone=phone_number
        )
        setattr(new_client, 'backend', 'Core.authentication.EmailBackend')
        login(request, new_client)
        messages.success(request, "Account created.")
        return redirect('home')

    return render(request, 'register.html')

def LoginView(request): 
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        client = authenticate(request, email=email, password=password)  # Authenticate client

        if client is not None:
            login(request, client)  # Log the client in
            request.session['client_id'] = client.id  
            request.session['client_name'] = client.full_name
            messages.success(request, f"Welcome, {client.full_name}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')

def ForgotPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            client = Client.objects.get(email=email)

            # Create a password reset entry for the client
            new_password_reset = PasswordReset(client=client)
            new_password_reset.save()

            # Generate password reset URL
            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})
            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

            # Email content
            email_body = f'Reset your password using the link below:\n\n{full_password_reset_url}'
        
            email_message = EmailMessage(
                'Reset your password',  # Subject
                email_body,
                settings.EMAIL_HOST_USER,  # Sender
                [email]  # Receiver
            )

            email_message.fail_silently = True
            email_message.send()

            messages.success(request, "Password reset link sent to your email.")
            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)

        except Client.DoesNotExist:
            messages.error(request, f"No client with email '{email}' found")
            return redirect('forgot-password')

    return render(request, 'forgot_password.html')

def PasswordResetSent(request, reset_id):
    # Check if reset_id exists in PasswordReset table
    password_reset_entry = get_object_or_404(PasswordReset, reset_id=reset_id)

    return render(request, 'password_reset_sent.html')

def ResetPassword(request, reset_id):
    password_reset_entry = get_object_or_404(PasswordReset, reset_id=reset_id)

    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        errors = []

        if password != confirm_password:
            errors.append('Passwords do not match')

        if len(password) < 5:
            errors.append('Password must be at least 5 characters long')

        expiration_time = password_reset_entry.created_when + timezone.timedelta(minutes=10)

        if timezone.now() > expiration_time:
            errors.append('Reset link has expired')
            password_reset_entry.delete()

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'reset_password.html', {'reset_id': reset_id})

        # Update password
        user = password_reset_entry.user
        user.set_password(password)
        user.save()

        password_reset_entry.delete()  # Delete reset entry after successful password change

        messages.success(request, 'Password reset successfully. Proceed to login')
        return redirect('login')

    return render(request, 'reset_password.html', {'reset_id': reset_id})

def hotel_view(request):
    return render(request, 'hotel.html')

def Package_view(request):
    return render(request, 'PackageHome.html')


def hotel_list_view(request):
    # Subquery to fetch the "Single Room" price
    single_room_price = HotelRooms.objects.filter(
        hotel=OuterRef('pk'),
        room_type__iexact="Single"  # case-insensitive match
    ).values('price_per_night')[:1]

    # Cast the price to match the DecimalField type for compatibility
    single_room_price = Subquery(single_room_price, output_field=DecimalField())

    # Apply to each hotel queryset
    luxe_hotels = Hotel.objects.filter(type='LUXE').annotate(
        min_price=single_room_price
    ).order_by('-rating')

    family_hotels = Hotel.objects.filter(type='FAMILIALE').annotate(
        min_price=single_room_price
    ).order_by('-rating')

    popular_hotels = Hotel.objects.filter(type='POPULAIRE').annotate(
        min_price=single_room_price
    ).order_by('-rating')

    context = {
        "luxe_hotels": luxe_hotels,
        "family_hotels": family_hotels,
        "popular_hotels": popular_hotels,
    }

    return render(request, 'hotel.html', context)



def hotel_detail_view(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)  # Fetch the hotel by ID
    context = {"hotel": hotel}
    return render(request, 'hotel_details.html', context)


def hotel_list_all(request):
    """ Fetch all hotels without filtering """
    hotels = Hotel.objects.all()
    return render(request, 'hotel.html', {'hotels': hotels})


#@login_required
#def submit_booking(request, hotel_id):
    if request.method == 'POST':
        client = request. user 

        hotel_id = request.POST.get('hotel_id')
        hotel = Hotel.objects.get(id=hotel_id)
        city = hotel.city
        
        
        # Retrieve form data
        check_in_date_str = request.POST.get('check_in_date')
        nights = int(request.POST.get('nights'))

        # Convert check-in string to datetime
        check_in_date = datetime.strptime(check_in_date_str, '%Y-%m-%d').date()

        # Calculate check-out
        check_out_date = check_in_date + timedelta(nights)

        
        # Create booking
        booking_code = str(uuid.uuid4())[:8].upper()
        
        booking = Booking.objects.create(
            booking_code=booking_code,
            client=client,
            hotel=hotel,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            number_of_nights=nights,
            status='pending',
            flight=None,
            package=None,
            package_type='hotel-only',
            city=city 
        )
        
        # Create payment (example)
        Payments.objects.create(
            booking=booking,
            amount=request.POST.get('amount'),
            currency='DZD',
            payment_method=request.POST.get('payment_method'),
            transaction_id=f"TX-{uuid.uuid4().hex[:10].upper()}",
            status='completed'
        )

        messages.success(request, "Booking was successful!")
        return render(request, 'hotel_details.html', {'hotel': hotel})  # Adjust as necessary

    return redirect('home')  # Redirect to home if not a POST request

@login_required
def submit_booking_unified(request, booking_type, item_id):
    if request.method == 'POST':
        client = request.user

        # Get shared data
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        coupon_code = request.POST.get('coupon_summary')  # Optional
        nights = int(request.POST.get('nights', 1))
        check_in_date_str = request.POST.get('check_in_date', None)

        if check_in_date_str:
            check_in_date = datetime.strptime(check_in_date_str, '%Y-%m-%d').date()
        else:
            check_in_date = datetime.now().date()
        check_out_date = check_in_date + timedelta(days=nights)

        # Initialize defaults
        hotel = None
        flight = None
        package = None
        package_type = 'hotel-only'
        city = None

        # Handle each booking type
        if booking_type == 'hotel':
            hotel = get_object_or_404(Hotel, id=item_id)
            city = hotel.city
            package_type = 'hotel-only'

        elif booking_type == 'flight':
            flight = get_object_or_404(Flight, id=item_id)
            city = flight.arrival_city
            package_type = 'flight-only'
            nights = 1  # Default for flights if no hotel

        elif booking_type == 'package':
            package = get_object_or_404(Package, id=item_id)
            hotel = package.hotel
            flight = package.flight
            city = package.city
            package_type = 'full-package'
            nights = package.duration
            check_in_date = package.check_in_date or datetime.now().date()
            check_out_date = package.check_out_date or (check_in_date + timedelta(days=nights))

        else:
            messages.error(request, "Invalid booking type.")
            return redirect('home')

        # Create booking
        booking_code = str(uuid.uuid4())[:8].upper()
        booking = Booking.objects.create(
            booking_code=booking_code,
            client=client,
            hotel=hotel,
            flight=flight,
            package=package,
            package_type=package_type,
            city=city,
            status='pending',
            number_of_nights=nights,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
        )

        # Create payment
        Payments.objects.create(
            booking=booking,
            amount=amount,
            currency='DZD',
            payment_method=payment_method,
            transaction_id=f"TX-{uuid.uuid4().hex[:10].upper()}",
            status='completed'
        )

        messages.success(request, "Booking was successful!")
        
        # Redirect based on type
        if booking_type == 'hotel':
            return redirect('hotel_det', hotel.id)
        elif booking_type == 'flight':
            return redirect('flightfiltre')
        else:
            return redirect('package_det', package.id)

    return redirect('home')


#==================MARIA PART========================================================#
def hotelfiltre(request):
    country = request.GET.get('country')
    city = request.GET.get('city')
    people = int(request.GET.get('people', 1))  
    departure = request.GET.get('departure')
    return_date = request.GET.get('return')

    # Perform search logic here, e.g., filter hotels based on the provided criteria

    hotels = Hotel.objects.all()

    if city:
        hotels = hotels.filter(city__name__icontains=city)
    if country:
        hotels = hotels.filter(city__destination__name__icontains=country)
    hotels = hotels.annotate(min_price=Min('hotelrooms__price_per_night'))
    # Calculate nights
    nights = None
    checkin = checkout = None
    try:
        checkin = datetime.strptime(departure, '%Y-%m-%d').date()
        checkout = datetime.strptime(return_date, '%Y-%m-%d').date()
        nights = (checkout - checkin).days
    except (TypeError, ValueError):
        pass  # If date is missing or invalid, skip calculation

    context = {
        'hotels': hotels,
        'nights': nights,
        'checkin': checkin,
        'checkout': checkout
    }
    return render(request, 'HotelFilter.html', context)

  
def get_countries(request):
    countries = Destination.objects.values('id', 'name').distinct()
    return JsonResponse(list(countries), safe=False)

def get_cities(request):
    query = request.GET.get('country', None)
    if query:
        cities = Cities.objects.filter(destination__name__icontains=query).values('id', 'name')
    else:
        cities = Cities.objects.all().values('id', 'name')
    return JsonResponse(list(cities), safe=False)




def hotel_id_cards_view(request):

    hotels = Hotel.objects.annotate(min_price=Min('hotelrooms__price_per_night'))

    #  1. Scope by original city & country
    country = request.GET.get('country')
    city = request.GET.get('city')

    if city:
        hotels = hotels.filter(city__name__icontains=city)
    if country:
        hotels = hotels.filter(city__destination__name__icontains=country)

    #  2. Hotel type filter (LUXE, etc.)
    hotel_type = request.GET.get('type')
    print('Hotel Type:', hotel_type)
    if hotel_type:
        hotels = hotels.filter(type=hotel_type)

    #  3. Rating
    rating = request.GET.get('rating')
    if rating:
        try:
            rating_value = int(rating)
            hotels = hotels.filter(rating__gte=rating_value, rating__lt=rating_value + 1)
        except ValueError:
            pass  # Invalid rating value? Ignore filter.

    #  4. Room type
    room_type = request.GET.get('room_type')
    if room_type:
        hotels = hotels.filter(hotelrooms__room_type=room_type).distinct()

    #  5. Price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        hotels = hotels.filter(
            hotelrooms__price_per_night__gte=float(min_price),
            hotelrooms__price_per_night__lte=float(max_price)
        ).distinct()

    #  6. Services
    selected_services = request.GET.getlist('facilities')
    if selected_services:  
      for service in selected_services:
         hotels = hotels.filter(hotelservice__service__service_name=service)
      hotels = hotels.distinct()   
    return render(request, 'partials/hotel_cards.html', {'hotels': hotels})


def validate_coupon(request):
    code = request.GET.get('code', '').strip()
    try:
        promo = PromoCode.objects.get(code=code)
        if promo.is_valid():
            return JsonResponse({'valid': True, 'discount': promo.discount_percent})
        else:
            return JsonResponse({'valid': False, 'message': 'Code expiré'})
    except PromoCode.DoesNotExist:
        return JsonResponse({'valid': False, 'message': 'Code invalide'})
    

def get_client_notifications(request):
    notifications = []

    if request.user.is_authenticated:
        client = request.user

        # ✅ Total Spent by This Client
        total_spent = Payments.objects.filter(
            booking__client=client,
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0

        # ✅ Determine Loyalty Level
        loyalty_level = None
        if total_spent >= 5000:
            loyalty_level = 'platinum'
        elif total_spent >= 3000:
            loyalty_level = 'gold'
        elif total_spent >= 1500:
            loyalty_level = 'silver'
        elif total_spent >= 500:
            loyalty_level = 'bronze'

        # ✅ Get Valid Promo Codes for "all" or loyalty level
        valid_promos = PromoCode.objects.filter(
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now(),
            is_active=True
        )

        # ✅ Public promo codes
        for promo in valid_promos:
            if promo.loyalty_level == 'all':
                notifications.append({
                    "type": "promo",
                    "message": f"🎉 Public Promo Code: {promo.code} - {promo.discount_percent}% OFF!"
                })

        # ✅ Loyalty promo code (only one shown)
        if loyalty_level:
            loyalty_promo = valid_promos.filter(loyalty_level=loyalty_level).first()
            if loyalty_promo:
                loyalty_msg = f"🌟 You're now a **{loyalty_level.title()} Client**! Use promo code **{loyalty_promo.code}** to get {loyalty_promo.discount_percent}% OFF your next booking!"
                notifications.append({
                    "type": "loyalty",
                    "message": loyalty_msg
                })

    return notifications



#-----------------------------------------------------------------------------------------------------
#------------------------ PACKAGES  ---------------------------------------------------------------------



def package_page(request):
    packages = Package.objects.all()  # or you can filter, order, etc
    return render(request, 'packages.html', {'packages': packages})

def package_det(request, pk):
    package = Package.objects.get(pk=pk)
    package_days = PackageImage.objects.filter(package=package)
    
    context = {
        "package": package,
        "package_days": package_days,
    }
    return render(request, 'PackageDetails.html', context)

def packagefiltre(request):
    from_country = request.GET.get('from_country')
    to_country = request.GET.get('to_country')
    people = int(request.GET.get('people', 1))
    departure = request.GET.get('departure')
    return_date = request.GET.get('return')

    packages = Package.objects.all()

    #if from_country:
        #packages = packages.filter(city__destination__name__icontains=from_country)
    if to_country:
        packages = packages.filter(city__destination__name__icontains=to_country)

    # packages = packages.annotate(min_price=Min('package_options__price'))  # adapt field names if needed

    # Get related cities for that to_country
    cities = Cities.objects.filter(destination__name__icontains=to_country)

    # Calculate trip duration
    duration_days = None
    checkin = checkout = None
    try:
        checkin = datetime.strptime(departure, '%Y-%m-%d').date()
        checkout = datetime.strptime(return_date, '%Y-%m-%d').date()
        duration_days = (checkout - checkin).days
    except (TypeError, ValueError):
        pass

    context = {
    'packages': packages,
    'duration_days': duration_days,
    'checkin': checkin,
    'checkout': checkout,
    'from_country': from_country,
    'to_country': to_country,
    'people': people,
    'cities': cities, 
}
    return render(request, 'PackageID.html', context)


def package_id_cards_view(request):
    packages = Package.objects.all()

    # 1. Filter by To Country (Destination)
    to_country = request.GET.get('to_country')
    if to_country:
        packages = packages.filter(city__destination__name__icontains=to_country)

    # 2. Filter by City
    city = request.GET.get('city')
    if city:
        packages = packages.filter(city__name__icontains=city)

    # 3. Filter by Rating
    rating = request.GET.get('rating')
    if rating:
        try:
            rating_val = int(rating)
            packages = packages.filter(rating__gte=rating_val, rating__lt=rating_val + 1)
        except ValueError:
            pass

    # 4. Filter by Duration
    duration_filter = request.GET.get('duration')
    if duration_filter:
      if duration_filter == 'more':
         packages = packages.filter(duration__gt=7)
      else:
        try:
            days = int(duration_filter)
            packages = packages.filter(duration=days)
        except ValueError:
            pass

    # 5. Filter by Price Range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        try:
            packages = packages.filter(
                price__gte=float(min_price),
                price__lte=float(max_price)
            )
        except ValueError:
            pass

    context = {
        'packages': packages
    }
    return render(request, 'partials/package_cards.html', context)

#-----------------------------------------------------------------------------------------------------
#------------------------ FLIGHTS  ---------------------------------------------------------------------
def Flight_view(request):
    return render(request, 'Flight.html')

def format_duration(duration):
    hours, remainder = divmod(duration.total_seconds(), 3600)
    minutes = remainder // 60
    return f"{int(hours)}h {int(minutes)}m"

#def flight_list(request):
    flights = Flight.objects.all().select_related('departure_city', 'arrival_city')

    for flight in flights:
        flight.formatted_duration = format_duration(flight.duration)

    return render(request, 'FlightsList.html', {
        'flights': flights
    })

def flightfiltre(request):
    from_city = request.GET.get('from_city')
    to_city = request.GET.get('to_city')
    departure = request.GET.get('departure')
    return_date = request.GET.get('return')
    people = int(request.GET.get('people', 1))

    flights = Flight.objects.all().select_related('departure_city', 'arrival_city')

    if from_city:
        flights = flights.filter(departure_city__name__icontains=from_city)
    if to_city:
        flights = flights.filter(arrival_city__name__icontains=to_city)

    if departure:
        try:
            dep_date = datetime.strptime(departure, "%Y-%m-%d").date()
            flights = flights.filter(departure_time__date__gte=dep_date)
        except ValueError:
            pass

    if return_date:
        try:
            ret_date = datetime.strptime(return_date, "%Y-%m-%d").date()
            flights = flights.filter(arrival_time__date__lte=ret_date)
        except ValueError:
           pass

    # Only flights with enough seats
    flights = flights.filter(available_seats__gte=people)

    for flight in flights:
        flight.formatted_duration = format_duration(flight.duration)

    context = {
        'flights': flights,
        'from_city': from_city,
        'to_city': to_city,
        'departure': departure,
        'return': return_date,
        'people': people
    }
    return render(request, 'FlightsList.html', context)

def flight_id_cards_view(request):
    flights = Flight.objects.all()

    to_city = request.GET.get('to_city')
    from_city = request.GET.get('from_city')
    if from_city:
        flights = flights.filter(departure_city__name__icontains=from_city)
    if to_city:
        flights = flights.filter(arrival_city__name__icontains=to_city)
    departure = request.GET.get('departure')
    return_date = request.GET.get('return')
    if departure:
        try:
            dep_date = datetime.strptime(departure, "%Y-%m-%d")
            flights = flights.filter(departure_time__date__gte=dep_date)
        except ValueError:
            pass

    if return_date:
        try:
            ret_date = datetime.strptime(return_date, "%Y-%m-%d")
            flights = flights.filter(arrival_time__date__lte=ret_date.date())
        except ValueError:
            pass

            
    # Price filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        try:
            flights = flights.filter(
                price__gte=float(min_price),
                price__lte=float(max_price)
            )
        except ValueError:
            pass

    # Travel class filter
    flight_class = request.GET.get('class')
    print('Flight Class:', flight_class)
    if flight_class:
        flights = flights.filter(flightclasses__class_type=flight_class).distinct()

    # Airline company filter
    airline_companies = request.GET.getlist("airline_company[]")
    if airline_companies:
        flights = flights.filter(airline_company__in=airline_companies)

    # Stops filter
    stops = request.GET.get("stops")
    print("Selected Stops:", stops)
    if stops is not None:
        try:
            stops = int(stops)
            if stops == 2:
                flights = flights.filter(stops__gte=2)
            else:
                flights = flights.filter(stops=stops)
        except ValueError:
         pass

    context = {
        'flights': flights
    }
    return render(request, 'partials/flight_cards.html', context)
  


#tHE CLIENT cHART
def client_chart_data(request):
    # Group clients by the month they were created
    qs = (
        Client.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # Format for JSON: ['Jan', 'Feb', ...], and [12, 8, ...]
    categories = [entry['month'].strftime('%b') for entry in qs]
    data       = [entry['count'] for entry in qs]

    return JsonResponse({
        'categories': categories,
        'data':       data,
    })


#tHE CHART
def chart_data(request):
    # Group bookings by day of 'booked_at'
    qs = (
        Booking.objects
        .annotate(day=TruncDay('booked_at'))
        .values('day')
        .annotate(
            flight_only = Count('id', filter=Q(package_type='flight-only')),
            hotel_only  = Count('id', filter=Q(package_type='hotel-only')),
            full_package= Count('id', filter=Q(package_type='full-package')),
        )
        .order_by('day')
    )

    # Format X-axis labels as “YYYY-MM-DD”
    categories    = [entry['day'].strftime('%Y-%m-%d') for entry in qs]
    flight_only   = [entry['flight_only']   for entry in qs]
    hotel_only    = [entry['hotel_only']    for entry in qs]
    full_package  = [entry['full_package']  for entry in qs]

    return JsonResponse({
        'categories':    categories,
        'flight_only':   flight_only,
        'hotel_only':    hotel_only,
        'full_package':  full_package,
    })
# Admin Section

def index(request):

    clients_count = Client.objects.count()
    cities_count =  Cities.objects.count()# Static or dynamically count if stored in DB
    bookings_count = Booking.objects.count()
    total_revenue = Payments.objects.filter(status="completed").aggregate(total=Sum("amount"))["total"] or 0

    star_clients = (
        Client.objects
        .annotate(
            total_spending=Sum(
                'booking__payments__amount',
                filter=Q(booking__payments__status='completed')
            )
        )
        .filter(total_spending__isnull=False)
        .order_by('-total_spending')[:5]
    )

    latest_bookings = Booking.objects.select_related('client', 'flight', 'hotel', 'package').order_by('-booked_at')[:5]

    latest_activities = []
    for booking in latest_bookings:
        item = None
        if booking.package and booking.package.name:
            item = f'Package "{booking.package.name}"'
        elif booking.flight and booking.flight.airline_company:
            item = f'Flight "{booking.flight.airline_company}"'
        elif booking.hotel and booking.hotel.name:
            item = f'Hotel "{booking.hotel.name}"'
        else:
            item = 'an unknown trip'

        latest_activities.append({
            "date": booking.booked_at.strftime("%b %d"),
            "text": f'{booking.client.full_name} booked {item}'
        })

    return render(request, "Home/index_admin.html", {
       "clients_count": clients_count,
        "cities_count": cities_count,
        "bookings_count": bookings_count,
        "total_revenue": total_revenue,
        "star_clients": star_clients,
        "latest_activities": latest_activities
    })
def profile(request):
    return render(request, "Profile/profile_admin.html")

#flights 

def add_flight(request):
    if request.method == "POST":
        departure_city_id = request.POST.get("departure_city")
        arrival_city_id = request.POST.get("arrival_city")
        departure_time = request.POST.get("departure_time")
        arrival_time = request.POST.get("arrival_time")
        price = request.POST.get("price")
        duration = request.POST.get("duration")  # should be in HH:MM:SS format
        available_seats = request.POST.get("available_seats")
        airline_company = request.POST.get("airline_company")
        plane_model = request.POST.get("plane_model")
        status = request.POST.get("status")
        image = request.FILES.get("image")  # for file upload

        # Create flight
        flight = Flight.objects.create(
            departure_city=Cities.objects.get(id=departure_city_id),
            arrival_city=Cities.objects.get(id=arrival_city_id),
            departure_time=departure_time,
            arrival_time=arrival_time,
            price=price,
            duration=duration,
            available_seats=available_seats,
            airline_company=airline_company,
            plane_model=plane_model,
            status=status,
            image=image
        )

        messages.success(request, "Flight added successfully")
        return redirect("flight_list")

    cities = Cities.objects.all()
    return render(request, "Flights/add-flight.html", {"cities": cities})


def edit_flight(request, id):
    flight = get_object_or_404(Flight, id=id)

    if request.method == "POST":
        departure_city_id = request.POST.get("departure_city")
        arrival_city_id = request.POST.get("arrival_city")
        departure_time = request.POST.get("departure_time")
        arrival_time = request.POST.get("arrival_time")
        price = request.POST.get("price")
        duration = request.POST.get("duration")
        available_seats = request.POST.get("available_seats")
        airline_company = request.POST.get("airline_company")
        plane_model = request.POST.get("plane_model")
        status = request.POST.get("status")
        image = request.FILES.get("image")  # optional

        # Update flight fields
        flight.departure_city = Cities.objects.get(id=departure_city_id)
        flight.arrival_city = Cities.objects.get(id=arrival_city_id)
        flight.departure_time = departure_time
        flight.arrival_time = arrival_time
        flight.price = price
        flight.duration = duration
        flight.available_seats = available_seats
        flight.airline_company = airline_company
        flight.plane_model = plane_model
        flight.status = status
        if image:
            flight.image = image

        flight.save()
        return redirect("flight_list")

    cities = Cities.objects.all()
    return render(request, "Flights/edit-flight.html", {
        "flight": flight,
        "cities": cities
    })

def flight_list(request):
    flight_list = Flight.objects.all()
    context = {
        'flight_list': flight_list
    }
    return render(request, "Flights/flights.html", context)

def delete_flight(request, id):
    if request.method == 'POST':
        flight = get_object_or_404(Flight, id=id)
        flight_name = f"Flight {flight.airline_company}"  # Show airline company or another attribute
        flight.delete()
        return redirect("flight_list")
    return HttpResponseForbidden()



#hotels

def add_hotel(request):
    if request.method == "POST":
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Hotel added successfully")
            return redirect("hotel_list")
    else:
        form = HotelForm()

    cities = Cities.objects.all()  # Fetch all cities
    return render(request, "Hotels/add-hotel.html", {"form": form, "cities": cities})

def hotel_list(request):
    hotel_list = Hotel.objects.all()
    context = {
        'hotel_list': hotel_list  
    }
    return render(request, "Hotels/hotels.html", context)

def edit_hotel(request, id):
    hotel = get_object_or_404(Hotel, id=id)
    if request.method == "POST":
        form = HotelForm(request.POST, request.FILES, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect("hotel_list")
    else:
        form = HotelForm(instance=hotel)
    
    cities = Cities.objects.all()  # Fetch all cities
    return render(request, "Hotels/edit-hotel.html", {"form": form, "hotel": hotel, "cities": cities})

def delete_hotel(request, id):
    if request.method == 'POST':
        hotel = get_object_or_404(Hotel, id=id)
        hotel_name = f"Hotel {hotel.name}"
        hotel.delete()
        return redirect("hotel_list")  
    return HttpResponseForbidden()

def hotel_details(request, id):
   
    hotel = get_object_or_404(Hotel, id=id)
    

    return render(request, 'Hotels/hotel-details.html', {'hotel': hotel})

#PACKAGES
def package_list(request):
    # Query all packages
    package_list = Package.objects.all()

    # Pass the package list to the context
    context = {
        'package_list': package_list
    }

    return render(request, "Packages/packages.html", context)
# Package details
def package_details(request, id):
    package = get_object_or_404(Package, id=id)
    return render(request, 'Packages/package-details.html', {'package': package})
# Add package
def add_package(request):
    flights = Flight.objects.all()
    hotels = Hotel.objects.all()
    activities = Activities.objects.all()

    if request.method == 'POST':
        flight_id = request.POST.get('flight')
        hotel_id = request.POST.get('hotel')
        activity_id = request.POST.get('activity')

        if not flight_id or not hotel_id or not activity_id:
            return render(request, 'Packages\add-package.html', {
                'flights': flights,
                'hotels': hotels,
                'activities': activities,
                'error': 'All fields (flight, hotel, and activity) are required!'
            })

        try:
            flight = Flight.objects.get(id=flight_id)
            hotel = Hotel.objects.get(id=hotel_id)
            activity = Activities.objects.get(id=activity_id)
        except (Flight.DoesNotExist, Hotel.DoesNotExist, Activities.DoesNotExist):
            return render(request, 'Packages/add-package.html', {
                'flights': flights,
                'hotels': hotels,
                'activities': activities,
                'error': 'Invalid flight, hotel, or activity ID.'
            })

        # Convert comma-separated string to a list (for array fields)
        included_features = request.POST.get('included_features', '').split(',')
        

        # Create the package object
        package = Package.objects.create(
            name=request.POST['name'],
            price=request.POST['price'],
            flight=flight,
            hotel=hotel,
            activity=activity,
            description=request.POST['description'],
            duration=request.POST['duration'],
            max_people=request.POST['max_people'],
            # Convert list to proper format for the database
            included_features=included_features,
            transportation_details=request.POST['transportation_details']
        )

        return redirect('package_list')

    return render(request, 'Packages/add-package.html', {'flights': flights, 'hotels': hotels, 'activities': activities})
# Edit package
def edit_package(request, id):
    package = get_object_or_404(Package, id=id)
    if request.method == 'POST':
        form = PackageForm(request.POST, instance=package)
        if form.is_valid():
            form.save()
            return redirect('package_list')
    else:
        form = PackageForm(instance=package)
    return render(request, 'Packages/edit-package.html', {'form': form, 'package': package})
# Delete package
def delete_package(request, id):
    if request.method == 'POST':
        package = get_object_or_404(Package, id=id)
        package_name = f"Package {package.name}"
        package.delete()
        return redirect("package_list")
    return HttpResponseForbidden()

# CLIENT
def add_client(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        password = request.POST.get("password")
        image = request.FILES.get("image")

        # Create client
        client = Client.objects.create_user(
            full_name=full_name,
            email=email,
            password=password,
        )
        client.phone = phone
        client.age = age
        client.gender = gender
        client.image = image
        client.save()

        messages.success(request, "Client added successfully")
        return redirect("client_list")

    return render(request,"Clients/add-client.html")

def client_list(request):
    # Query all clients
    client_list = Client.objects.all()

    # Pass the client list to the context
    context = {
        'client_list': client_list
    }

    return render(request, "Clients/clients.html",context)

def edit_client(request, id):
    client = get_object_or_404(Client, id=id)

    if request.method == "POST":
        client.full_name = request.POST.get("full_name")
        client.email = request.POST.get("email")
        client.phone = request.POST.get("phone")
        client.age = request.POST.get("age")
        client.gender = request.POST.get("gender")

        image = request.FILES.get("image")
        if image:
            client.image = image

        client.save()
        messages.success(request, "Client updated successfully")
        return redirect("client_list")

    return render(request, "Clients/edit-client.html", {
        "client": client
    })

def client_details(request, id):
    client = get_object_or_404(Client, id=id)

    return render(request, 'Clients/client-details.html', {'client': client})

def delete_client(request, id):
    if request.method == 'POST':
        client = get_object_or_404(Client, id=id)
        client_name = f"Client {client.full_name}"
        client.delete()
        return redirect("client_list")  # Update this with the URL name for the client list view
    return HttpResponseForbidden()

#agent 

def add_agent(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        insurance_number = request.POST.get("insurance_number")
        role = request.POST.get("role")
        password = request.POST.get("password")
        image = request.FILES.get("image")

        is_active = request.POST.get("is_active") == "on"
        is_staff = request.POST.get("is_staff") == "on"
        is_superuser = request.POST.get("is_superuser") == "on"

        # Create agent user
        agent = Agent.objects.create_user(
            full_name=full_name,
            email=email,
            password=password,
        )

        # Set additional fields
        agent.phone = phone
        agent.insurance_number = insurance_number
        agent.role = role
        agent.is_active = is_active
        agent.is_staff = is_staff
        agent.is_superuser = is_superuser
        if image:
            agent.image = image
        agent.save()

        # Handle groups
        group_ids = request.POST.getlist("groups")
        agent.groups.set(group_ids)

        # Handle permissions
        permission_ids = request.POST.getlist("permissions")
        agent.user_permissions.set(permission_ids)

        messages.success(request, "Agent added successfully.")
        return redirect("agent_list")

    all_groups = Group.objects.all()
    all_permissions = Permission.objects.all()

    return render(request, "Agents/add-agent.html", {
        "all_groups": all_groups,
        "all_permissions": all_permissions
    })

def edit_agent(request, id):
    agent = get_object_or_404(Agent, id=id)

    if request.method == "POST":
        agent.full_name = request.POST.get("full_name")
        agent.email = request.POST.get("email")
        agent.phone = request.POST.get("phone")
        agent.insurance_number = request.POST.get("insurance_number")
        agent.role = request.POST.get("role")
        agent.is_active = request.POST.get("is_active") == "on"
        agent.is_staff = request.POST.get("is_staff") == "on"
        agent.is_superuser = request.POST.get("is_superuser") == "on"

        image = request.FILES.get("image")
        if image:
            agent.image = image

        agent.save()

        # Handle groups
        selected_group_ids = request.POST.getlist("groups")
        agent.groups.set(selected_group_ids)

        # Handle permissions
        selected_permission_ids = request.POST.getlist("permissions")
        agent.user_permissions.set(selected_permission_ids)

        messages.success(request, "Agent updated successfully.")
        return redirect("agent_list")

    all_groups = Group.objects.all()
    all_permissions = Permission.objects.all()

    return render(request, "Agents/edit-agent.html", {
        "agent": agent,
        "all_groups": all_groups,
        "all_permissions": all_permissions,
    })

def agent_list(request):
    agents = Agent.objects.all()  # Fetch all agents
    return render(request, 'Agents/agents.html', {'agents': agents})

def agent_details(request, id):
    agent = get_object_or_404(Agent, id=id)
    return render(request, 'Agents/agent-details.html', {'agent': agent})

def delete_agent(request, id):
    agent = get_object_or_404(Agent, id=id)
    
    # Optionally, check if the agent is active before deletion
    if agent.is_active:
        agent.delete()
        messages.success(request, "Agent deleted successfully")
    else:
        messages.error(request, "Cannot delete an inactive agent")
    
    return redirect("agent_list")

#booking

def add_booking(request):
    if request.method == 'POST':
        # Initialize the form with POST data
        form = BookingForm(request.POST)
        if form.is_valid():
            # Save the new booking
            form.save()
            return redirect('booking_list')  # Redirect to the list of bookings or a success page
    else:
        # Initialize an empty form for GET request
        form = BookingForm()

    # Pass all necessary models for selecting data
    context = {
        'form': form,
        'clients': Client.objects.all(),  # All clients
        'cities': Cities.objects.all(),  # All cities
        'flights': Flight.objects.all(),  # All flights
        'hotels': Hotel.objects.all(),  # All hotels
        'packages': Package.objects.all(),  # All packages
    }

    return render(request, 'Bookings/add-booking.html', context)

def edit_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    
    # Get necessary data for selection fields
    clients = Client.objects.all()
    packages = Package.objects.all()
    flights = Flight.objects.all()  # Include flights
    hotels = Hotel.objects.all()  
    cities = Cities.objects.all() 

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('booking_list')  # Redirect after successful update
    else:
        form = BookingForm(instance=booking)

    return render(request, 'Bookings/edit-booking.html', {
        'form': form,
        'booking': booking,
        'clients': clients,
        'cities': cities,
        'packages': packages,
        'flights': flights,  # Pass flights to the template
        'hotels': hotels     # Pass hotels to the template
    })

def booking_list(request):
    bookings = Booking.objects.all()  # Fetch all bookings from the database
    return render(request, 'Bookings/bookings.html', {'bookings': bookings})

# View booking details
def booking_details(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)  # Fetch the booking by ID
    return render(request, 'Bookings/booking-details.html', {'booking': booking})

# Delete a booking
def delete_booking(request, id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=id)  # Get the booking object to delete
        booking_code = f"Booking {booking.booking_code}"  # The booking code for reference
        booking.delete()  # Delete the booking
        return redirect("booking_list")  # Redirect to the bookings list page
    return HttpResponseForbidden()  # Return Forbidden if it's not a POST reques




#cities 

def add_city(request):
    if request.method == "POST":
        name = request.POST.get("name")
        destination_id = request.POST.get("destination")
        timezone = request.POST.get("timezone")
        airport_code = request.POST.get("airport_code")
        image = request.FILES.get("image")

        destination = Destination.objects.get(id=destination_id)

        Cities.objects.create(
            name=name,
            destination=destination,
            timezone=timezone,
            airport_code=airport_code,
            image=image
        )

        messages.success(request, "City added successfully")
        return redirect("city_list")

    destinations = Destination.objects.all()
    return render(request, "Cities/add-city.html", {"destinations": destinations})
 
 
 # Fin

def edit_city(request, id):
    city = get_object_or_404(Cities, id=id)

    if request.method == "POST":
        name = request.POST.get("name")
        destination_id = request.POST.get("destination")
        timezone = request.POST.get("timezone")
        airport_code = request.POST.get("airport_code")
        image = request.FILES.get("image")

        city.name = name
        city.destination = Destination.objects.get(id=destination_id)
        city.timezone = timezone
        city.airport_code = airport_code
        if image:
            city.image = image

        city.save()
        messages.success(request, "City updated successfully")
        return redirect("city_list")

    destinations = Destination.objects.all()
    return render(request, "Cities/edit-city.html", {
        "city": city,
        "destinations": destinations
    })

def city_list(request):
    cities = Cities.objects.select_related("destination").all()
    return render(request, "Cities/cities.html", {"cities": cities})

def delete_city(request, id):
    if request.method == "POST":
        city = get_object_or_404(Cities, id=id)
        city.delete()
        messages.success(request, "City deleted successfully")
        return redirect("city_list")
    return HttpResponseForbidden()


# 1. List all activities
def activity_list(request):
    activities = Activities.objects.all()
    return render(request, 'Activities/activities.html', {'activities': activities})

# 2. Add new activity

def add_activity(request):
    cities = Cities.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        city_id = request.POST['city']
        activity_type = request.POST.get('activity_type')
        description = request.POST.get('description')
        price = request.POST.get('price')
        opening_hours = request.POST.get('opening_hours')
        website_url = request.POST.get('website_url')
        rating = request.POST.get('rating')

        Activities.objects.create(
            name=name,
            city=Cities.objects.get(id=city_id),
            activity_type=activity_type,
            description=description,
            price=price if price else None,
            opening_hours=opening_hours,
            website_url=website_url,
            rating=rating if rating else None,
        )
        return redirect('activity_list')

    return render(request, 'Activities/add-activity.html', {'cities': cities})

# 3. Edit an activity
def edit_activity(request, id):
    activity = get_object_or_404(Activities, id=id)
    cities = Cities.objects.all()

    if request.method == 'POST':
        activity.name = request.POST['name']
        activity.city = Cities.objects.get(id=request.POST['city'])
        activity.activity_type = request.POST.get('activity_type')
        activity.description = request.POST.get('description')
        activity.price = request.POST.get('price') or None
        activity.opening_hours = request.POST.get('opening_hours')
        activity.website_url = request.POST.get('website_url')
        activity.rating = request.POST.get('rating') or None
        activity.save()
        return redirect('activity_list')

    return render(request, 'Activities/edit_activity.html', {
        'activity': activity,
        'cities': cities
    })

# 4. Delete an activity

def delete_activity(request, id):
    activity = get_object_or_404(Activities, id=id)
    if request.method == 'POST':
        activity.delete()
        return redirect('activity_list')
    return HttpResponseForbidden()
def add_destination(request):
    if request.method == "POST":
        name = request.POST.get("name")
        code = request.POST.get("code")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        Destination.objects.create(
            name=name,
            code=code,
            description=description,
            image=image
        )

        messages.success(request, "Destination added successfully")
        return redirect("destination_list")

    return render(request, "Destinations/add-destination.html")


def edit_destination(request, id):
    destination = get_object_or_404(Destination, id=id)

    if request.method == "POST":
        destination.name = request.POST.get("name")
        destination.code = request.POST.get("code")
        destination.description = request.POST.get("description")
        image = request.FILES.get("image")

        if image:
            destination.image = image

        destination.save()
        messages.success(request, "Destination updated successfully")
        return redirect("destination_list")

    return render(request, "Destinations/edit-destination.html", {"destination": destination})

def destination_list(request):
    destinations = Destination.objects.all()
    return render(request, "Destinations/destinations.html", {"destinations": destinations})
def delete_destination(request, id):
    if request.method == "POST":
        destination = get_object_or_404(Destination, id=id)
        destination.delete()
        messages.success(request, "Destination deleted successfully")
        return redirect("destination_list")
    return HttpResponseForbidden()



