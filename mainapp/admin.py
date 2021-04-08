from django.contrib import admin
from .models import User, Shoe, Size, Customer, Order, OrderItem, Shipping, Voucher, Review
# Register your models here.
admin.site.register(User)
admin.site.register(Shoe)
admin.site.register(Size)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Shipping)
admin.site.register(Voucher)
admin.site.register(Review)