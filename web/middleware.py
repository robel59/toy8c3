# myapp/middleware.py
import datetime
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import UserAccess

from django.contrib.sessions.models import Session
import requests

from geopy.geocoders import Nominatim

def get_location_from_ip1(ip_address):
    geolocator = Nominatim(user_agent="myGeocoder")

    try:
        location = geolocator.geocode(ip_address)
        if location:
            return location.address
        else:
            return "Location not found"
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Error occurred while fetching location"
    

def get_country_from_ip(ip_address):
    try:
        #response = requests.get(f'http://ip-api.com/json/{ip_address}')
        data ={}# response.json()
        if data['status'] == 'success':
            return data['country']
        else:
            return 'Unknown Country'
    except Exception as e:
        print(f"Error fetching country for IP {ip_address}: {e}")
        return 'Unknown Country'



class UserAccessMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Skip recording for API requests
        if '/api/' in request.path or '/ws/' in request.path or '/media/' in request.path:
            return  # Do not record this request

        session_key = request.session.session_key
        if not session_key:
            request.session.save()  # Ensure the session is saved and has a key
            session_key = request.session.session_key

        # Check if this session key has already been recorded
        if UserAccess.objects.filter(session_key=session_key).exists():
            return  # Skip recording if session key already exists

        # Check if the session has been recently recorded
        last_access_time = request.session.get('last_access_time')
        if last_access_time:
            last_access_time = datetime.datetime.fromisoformat(last_access_time)
            if (timezone.now() - last_access_time).seconds < 60:  # Skip if last access was less than 60 seconds ago
                return

        ip_address = request.META.get('REMOTE_ADDR')
        location = get_country_from_ip(ip_address)
        referer = request.META.get('HTTP_REFERER', '')

        UserAccess.objects.create(
            ip_address=ip_address,
            location=location,
            referer=referer,
            session_key=session_key
        )

        # Update session with the new access time
        request.session['last_access_time'] = timezone.now().isoformat()




class UserAccessMiddleware3:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user's session already has an access record
        if not request.session.get('access_recorded', False):

            referer = request.META.get('HTTP_REFERER')
            if referer:
                UserAccess.objects.create(
                    ip_address=request.META.get('REMOTE_ADDR'),
                    location=request.META.get('HTTP_USER_AGENT'),
                    access_time=timezone.now(),
                    referer=referer
                )


            # Mark that the access has been recorded for this session
            request.session['access_recorded'] = True

        response = self.get_response(request)
        return response