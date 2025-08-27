from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField  # If using PostgreSQL
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.utils import timezone

class PasswordReset(models.Model):
    client = models.ForeignKey(
        'Client', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name="password_resets"
    )
    agent = models.ForeignKey(
        'Agent', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name="password_resets"
    )
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    created_when = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Ensure that at least one of 'client' or 'agent' is set."""
        if not self.client and not self.agent:
            raise ValueError("Either 'client' or 'agent' must be set for password reset.")

    def __str__(self):
        if self.client:
            return f"Password reset for client {self.client.full_name} at {self.created_when}"
        elif self.agent:
            return f"Password reset for agent {self.agent.full_name} at {self.created_when}"
        return "Invalid Password Reset Entry"

    class Meta:
        db_table = 'password_resets'
        ordering = ['-created_when']  # Most recent resets first


class AgentManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        agent = self.model(email=email, **extra_fields)
        agent.set_password(password)
        agent.save(using=self._db)
        return agent
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with a given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, password, **extra_fields)


class Agent(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255, db_index=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    insurance_number = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=5)
    image = models.ImageField(upload_to='agents_images/', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    objects = AgentManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(Group, related_name="agent_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="agent_permissions", blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'agents'

class ClientManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        client = self.model(email=email, **extra_fields)
        client.set_password(password)
        client.save(using=self._db)
        return client

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Client(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255, db_index=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='users_images/', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  
    is_superuser = models.BooleanField(default=False)

    objects = ClientManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    groups = models.ManyToManyField(Group, related_name="client_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="client_permissions", blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'clients'



class Destination(models.Model):
    name = models.CharField(unique=True, max_length=255)
    code = models.CharField(unique=True, max_length=10)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'destinations'

class Cities(models.Model):
    name = models.CharField(max_length=255)
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE)
    timezone = models.CharField(max_length=50, blank=True, null=True)
    airport_code = models.CharField(max_length=10, blank=True, null=True)
    image = models.ImageField(upload_to='cities/', blank=True, null=True)
    short_description = models.CharField(max_length=255 ,default="No short description yet.")  # For a brief summary
    long_description = models.TextField(default="No description yet.")  # For a detailed overview

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cities'

class LocalDish(models.Model):
    city = models.ForeignKey('Cities', on_delete=models.CASCADE, related_name='dishes')
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='dishes/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.city.name})"
    
class Restaurant(models.Model):
    city = models.ForeignKey('Cities', on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    image = models.ImageField(upload_to='restaurants/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.city.name})"


class Activities(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey('Cities', models.CASCADE)
    activity_type = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    opening_hours = models.CharField(max_length=255, blank=True, null=True)
    website_url = models.URLField(max_length=255, blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'activities'


class ActivityImages(models.Model):
    activity = models.ForeignKey(Activities, models.CASCADE)
    image = models.ImageField(upload_to='activities/', blank=True, null=True)
    def __str__(self):
        return f"Image for {self.activity.name}"
    class Meta:
        db_table = 'activity_images'



class Article(models.Model):
    city = models.ForeignKey('Cities', on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(blank=True, null=True)
    activity = models.ForeignKey(Activities, on_delete=models.CASCADE, blank=True, null=True)

    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    icon = models.ImageField(upload_to='articles/', blank=True, null=True)
    def __str__(self):
        return f"{self.title} ({self.city.name})"
    class Meta:
        db_table = 'articles'

class CitySeasonInfo(models.Model):
    SEASON_CHOICES = [
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('autumn', 'Autumn'),
        ('winter', 'Winter'),
    ]

    city = models.ForeignKey('Cities', related_name='seasons', on_delete=models.CASCADE)
    season = models.CharField(max_length=10, choices=SEASON_CHOICES)
    description = models.TextField()  # what's the city like in this season?
    image1 = models.ImageField(upload_to='seasons/', null=True, blank=True)  # optional
    image2 = models.ImageField(upload_to='seasons/', null=True, blank=True)  # optional
    is_best_season = models.BooleanField(default=False)  # true if this is the best season to visit

    class Meta:
        unique_together = ('city', 'season')  # avoid duplicate season entries per city

    def __str__(self):
        return f"{self.city.name} in {self.get_season_display()}"

class Place(models.Model):
    city = models.ForeignKey('Cities', on_delete=models.CASCADE, related_name='places')
    name = models.CharField(max_length=200)  # Name of the place
    description = models.TextField()  # Description of the place
    image1 = models.ImageField(upload_to='places/', null=True, blank=True)  # Optional image
    image2 = models.ImageField(upload_to='places/', null=True, blank=True)  # Optional image
    is_best_place = models.BooleanField(default=False)  # Mark the best place

    class Meta:
        unique_together = ('city', 'name')  # Ensure no duplicate places for a city

    def __str__(self):
        return f"{self.name} in {self.city.name}"


class Flight(models.Model):
    departure_city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    departure_iata = models.CharField(max_length=10, blank=True, null=True)
    departure_time = models.DateTimeField()
    arrival_city = models.ForeignKey(Cities, on_delete=models.CASCADE, related_name='flights_arrival_city_set')
    arrival_iata = models.CharField(max_length=10, blank=True, null=True)
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()
    available_seats = models.IntegerField()
    airline_company = models.CharField(max_length=255)
    plane_model = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=9)
    image = models.ImageField(upload_to='flights/', blank=True, null=True)
    stops = models.IntegerField(default=0) 
    def __str__(self):
        return self.airline_company
    class Meta:
        db_table = 'flights'

class FlightClasses(models.Model):
    flight = models.ForeignKey('Flight', models.CASCADE)
    class_type = models.CharField(max_length=11)
    price_multiplier = models.DecimalField(max_digits=3, decimal_places=2)
    available_seats = models.IntegerField()
    def __str__(self):
        return self.class_type
    class Meta:
        db_table = 'flight_classes'



class Hotel(models.Model):

    HOTEL_TYPES = [
        ('LUXE', 'Luxe'),
        ('FAMILIALE', 'Familiale'),
        ('POPULAIRE', 'Populaire'),
    ]
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.ForeignKey(Cities, models.CASCADE)
    hotel_telephone = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.EmailField(max_length=255, blank=True, null=True)   
    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    website_url = models.URLField(max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=10, blank=True, null=True)
    image = models.ImageField(upload_to='hotels/', blank=True, null=True)
    type = models.CharField(max_length=10, choices=HOTEL_TYPES, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # Add latitude and longitude fields
    latitude = models.DecimalField(max_digits=11, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=7, blank=True, null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'hotels'


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_images')
    image = models.ImageField(upload_to='hotel_images/')
    description = models.CharField(max_length=255, blank=True, null=True)  # e.g. "Lobby", "Suite", etc.
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.description or 'Image'}"

class HotelRooms(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE)
    room_type = models.CharField(max_length=50)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    available_rooms = models.IntegerField()
    description = models.TextField(null=True, blank=True)  
    def __str__(self):
        return f"{self.room_type} at {self.hotel.name}"
    class Meta:
        db_table = 'hotel_rooms'

class RoomImages(models.Model):
    hotelroom = models.ForeignKey(HotelRooms, models.CASCADE)
    image = models.ImageField(upload_to='hotels/HotelRooms/', blank=True, null=True)
    def __str__(self):
        return f"Image for {self.hotelroom.room_type} at {self.hotelroom.hotel.name} "
    
    class Meta:
        db_table = 'room_images'


class Services(models.Model):
    service_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to='hotels/hotels_services/service_icons/', blank=True, null=True)
    def __str__(self):
        return self.service_name
    class Meta:
        db_table = 'services'


class HotelService(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE)
    service = models.ForeignKey('Services', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='hotels/hotels_services/', blank=True, null=True)
    
    class Meta:
        db_table = 'hotel_services'




class Package(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey('Cities', on_delete=models.CASCADE)
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE)
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE)
    activity = models.ForeignKey('Activities', null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    duration = models.IntegerField(help_text="Duration in days")  # Trip duration
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    max_people = models.IntegerField(default=1)  # Maximum number of people
    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    included_features = ArrayField(models.CharField(max_length=255), blank=True, null=True)  # List of included services  
    transportation_details = models.CharField(max_length=255, null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "packages"

# Image Model to handle multiple images per package
class PackageImage(models.Model):
    package = models.ForeignKey(
        'Package',
        on_delete=models.CASCADE,
        related_name="package_images"
    )

    # your original image
    image = models.ImageField(upload_to='packages/', blank=True, null=True)

    # where-to-go
    where_to_go_title        = models.CharField(max_length=255, blank=True)
    img_where_to_go          = models.ImageField(upload_to='where_to_go/', blank=True, null=True)
    description_where_to_go  = models.TextField(blank=True)

    # where-to-eat
    where_to_eat_title        = models.CharField(max_length=255, blank=True)
    img_where_to_eat          = models.ImageField(upload_to='where_to_eat/', blank=True, null=True)
    description_where_to_eat  = models.TextField(blank=True)

    def __str__(self):
        return f"Assets for {self.package.name}"

    class Meta:
        db_table = 'package_images'



class Booking(models.Model):
    booking_code = models.CharField(max_length=50, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    city = models.ForeignKey('Cities', on_delete=models.CASCADE)
    flight = models.ForeignKey('Flight', null=True, blank=True, on_delete=models.SET_NULL)
    hotel = models.ForeignKey('Hotel', null=True, blank=True, on_delete=models.SET_NULL)
    package = models.ForeignKey('Package', null=True, blank=True, on_delete=models.SET_NULL)
    PACKAGE_TYPES = [
        ('flight-only', 'Flight Only'),
        ('hotel-only', 'Hotel Only'),
        ('full-package', 'Full Package'),
    ]
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPES)

    # Optional if hotel is booked
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    number_of_nights = models.IntegerField(null=True, blank=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        booked = self.booked_at.strftime('%Y-%m-%d %H:%M') if self.booked_at else "unsaved"
        return f"Booking of {self.client.full_name} at {booked}"
    class Meta:
        db_table = "bookings"
    



class Payments(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    CURRENCY_CHOICES = [
    ('USD', 'US Dollar'),
    ('EUR', 'Euro'),
    ('GBP', 'British Pound'),
    ('DZD', 'Algerian Dinar'),
    ]

    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    PAYMENT_METHOD_CHOICES = [
    ('credit_card', 'Credit Card'),
    ('paypal', 'PayPal'),
    ('bank_transfer', 'Bank Transfer'),
    ('edahabia', 'Edahabia'),
    ]

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(unique=True, max_length=50)
    paid_at = models.DateTimeField(blank=True, null=True)
    refunded_at = models.DateTimeField(blank=True, null=True)
    PAYMENT_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
    ('refunded', 'Refunded'),
    ]

    status = models.CharField(max_length=9, choices=PAYMENT_STATUS_CHOICES, default='pending')

    class Meta:
        db_table = 'payments'


class Review(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE) 
    
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, null=True, blank=True)
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE, null=True, blank=True)
    package = models.ForeignKey('Package', on_delete=models.CASCADE, null=True, blank=True)

    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Ensures rating is between 1 and 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'

class SpecialOffer(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, blank=True, null=True)

    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, null=True, blank=True)
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE, null=True, blank=True)
    package = models.ForeignKey('Package', on_delete=models.CASCADE, null=True, blank=True)

    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        db_table = 'special_offers'
    def __str__(self):
        return f"Special Offer: {self.discount_percentage}% off"


class Cancellation(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, blank=True, null=True)  # Nullable if no agent
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    canceled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cancellations'

class PromoCode(models.Model):
    LOYALTY_CHOICES = [
        ('all', 'All'),
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ]

    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField(default=10)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    times_used = models.PositiveIntegerField(default=0)

    loyalty_level = models.CharField(
        max_length=10,
        choices=LOYALTY_CHOICES,
        default='all',
        help_text="Set who can see this code: All users or based on loyalty tier."
    )

    def is_valid(self):
        now = timezone.now()
        return (
            self.is_active and
            self.start_date <= now <= self.end_date and
            (self.usage_limit is None or self.times_used < self.usage_limit)
        )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Promo Code"
        verbose_name_plural = "Promo Codes"
        ordering = ['-start_date']
