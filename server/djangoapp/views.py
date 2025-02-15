from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_request, get_dealer_reviews_from_cf

from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, "djangoapp/about.html")



# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, "djangoapp/contact.html")

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        psw = request.POST["psw"]
        user = authenticate(username=username, password=psw)
        if user is not None:
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, "djangoapp/login.html", context)
    
    else:
        return render(request, "djangoapp/login.html", context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect("djangoapp:index")


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/registration.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["psw"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        exist = False
        try:
            User.objects.get(username=username)
            exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not exist:
            user = User.objects.create(username=username, first_name=first_name, last_name=last_name, password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/2fc9619c-d3e1-4ab1-afc4-075459516547/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == 'GET' and dealer_id:
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/2fc9619c-d3e1-4ab1-afc4-075459516547/dealership-package/reviews"

        reviews = get_dealer_reviews_from_cf(url, dealer_id)

        reviews_details = " ".join([review.sentiment for review in reviews])

        return HttpResponse(reviews_details)
# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

