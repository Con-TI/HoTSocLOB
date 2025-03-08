from django.shortcuts import render
from ..orderbook import OrderBook
from ..pricedata import PriceData
from ..userstats import UserStats

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
        pass
        
def sell_order(request):
    if request.method == 'GET':
        pass