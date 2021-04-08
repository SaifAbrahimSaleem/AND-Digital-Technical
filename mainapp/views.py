from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.contrib.auth import logout
from django.http import JsonResponse
from django.core import serializers
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from dateutil.parser import parse
from .utilities import (
    basket_content,
    ProcessOrder,
    get_basket,
    get_shoes_from_category,
    get_gender_categories,
    sort_shoes,
    DecimalEncoder,
)
from .serializers import (
    ShoeSerializer,
    ShoeSearchSerializer,
    SizeSerializer,
    OrderSerializer,
    OrderItemSerializer,
    ShippingSerializer,
    ReviewSerializer
)
from .models import Shoe, Size, Customer, Order, OrderItem, User, Shipping, Voucher, Review
from .forms import (
    ContactForm,
    LoginForm, 
    RegisterForm
)
import datetime
import urllib
import json
import pytz

"""
    The general logic for each method which renders a page is as follows: 
        - Build and get the basket data
        - Pass the contact form and (depending on the page) the login and signup forms
"""

@api_view(["GET"])
def index(request):
    response = {}
    if request.user.is_superuser:
        logout(request)
    response["basket"] = basket_content(request, request.data)
    response["form"] = ContactForm()
    return render(request, "mainapp/index.html", response)

"""
    PRODUCT DETAIL METHOD:
        LOGIC:
            - This method is passed the catalogue code of a shoe as a parameter in the url (ref urls.py)
            - The shoe data is found and serialized. 
            - Since there is a review section on the product detail page, all the reviews for that particular shoe are queried, serialized
              and returned:
                * As the customer model returns its id by default (ref models.py @ __str__(self)) the serialized data is parsed to json data
                  and manipulated: The customer id is changed to the username of the user that left the comment (Customer.User.username) and 
                  date_added is casted to a human-readable format (parsing from Django Timezone aware datetime (TZ) to strftime (string for-
                  matted time))
                

"""
@api_view(["GET"])
def product_detail(request, code):
    response = {}
    shoe = Shoe.objects.get(catalogue_code=code)
    reviews = Review.objects.filter(shoe=shoe)
    review_serializer = ReviewSerializer(reviews, many=True)
    json_reviews = json.loads(json.dumps(review_serializer.data))
    for review in json_reviews:
        customer = Customer.objects.get(id=review["customer"])
        review['customer'] = customer.user.username
        review['date_added'] = timezone.datetime.strftime(parse(review['date_added']), '%d/%m/%Y')
    response["code"] = code
    response["basket"] = basket_content(request, request.data)
    response["form"] = ContactForm()
    response["reviews"] = json_reviews
    return render(request, "mainapp/product_detail.html", response)

"""
    PRODUCT_LIST METHOD:
    - This is an independent, asynchronous method which takes a request and returns a JsonResponse (a dictionary)
    LOGIC:
        - Query all Shoe objects from the database, serialize them and return them to be rendered on the page
        - Potential Extension: Paginating all large querysets to improve front-end machine performance
"""

@api_view(["GET"])
def product_list(request):
    response = {}
    shoes = Shoe.objects.all()
    serializer = ShoeSerializer(shoes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

"""
    SEARCH_BAR METHOD:
        When the minimum number of characters is entered into the searchbar, a get request is sent to the server to find any shoe instances matching the search text:
            If there is only one word, filter the database for any objects who's name or collection matches the search text and return them
            Otherwise, if the search text is more than one word, the process is slightly more complex as a filter operation for each word must be conducted:
                - Take the search input and split it into an array of keywords.
                - create a Query object, to filter through the name and collection fields.
                - Take the first element of this list and complete an in-place OR (IOR) operation for each query in the queryset e.g. x |= 5 means x = x | 5 (x or 5).
                - Filter the database for these objects and return them.
"""
@api_view(["GET"])
def search_bar(request, code=None):
    response = {}
    search_text = request.GET.get("search_text")
    if " " in search_text:
        keywords = search_text.split(" ")
        qs = [
            Q(name__icontains=keyword) | Q(collection__icontains=keyword)
            for keyword in keywords
        ]
        query = qs.pop()
        for q in qs:
            query |= q
        queryset = Shoe.objects.filter(query)
    else:
        queryset = Shoe.objects.filter(
            Q(name__icontains=search_text) | Q(collection__icontains=search_text)
        )
    serializer = ShoeSearchSerializer(queryset, many=True)
    # PAGINATE RESULTS AND LIMIT TO 10 --> Extension
    return JsonResponse(serializer.data, safe=False)

"""
    SEARCH METHOD:
    LOGIC:
        - Find the category given in the url query "?category=arg" and find the correct category to query in utilities.py (ref. get_shoes_from_category()).
          the method will return a QueryDict object containing all objects found by the given category
        - Sort the shoes based on their prices and return the data in a json format (for template manipulation)
"""
@api_view(["GET"])
def search(request):
    response = {}
    response["basket"] = basket_content(request, request.data)
    response["form"] = ContactForm()
    category = request.GET.get("category")
    shoes, category = get_shoes_from_category(category)
    shoes = sort_shoes(shoes)
    serializer = ShoeSerializer(shoes, many=True)
    response["shoes"] = json.loads(json.dumps(serializer.data, cls=DecimalEncoder))
    response["category"] = "".join(category)
    response["categories"] = get_gender_categories(category)
    return render(request, "mainapp/search.html", response)

"""
    GET_PRODUCT_DETAIL:
    LOGIC:
        - Find the required shoe through querying the code sent as a url parameter
        - Serialize and return the resultant shoe
    
"""
@api_view(["GET"])
def get_product_detail(request, code): 
    response = {}
    if Shoe.objects.filter(catalogue_code=code).exists():
        shoe = Shoe.objects.get(catalogue_code=code)
        serializer = ShoeSerializer(shoe, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        response["Error"] = "Product does not exist!"
        return Response(response, status=status.HTTP_404_NOT_FOUND)

"""
    UPDATE_COOKIES_ASYNCH METHOD
        - This method is used to update the basket content (cookies) asynchronously (without reloading the page)
        - The result is a json formatted basket which is returned to the frontend, which will update the document basket cookie
"""

@api_view(["POST"])
def update_cookies_asynch(request, code=None):
    cookies = basket_content(request, request.data)
    return JsonResponse(cookies, safe=False)

"""
    CHECKOUT METHOD:
    - The sole purpose of this method is to provide the necessary basket data to render the checkout page
"""
@api_view(["GET"])
def checkout(request): 
    response = {}
    basket = basket_content(request, request.data)
    items = json.loads(basket)
    response["basket"] = basket
    response["basket_items"] = [x for x in items["items"]]
    response["basket_content"] = items
    response["form"] = ContactForm()
    return render(request, "mainapp/checkout.html", response)

"""
    DISCOUNT METHOD:
    - The purpose of this method is to find a valid discount code to apply to the total on the checkout.
    LOGIC:
        - Query the code passed in the request.GET parameter.
        - If the current time is less than the vouchers valid to attribute, return the discount given by the voucher code
        - Otherwise, return an error message
"""
@api_view(['GET'])
def discount(request):
    response = {}
    code = request.GET.get('code')
    try:
        voucher = Voucher.objects.get(code=code)  
        if timezone.now() < voucher.valid_to:
            response["message"] = "Voucher Successfully Applied!"
            response["discount"] = voucher.discount
            response["code"] = 1
        else:
            response["message"] = "Voucher Expired"
            response["code"] = 0
    except Voucher.DoesNotExist:
        response["message"] = "Voucher does not exist"
        response["code"] = 0
    return JsonResponse(response, safe=False)

"""
    PROCESS_ORDER METHOD:
    - This method is called when the user clicks on the checkout button and atempts to process the order contained within the current basket
    LOGIC:
        - Find the customer and get/create an order for the customer (ref. utilities.py => ProcessOrder)
        - Mark the order as complete
        - Take the shipping information, given by the form
        - Find each shoe contained within the basket and deduct the appropriate quantities
        - render the correct email template and send it (attaching template variables to it) (as order.completed==True implies that the order has been successfully completed)
        - Return the appropriate data to be rendered in the consequent redirect to the order_success method
"""
@api_view(["POST"])
def process_order(request):
    response = {}
    basket = json.loads(basket_content(request, None))
    customer, order = ProcessOrder(request, request.data)        
    total = float(basket["order"]["basket_total"])
    if total == order.get_basket_total:
        order.completed = True
    try:
        order.save()
    except Exception as e:
        print(e)
    if order.completed == True:
        total_price = order.get_basket_total
        total_items = order.get_basket_items
        shipping = Shipping.objects.create(
            customer=customer,
            order=order,
            address=request.data["address"],
            city=request.data["city"],
            postcode=request.data["postcode"],
        )
        order_items = order.orderitem_set.all()
        items = {}
        for item in order_items:
            shoe = Shoe.objects.get(catalogue_code=item.shoe.catalogue_code)
            shoe.quantity -= item.quantity
            order_item_serializer = OrderItemSerializer(item, many=False)
            items[item.id] = order_item_serializer.data
            try:
                shoe.save()
            except Exception as e:
                print(e)
        order_serializer = OrderSerializer(order, many=False)
        shipping_serializer = ShippingSerializer(shipping, many=False)
        response["email"] = customer.email
        response["items"] = items
        response["message"] = "Order Successful!"
        response["transaction_id"] = order.transaction_id
        response["total_price"] = request.data['total']
        response["total_items"] = order.get_basket_items
        response["shipping"] = shipping_serializer.data
        email_template = get_template("mainapp/success_email.html")
        contact_email = customer.email
        today = timezone.now()
        duration = today + datetime.timedelta(days=30)
        voucher, created = Voucher.objects.get_or_create(code="SPECIAL20")
        voucher.valid_to = duration
        voucher.discount=0.1
        subject, from_email, to = (
        "Order Received! - Golden Shoe",
        "saifportfolioprojects@gmail.com",
        contact_email,   
        )
        e = {
            "items": [items[x] for x in items],
            "transaction_id": response["transaction_id"],
            "total_price": response["total_price"],
            "shipping": json.loads(json.dumps(shipping_serializer.data)),
            "voucher":voucher.code
        }
        email_content = email_template.render(e)
        email = EmailMessage(subject, email_content, from_email, [to])
        email.content_subtype = "html"
        try:
            email.send()
            voucher.save()
        except Exception as e:
            print(e)
    return JsonResponse(response, safe=False)

"""
    ORDER_SUCCESS METHOD:
        LOGIC:
        - Take data passed by the url string query in the redirect and parse the data to the appropriate datatype before returning it to be rendered
          as part of the context dictionary

"""
@api_view(["GET"])
def order_success(request):
    response = {}
    items = json.loads(request.GET.get("items"))
    response["email"] = request.GET.get("email")
    response["items"] = [items[x] for x in items]
    response["message"] = request.GET.get("message").replace('"', " ")
    response["total_price"] = "£{:.2f}".format(float(request.GET.get("total_price").replace('"', " ")))
    response["total_items"] = request.GET.get("total_items").replace('"', " ")
    response["transaction_id"] = request.GET.get("transaction_id").replace('"', " ")
    response["shipping"] = json.loads(request.GET.get("shipping"))
    response["basket"] = basket_content(request, request.data)
    response["form"] = ContactForm()
    return render(request, "mainapp/success.html", response)

"""
    PORTAL METHOD:
    This method serves as a precursor to the login and signup methods and is solely for the rendering of the portal page.
"""
@api_view(['GET'])
def portal(request):
    response = {}
    response['basket'] = basket_content(request, request.data)
    response["form"] = ContactForm()
    response['login_form'] = LoginForm() 
    response['register_form'] = RegisterForm()
    return render(request, 'mainapp/portal.html', response)

def login_view(request):
    response = {}
    user = request.user
    if request.is_ajax and request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            
            user = authenticate(email=email, password=raw_password)
            if user:
                login(request, user)
                response['code'] = 1
                response['redirect'] = 1
            else:
                response['response'] = "User with the entered email does not exist. Please Signup to continue"
                response['redirect'] = 0
                response['code'] = 0
        else:
            response['form_errors'] = form.errors
            response['redirect'] = 0
            response['code'] = 0
    else:
        response['response'] = 'Something went Wrong! Please try again Later.'
        response['redirect'] = 0
        response['code'] = 0
    return JsonResponse(response, safe=False)

def signup(request):
        response = {}
        if request.method == 'POST':
            form = RegisterForm(data = request.POST)
            if form.is_valid():
                user = form.save()
                customer=Customer.objects.create(user=user)
                customer.email = user.email
                customer.name = user.first_name
                login(request, user)
                response['response'] = 'Registered Successfully! You can now login! Check your email for a special surprise!'
                response['redirect'] = 0
                response['code'] = 1
                today = timezone.now()
                duration = today + datetime.timedelta(days=30)
                voucher, created = Voucher.objects.get_or_create(code="WELCOME10")
                voucher.valid_to = duration
                voucher.discount=0.1

                email_template = get_template("mainapp/signup_email.html")
                contact_email = user.email
                subject, from_email, to = (
                "Verify Email - Golden Shoe",
                "saifportfolioprojects@gmail.com",
                contact_email,   
                )
                e = {
                    "voucher":voucher.code,
                    "message": "Welcome to Golden Shoe!",
                }
                email_content = email_template.render(e)
                email = EmailMessage(subject, email_content, from_email, [to])
                email.content_subtype = "html"
                try:
                    email.send()
                    voucher.save()
                    customer.save()
                except Exception as e:
                    print(e)
            else:
                response['form_errors'] = form.errors
                response['redirect'] = 0
                response['code'] = 0
        else:
            response['response'] = 'Something went Wrong! Please try again later.'
            response['redirect'] = 0
            response['code'] = 0
        return JsonResponse(response, safe=False)

@api_view(['POST'])
def review(request):
    response = {}
    if request.method == 'POST':
        catalogue_code = request.data.get('code')
        rating = request.data.get('rating')
        review_text = request.data.get('review')
        customer = request.user.customer 
        shoe = Shoe.objects.get(catalogue_code=catalogue_code)
        review = Review.objects.create(customer=customer, shoe=shoe, rating=rating, description=review_text)
        try:
            review.save()
        except Exception as e:
            print(e)
        response['code'] = 1
    else:
        response['code'] = 0
    return JsonResponse(response, safe=False)



@api_view(["GET"])
def faq(request):
    response = {}
    response["basket"] = basket_content(request, request.data)
    response["form"] = ContactForm()
    return render(request, "mainapp/FAQ.html", response)


@api_view(["POST"])
def contact(request):
    response = {}
    form = ContactForm(data=request.POST)
    if form.is_valid():
        email_template = get_template("mainapp/contact_template.txt")
        contact_name = form.cleaned_data.get("contact_name")
        contact_email = form.cleaned_data.get("contact_email")
        contact_number = form.cleaned_data.get("contact_number")
        contact_content = form.cleaned_data.get("contact_content")
        subject, from_email, to = (
            "New Contact Received! - Golden Shoe",
            "contact_email",
            "saifportfolioprojects@gmail.com",
        )
        e = {
            "contact_name": contact_name,
            "contact_email": contact_email,
            "contact_number": contact_number,
            "contact_content": contact_content,
        }
        email_content = email_template.render(e)
        email = EmailMessage(subject, email_content, from_email, [to])
        try:
            email.send()
        except Exception as e:
            response["message"] = "ERROR Something went Wrong! Please Try again later! "
            response["code"] = 0
            print(e)
        response["message"] = "Contact Sent Successfully!"
        response["code"] = 1
    else:
        response["message"] = form.errors
        response["code"] = 0
    return JsonResponse(response, safe=False)

def redirect_index(request):
    return HttpResponseRedirect('/')

def logout_view(request):
    logout(request)
    return redirect_index(request)