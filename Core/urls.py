from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView, name='login'),
    path('register/', views.RegisterView, name='register'),  
    path('', views.Home, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.ForgotPassword, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', views.PasswordResetSent, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', views.ResetPassword, name='reset-password'),
    path('hotel/', views.hotel_list_view, name='hotel_page'),
    path('hotel_details/<int:hotel_id>/', views.hotel_detail_view, name='hotel_det'),
    path('hotelfiltre/', views.hotelfiltre, name='hotelfiltre'),
    path('api/countries/', views.get_countries, name='get_countries'),
    path('api/cities/', views.get_cities, name='get_cities'),
    path('hotel-id/cards/', views.hotel_id_cards_view, name='hotel-id-cards'),
    path('packages/', views.package_page, name='package_page'),  
    path('packages/<int:pk>/', views.package_det, name='package_det'),
    path('book/<str:booking_type>/<int:item_id>/', views.submit_booking_unified, name='submit_booking_unified'),
    path('Flight/', views.Flight_view, name='Flight_page'),   
    path('flightfiltre/', views.flightfiltre, name='flightfiltre'),   
    path('validate-coupon/', views.validate_coupon, name='validate_coupon'),  
    path('package-id/cards/', views.package_id_cards_view, name='package-id-cards'),
    path('packagefiltre/', views.packagefiltre, name='packagefiltre'),
    path('flight-id/cards/', views.flight_id_cards_view, name='flight-id-cards'),
    path('destination/', views.destination_view, name='destination'),
    path('constantine/', views.constantine_detail, name='constantine_detail'),
       #admin
    path('Home_admin/', views.index, name="Home"),  
    path('profile_admin/', views.profile, name="Profile"),
    #flights
    path("flights.html", views.flight_list, name="flight_list"),
    path("add/", views.add_flight, name="add_flight"),
    path("add-flight.html", views.add_flight, name="add_flight_html"),
    path('flights/edit/<int:id>/', views.edit_flight, name='edit_flight'),
    path('flights/delete/<int:id>/', views.delete_flight, name='delete_flight'),
    #hotels
    path("hotels.html", views.hotel_list, name="hotel_list"),
    path("add-hotel.html", views.add_hotel, name="add_hotel"),
    path('hotel/<int:id>/', views.hotel_details, name='hotel_details'),
    path('hotels/edit/<int:id>/', views.edit_hotel, name='edit_hotel'),
    path('hotels/delete/<int:id>/', views.delete_hotel, name='delete_hotel'),
    #packages
    path("packages.html", views.package_list, name="package_list"),
    path("add-package.html", views.add_package, name="add_package"),
    path('package/<int:id>/', views.package_details, name='package_details'),
    path('packages/edit/<int:id>/', views.edit_package, name='edit_package'),
    path('packages/delete/<int:id>/', views.delete_package, name='delete_package'),

    #CLIENTS
    path("clients.html", views.client_list, name="client_list"),
    path("add-client.html", views.add_client, name="add_client"),
    path("client/<int:id>/", views.client_details, name="client_details"),
    path("clients/edit/<int:id>/", views.edit_client, name="edit_client"),
    path("clients/delete/<int:id>/", views.delete_client, name="delete_client"),

    #agents 
     path("agents.html", views.agent_list, name="agent_list"),
    path("add-agent.html", views.add_agent, name="add_agent"),
    path("agent/<int:id>/", views.agent_details, name="agent_details"),
    path("agents/edit/<int:id>/", views.edit_agent, name="edit_agent"),
    path("agents/delete/<int:id>/", views.delete_agent, name="delete_agent"),
    #Bookings
    path("bookings.html", views.booking_list, name="booking_list"),
    path("add-booking.html", views.add_booking, name="add_booking"),
    path("booking/<int:id>/", views.booking_details, name="booking_details"),
    path("bookings/edit/<int:id>/", views.edit_booking, name="edit_booking"),
    path("bookings/delete/<int:id>/", views.delete_booking, name="delete_booking"),
    #statistics 
    path('chart-data/', views.chart_data, name='chart_data'),
    path('client-chart-data/', views.client_chart_data, name='client_chart_data'),

    #cities
    path("cities.html", views.city_list, name="city_list"),
    path("add-city/", views.add_city, name="add_city"),
    path("add-city.html", views.add_city, name="add_city_html"),
    path("cities/edit/<int:id>/", views.edit_city, name="edit_city"),
    path("cities/delete/<int:id>/", views.delete_city, name="delete_city"),

    #destinations 
    path("destinations.html", views.destination_list, name="destination_list"),
    path("add-destination/", views.add_destination, name="add_destination"),
    path("add-destination.html", views.add_destination, name="add_destination_html"),
    path("destinations/edit/<int:id>/", views.edit_destination, name="edit_destination"),
    path("destinations/delete/<int:id>/", views.delete_destination, name="delete_destination"),
    
    #activities 
    path("activities.html", views.activity_list, name="activity_list"),
    path("add-activity/", views.add_activity, name="add_activity"),
    path("add-activity.html", views.add_activity, name="add_activity_html"),
    path("activities/edit/<int:id>/", views.edit_activity, name="edit_activity"),
    path("activities/delete/<int:id>/", views.delete_activity, name="delete_activity"),
    path('best-things-to-do/', views.best_things_to_do, name='best_things_to_do'),
    path('best-time-to-visit/', views.best_time_to_visit, name='best_time_to_visit'),
    path('best-dishes/', views.best_dishes, name='best_dishes'),
    path('best-places/', views.best_places, name='best_places'),

    ]