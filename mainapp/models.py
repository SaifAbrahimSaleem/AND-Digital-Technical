from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now
from django.db import models
from datetime import date
import numpy as np
import random
import string
import datetime

def upload_media(instance, filename):
    return 'product_uploads/{0}/{1}'.format(instance.catalogue_code, filename)

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username")
        if not password:
            raise ValueError("User must have a password")
        user = self.model(email = self.normalize_email(email), username = username)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, username, password):
        superuser = self.create_user(email = self.normalize_email(email), username=username, password=password)
        superuser.is_admin = True
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save(using = self._db)

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name = 'email', max_length = 60, unique = True)
    username = models.CharField(max_length = 30, unique = True)
    date_joined = models.DateTimeField(verbose_name = 'Date Joined', auto_now_add = True)
    last_login = models.DateTimeField(verbose_name = 'Last Login', auto_now_add = True)
    is_admin = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 50)
    address = models.CharField(max_length=150)
    postcode = models.CharField(max_length=10)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','password']
    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class Size(models.Model):
    size = models.DecimalField(max_digits=3, decimal_places=1, primary_key=True)
# Implement quantity
    def __str__(self):
        return '{}'.format(self.size)

class Shoe(models.Model):
    # Shoe gender sizes
    MALE = 'M'
    FEMALE =  'F'
    UNISEX = 'U' 
    SHOE_GENDER_CHOICES = {
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (UNISEX, 'Unisex')
    }
    # Shoe category choices
    SPORT = 'S'
    CASUAL = 'C'
    EVENING_WEAR = 'E'
    SLIPPERS = 'SL'
    SANDALS = 'SA'
    PUMPS = 'P'
    HIGH_HEELS = 'H'
    SHOE_CATEGORY_CHOICES = {
        (SPORT, 'Sport'),
        (CASUAL, 'Casual'),
        (EVENING_WEAR, 'Evening Wear'),
        (SLIPPERS, 'Slippers'),
        (SANDALS, 'Sandals'),
        (PUMPS, 'Pumps'),
        (HIGH_HEELS, 'Highheels')        
    }
    catalogue_code = models.CharField(max_length=50, blank=True, unique=True) 
    name = models.CharField(max_length=50, unique=True)
    quantity = models.IntegerField(default=1)
    collection = models.CharField(max_length=50)
    gender_category = models.CharField(max_length=20, choices = SHOE_GENDER_CHOICES)
    shoe_category  = models.CharField(max_length=20, choices = SHOE_CATEGORY_CHOICES)
    sizes = models.ManyToManyField(Size, help_text='Shoe Sizes of the product currently offered')
    colour = models.CharField(max_length=30, default='Unregistered')
    materials = models.CharField(max_length=50, default='Unregistered')
    description = models.TextField(max_length=800, default='Unregistered')
    date_added = models.DateField(auto_now_add=True)
    shoe_image = models.ImageField(upload_to=upload_media, default='DefaultEmptyImage.png')
    price = models.DecimalField(max_digits=5, decimal_places=2, default="0.00",blank=True)
    
    def __str__(self):
        return self.name + '(' + self.catalogue_code + ')'
    
    def average_rating(self):
        all_review_ratings = all_ratings = map(lambda x: x.rating, self.review_set.all())
        return np.mean(all_ratings)

    def save(self, **kwargs):
        length = 7
        while True:
            if Shoe.objects.filter(catalogue_code=self.catalogue_code).exists():
                break
            numeric_code = map(str, random.choices(range(0,9), k=length))
            string_code = ''.join(numeric_code)
            self.catalogue_code = self.collection[:3].upper()+ "-" + string_code
            if Shoe.objects.filter(catalogue_code = self.catalogue_code).count() == 0:
                break
        super(Shoe, self).save(**kwargs)

class Customer(models.Model):
    customer_id = models.CharField(max_length=20, blank=True, unique=True)
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default='AnonymousUser', null=True)
    email = models.CharField(max_length=200, default='AnonymousUser',null=True)

    def __str__(self):
        return self.customer_id
    
    def save(self, **kwargs):
        length = 6
        while True:
            if Customer.objects.filter(customer_id=self.customer_id).exists():
                break
            numeric_code = map(str, random.choices(range(0,9), k=length))
            string_code = ''.join(numeric_code)
            self.customer_id = "CUST-" + string_code
            if Customer.objects.filter(customer_id = self.customer_id).count() == 0:
                break
        super(Customer, self).save(**kwargs)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length = 50, null=True)

    def __str__(self):
        return str(self.transaction_id)
    
    @property
    def get_basket_total(self):
        order_items = self.orderitem_set.all()
        basket_total = sum([item.get_order_total for item in order_items])
        return basket_total
    
    @property
    def get_basket_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total
    
    @property
    def get_order_shipping_addresses(self):
        shipping = self.shipping_set.all()
        shipping_addresses = [x for x in shipping]
        return shipping_addresses
    
    def save(self, **kwargs):
        length = 8
        while True:
            if Order.objects.filter(transaction_id=self.transaction_id).exists():
                break
            numeric_code = map(str, random.choices(range(0,9), k=length))
            string_code = ''.join(numeric_code)
            self.transaction_id = "GS-" + string_code
            if Order.objects.filter(transaction_id = self.transaction_id).count() == 0:
                break
        super(Order, self).save(**kwargs) 

class OrderItem(models.Model):
    shoe = models.ForeignKey(Shoe, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    size = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shoe.name

    @property
    def get_order_total(self):
        total = self.shoe.price * self.quantity
        return total

class Shipping(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    postcode = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.address

class Voucher(models.Model):
    code = models.CharField(max_length=20, null=True)
    valid_from=models.DateTimeField(auto_now_add=True)
    valid_to=models.DateTimeField(auto_now_add=False, null=True, blank=True)
    discount=models.DecimalField(max_digits=5, decimal_places=2, default=0.00, validators=[MinValueValidator(0), MaxValueValidator(50)])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

class Review(models.Model):
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.CASCADE)
    shoe = models.ForeignKey(Shoe, blank=True, null=True, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, blank=True, null=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)