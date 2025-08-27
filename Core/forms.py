from django import forms
from .models import Hotel, Package, Booking

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = '__all__'

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
