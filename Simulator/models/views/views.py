from django.shortcuts import render
from ..orderbook import OrderBook
from ..pricedata import PriceData
from ..userstats import UserStats
from django.http import JsonResponse
from models.models import Users

# GUI Views.
# Login will serve as both a login page and a registration page. 
# If the user inputs new details, they make a new account.
# If the user inputs existing details, they login to their account
# If the user inputs an existing user but incorrect password, generate an alert
def login(request):
    return render(request, 'login.html')

def index(request):
    return render(request,'index.html')

# Functions.
def buy_order(request):
    if request.method == 'GET':
        price = request.GET.get('price')
        quantity = request.GET.get('quantity')
        user = request.GET.get('user')
        try:
            u = Users.objects.get(name=user)
            OrderBook.add_buy_order(user=u,price=price,quantity=quantity)
            OrderBook.match_orders()
            return  JsonResponse({
                'message': 'success'
            })
        except:
            return JsonResponse({
                'message': 'error'
            })

def sell_order(request):
    if request.method == 'GET':
        price = request.GET.get('price')
        quantity = request.GET.get('quantity')
        user = request.GET.get('user')
        try:
            u = Users.objects.get(name=user)
            OrderBook.add_sell_order(user=u,price=price,quantity=quantity)
            OrderBook.match_orders()
            return  JsonResponse({
                'message': 'success'
            })
        except:
            return JsonResponse({
                'message': 'error'
            })

def get_user_balance(request):
    pass