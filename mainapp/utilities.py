from email.mime.image import MIMEImage
from functools import lru_cache
from .models import *
from decimal import *
from .serializers import ShoeSearchSerializer
import json, random, string, datetime
# Decimal Encoder (Extending the JSONEncoder class) for decimal numbers since Json dumps will throw the error "Object of type Decimal is not JSON serializable" 
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

def basket_cookies(request):
    try:
        basket = json.loads(request.COOKIES["basket"])
        basket_items = basket["order"]["basket_items"]
        order = basket["order"]
        items = basket["items"]
    except Exception as e:
        order = {"basket_total":float(0), "basket_items":0}
        items = []
        basket = {"order":order, "items":items}
    c_items = []
    order["basket_items"]=0
    order["basket_total"] = 0
    for item in items:
        try:
            # Check for items already in the basket
            shoe_code = item["code"]
            item_quantity = int(item["shoe"]["quantity"])
            shoe = Shoe.objects.get(catalogue_code = shoe_code)
            total_price = shoe.price * item_quantity
            order["basket_total"] += float(total_price)
            order["basket_items"] += item_quantity
            item_ = {
                "code":shoe.catalogue_code,
                "shoe":{
                    "id":shoe.id, 
                    "size": str(item["shoe"]["size"]),
                    "name":shoe.name, 
                    "collection":shoe.collection,
                    "price":float(shoe.price),
                    "image":str(shoe.shoe_image),
                    "quantity": item["shoe"]["quantity"],
                    "stock":shoe.quantity
                },
                "total": "{:.2f}".format(total_price)
            }
            c_items.append(item_)
        except Exception as e:
            print("ERROR", e)
            pass
    order["basket_total"] = "{:.2f}".format(order["basket_total"])
    return json.dumps({"order":order, "items":c_items}, cls=DecimalEncoder)

def basket_content(request, data):
    basket = {}
    cookies = json.loads(basket_cookies(request))
    basket["order"] = cookies["order"]
    basket["items"] = cookies["items"]
    return json.dumps(basket, cls=DecimalEncoder)


def ProcessOrder(request, data):
    """
     LOGIC: 
        Check if data contains form data (indicating that the user wishes to checkout):
            if data contains form data:
                - set name and email with form data and save customer
            if data doesn"t contain form data:
                - create new customer object and use customer id
        Check for customer object first to avoid creating duplicates
    """
    cookies = json.loads(basket_cookies(request))
    items = cookies["items"]
    if request.user.is_authenticated:
      customer, created = Customer.objects.get_or_create(user=request.user)
      name=customer.name
      email=customer.email
    else:
      name = data["name"]
      email = data["email"]
      customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    try:
      customer.save()
    except Exception as e:
      print(e)
    order = Order.objects.create(customer=customer, completed=False)
    for item in items:
      shoe = Shoe.objects.get(catalogue_code=item["code"])
      order_item = OrderItem.objects.create(shoe=shoe, order=order, size=item["shoe"]["size"], quantity=(item["shoe"]["quantity"] if item["shoe"]["quantity"] > 0 else -1 * item["shoe"]["quantity"]))
    return customer, order

def get_basket(request):
    response = {}
    if request.method == "GET":
        basket = basket_content(request)
        response["basket"] = basket
        return response
    else:
        response["Error"] = "Request method is invalid"
        return response

def sort_shoes(shoes):
  prices = sorted(shoe.price for shoe in shoes)
  return sorted(shoes, key=lambda x:prices.index(x.price))

def mens():
  return "M"

def womens():
  return "F"

def unisex():
  return "U"

def sport(gc = None):
  if gc == "mens":
    return ["M", "S"]
  elif gc == "womens":
    return ["F", "S"]
  else:
    return ["U", "S"]
  return "S"

def casual(gc = None):
  if gc == "mens":
    return ["M", "C"]
  elif gc == "womens":
    return ["F", "C"]
  else:
    return ["U", "C"]
  return "C"

def evening_wear(gc = None):
  if gc == "mens":
    return ["M", "E"]
  elif gc == "womens":
    return ["F", "E"]
  else:
    return ["U", "E"]
  return "E"

def slippers(gc = None):
  if gc == "mens":
    return ["M", "SL"]
  elif gc == "womens":
    return ["F", "SL"]
  else:
    return ["U", "SL"]
  return "SL"

def sandals(gc = None):
  if gc == "mens":
    return ["M", "SA"]
  elif gc == "womens":
    return ["F", "SA"]
  else:
    return ["U", "SA"]
  return "SA"

def pumps(gc = None):
  if gc == "mens":
    return ["M", "P"]
  elif gc == "womens":
    return ["F", "P"]
  else:
    return ["U", "P"]
  return "P"

def high_heels(gc = None):
  if gc == "mens":
    return ["M", "H"]
  elif gc == "womens":
    return ["F", "H"]
  else:
    return ["U", "H"]
  return "H"

def convert_to_label(category):
  switch = {
    "M":"MENS",
    "F": "WOMENS",
    "U": "UNISEX",
    "S": " SPORT",
    "C": " CASUAL",
    "E": " EVENING WEAR",
    "SL": " SLIPPERS",
    "SA": " SANDALS",
    "P": " PUMPS",
    "H": " HIGH HEELS"
  }
  if type(category) is list:
    gender = switch.get(category[0])
    category = switch.get(category[1])
    return [gender, category]
  else:
    return switch.get(category[0])

def get_shoes_from_category(argument):
    category = ""
    gender_categories = ["M","F","U"]
    shoe_categories = ["S","C","E","SL","SA","P","H"]
    switch = {
        "mens":mens,
        "womens":womens,
        "unisex":unisex,
        "sport": sport,
        "casual": casual,
        "evening-wear": evening_wear,
        "slippers": slippers,
        "sandals": sandals,
        "pumps": pumps,
        "high-heels": high_heels,
        "mens-sport": sport("mens"),
        "mens-casual": casual("mens"),
        "mens-evening-wear": evening_wear("mens"),
        "mens-slippers": slippers("mens"),
        "mens-sandals": sandals("mens"),
        "mens-pumps": pumps("mens"),
        "mens-high-heels": high_heels("mens"),
        "womens-sport": sport("womens"),
        "womens-casual": casual("womens"),
        "womens-evening-wear": evening_wear("womens"),
        "womens-slippers": slippers("womens"),
        "womens-sandals": sandals("womens"),
        "womens-pumps": pumps("womens"),
        "womens-high-heels": high_heels("womens"),
        "unisex-sport": sport("unisex"),
        "unisex-casual": casual("unisex"),
        "unisex-evening-wear": evening_wear("unisex"),
        "unisex-slippers": slippers("unisex"),
        "unisex-sandals": sandals("unisex"),
        "unisex-pumps": pumps("unisex"),
        "unisex-high-heels": high_heels("unisex"),
    }
    func = switch.get(argument, lambda:"invalid key")
    if type(func) is list:
        return Shoe.objects.filter(gender_category=func[0], shoe_category=func[1]), convert_to_label(func)
    else:
        if func() in gender_categories:
            return Shoe.objects.filter(gender_category=func()), convert_to_label(func())
        elif func() in shoe_categories:
            return Shoe.objects.filter(shoe_category=func()), convert_to_label(func())
        else:
            print("THROW A SHOE FILTER ERROR")


def get_gender_categories(category):
  if type(category) is list:
    category = category[0]
  if category == "MENS":
      return ["WOMENS", "UNISEX"] 
  elif category == "WOMENS":
      return ["MENS", "UNISEX"] 
  elif category == "UNISEX":
      return ["MENS", "WOMENS"]
  else:
    return ["MENS", "WOMENS", "UNISEX"]
