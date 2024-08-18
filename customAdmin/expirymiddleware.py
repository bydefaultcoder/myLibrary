from django.shortcuts import redirect
from datetime import date

class CheckUserExpiryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("helo")
        response = self.get_response(request)
        return response