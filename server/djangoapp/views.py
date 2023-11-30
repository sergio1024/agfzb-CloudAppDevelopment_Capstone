'''Views'''
import logging
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from .models import CarModel


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    '''Creates an `about` view to render a static about page'''
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    '''Creates a `contact` view to return a static contact page'''
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


# This view and this page is not part of the exercise,
# I just thought it would be an effective way to get around with errors
# without blocking the execution of the code.
#=======================================================================
# Create a `error` view to return a static contact page
#def contact(request):
def error(request):
    '''Creates a `error` view to return a static error page'''
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/error.html', context)
#======================================================================


# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    '''Creates a `login_request` view to handle sign in request'''
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
    if username == "" or password == "": # In case the fields are empty
        context['error'] =  ("Forgot your login details? No problem! "
        "Get in touch with us, and "
        "we will be happy to help you. "
        "You will be now directed to our contacts page.")
        return render(request, 'djangoapp/contact.html', context)
    elif user is not None:    
        login(request, user)
        return render(request, 'djangoapp/index.html', context)
    else: # In case the credentials are wrong
        context['error'] =  ("INCORRECT LOGIN DETAILS!!! But don t worry! "
        "You will be now directed to our error page. "
        "You can try again, there is no limit to the number of attempts! "
        "Use our contact page if you have any questions.")
        return render(request, 'djangoapp/error.html', context)


# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    '''Creates a `logout_request` view to handle sign out request'''
    context = {}
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return render(request, 'djangoapp/index.html', context)


# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    '''Creates a `registration_request` view to handle sign up request'''
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except():
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name,
             last_name=last_name, password=password)
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    '''Update the `get_dealerships` view to render the index page with a list of dealerships'''
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/083e1099-73a9-4b54-b7a4-454021498f80/api/dealerships.json"
        # Get dealers from the URL
        try:
            dealerships = get_dealers_from_cf(url)
            context = {
                "dealerships": dealerships,
            }
            return render(request, 'djangoapp/index.html', context)
        except Exception as e:
            # If an error occurs, redirect to an error page
            print(e)  # Print the error to the console
            return render(request, 'djangoapp/error.html')


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    '''Create a `get_dealer_details` view to render the reviews of a dealer'''
    if request.method == "GET":
        url_r = f"https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/a9220b6d6b26f1eb3b657a98770b743616f7d4cd223b89cd1ca4e88ab49bdb92/api/review?dealerId={dealer_id}"
        url_ds = f"https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/a9220b6d6b26f1eb3b657a98770b743616f7d4cd223b89cd1ca4e88ab49bdb92/api/dealership?dealerId={dealer_id}"
        # Get dealers from the URL
        try:
            context = {
               "dealer": get_dealers_from_cf(url_ds)[0],
               "reviews": get_dealer_reviews_from_cf(url_r, dealer_id),
            }
            return render(request, 'djangoapp/dealer_details.html', context)
        except Exception as e:
            # If an error occurs, redirect to an error page
            print(e)  # Print the error to the console
            return render(request, 'djangoapp/error.html')


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
def add_review(request, dealer_id):
    '''Create a `add_review` view to submit a review'''
    if request.method == "GET":
        url = f"https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/a9220b6d6b26f1eb3b657a98770b743616f7d4cd223b89cd1ca4e88ab49bdb92/api/dealership?dealerId={dealer_id}"
        # Get dealers from the URL
        try:
            context = {
                "cars": CarModel.objects.all(),
                "dealer": get_dealers_from_cf(url)[0],
            }
            print(context)
            return render(request, 'djangoapp/add_review.html', context)
        except Exception as e:
            # If an error occurs, redirect to an error page
            print(e)  # Print the error to the console
            return render(request, 'djangoapp/error.html')
    if request.method == "POST":
        form = request.POST
        review = {
            "name": f"{request.user.first_name} {request.user.last_name}",
            "dealership": dealer_id,
            "review": form["content"],
            "purchase": form.get("purchasecheck"),
            }
        if form.get("purchasecheck"):
            review["purchasedate"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
            car = CarModel.objects.get(pk=form["car"])
            review["car_make"] = car.car_make.name
            review["car_model"] = car.name
            review["car_year"]= car.year.strftime("%Y")
        json_payload = {"review": review}
        URL = 'https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/a9220b6d6b26f1eb3b657a98770b743616f7d4cd223b89cd1ca4e88ab49bdb92/api/review'
        post_request(URL, json_payload, dealerId=dealer_id)
    return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
