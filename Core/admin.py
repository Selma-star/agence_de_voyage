from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import *

# Custom User Admins
class AgentAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'insurance_number', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('email', 'full_name', 'insurance_number')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone', 'insurance_number', 'role', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

class ClientAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'age', 'gender', 'is_active', 'is_staff')
    list_filter = ('gender', 'is_active', 'is_staff')
    search_fields = ('email', 'full_name', 'phone')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone', 'age', 'gender', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

# Model Admins
class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'reset_id', 'created_when')
    search_fields = ('client__email', 'agent__email')
    list_filter = ('created_when',)

    def get_user(self, obj):
        return obj.client or obj.agent
    get_user.short_description = 'User'

class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

class CitiesAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'airport_code')
    list_filter = ('destination',)
    search_fields = ('name', 'airport_code')

class ActivitiesAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'price', 'rating')
    list_filter = ('city',)
    search_fields = ('name', 'activity_type')

class ActivityImagesAdmin(admin.ModelAdmin):
    list_display = ('activity', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="50" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Preview'

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'published_at')
    list_filter = ('city', 'published_at')
    search_fields = ('title', 'content')

class FlightAdmin(admin.ModelAdmin):
    list_display = ('airline_company', 'get_departure', 'get_arrival', 'departure_time', 'status')
    list_filter = ('status', 'departure_city', 'arrival_city')
    search_fields = ('airline_company', 'plane_model')

    def get_departure(self, obj):
        return f"{obj.departure_city.name} ({obj.departure_iata or '-'})"
    get_departure.short_description = 'From'

    def get_arrival(self, obj):
        return f"{obj.arrival_city.name} ({obj.arrival_iata or '-'})"
    get_arrival.short_description = 'To'

class FlightClassesAdmin(admin.ModelAdmin):
    list_display = ('flight', 'class_type', 'price_multiplier', 'available_seats')
    list_filter = ('class_type',)

class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'type', 'rating', 'contact_email')
    list_filter = ('type', 'city', 'rating')
    search_fields = ('name', 'contact_email')

class HotelImageAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="50" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Preview'

class HotelRoomsAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'room_type', 'price_per_night', 'available_rooms')
    list_filter = ('hotel',)

class RoomImagesAdmin(admin.ModelAdmin):
    list_display = ('hotelroom', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="50" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Preview'

class ServicesAdmin(admin.ModelAdmin):
    list_display = ('service_name',)
    search_fields = ('service_name',)

class HotelServiceAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'service', 'price')
    list_filter = ('hotel', 'service')

class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'price', 'duration')
    list_filter = ('city',)
    search_fields = ('name', 'description')


class PackageImageAdmin(admin.ModelAdmin):
    list_display = ('package', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="50" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Preview'

class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_code', 'client', 'status', 'booked_at')
    list_filter = ('status', 'package_type', 'booked_at')
    search_fields = ('booking_code', 'client__email')

class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'currency', 'status', 'paid_at')
    list_filter = ('status', 'currency', 'payment_method')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client', 'get_service', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')

    def get_service(self, obj):
        return obj.hotel or obj.flight or obj.package
    get_service.short_description = 'Service'

class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ('agent', 'get_service', 'discount_percentage', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')

    def get_service(self, obj):
        return obj.hotel or obj.flight or obj.package
    get_service.short_description = 'Service'

class CancellationAdmin(admin.ModelAdmin):
    list_display = ('booking', 'agent', 'refund_amount', 'canceled_at')
    list_filter = ('canceled_at',)

# Register all models
admin.site.register(Agent, AgentAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(PasswordReset, PasswordResetAdmin)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(Cities, CitiesAdmin)
admin.site.register(Activities, ActivitiesAdmin)
admin.site.register(ActivityImages, ActivityImagesAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(FlightClasses, FlightClassesAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(HotelImage, HotelImageAdmin)
admin.site.register(HotelRooms, HotelRoomsAdmin)
admin.site.register(RoomImages, RoomImagesAdmin)
admin.site.register(Services, ServicesAdmin)
admin.site.register(HotelService, HotelServiceAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(PackageImage, PackageImageAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Payments, PaymentsAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(SpecialOffer, SpecialOfferAdmin)
admin.site.register(Cancellation, CancellationAdmin)
admin.site.register(PromoCode)