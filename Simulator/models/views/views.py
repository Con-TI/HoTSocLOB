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

def get_user_stats(request):
    try:
        username = request.GET.get('user')
        user = Users.objects.get(user=username)
        equity = user.equity
        pnl = UserStats.calc_pnl(user)
        unreal_pnl = UserStats.calc_unreal_pnl(user,PriceData.fetch_midprice())
        pending_orders = UserStats.fetch_pending_orders(user)
        return JsonResponse({
            'equity':equity,
            'pnl':pnl,
            'unreal_pnl':unreal_pnl,
            'pending_orders':pending_orders
        })
    except:
        return JsonResponse({
            'message':'error'
        })

def check_for_bankruptcy(request):
    try:
        username = request.GET.get('user')
        user = Users.objects.get(user=username)
        equity = user.equity
        unreal_pnl = UserStats.calc_unreal_pnl(user,PriceData.fetch_midprice())
        if equity + unreal_pnl < 0:
            user.equity = 0
            user.save(update_fields=['equity'])
            orders = OrderBook.objects.filter(user=user)
            for order in orders:
                order.delete()
            return JsonResponse({'message':'bankrupt'})
    except:
        return JsonResponse({'message':'not bankrupt'})
        
def delete_user(request):
    try: 
        username = request.GET.get('user')
        user = Users.objects.get(user=username)
        user.delete()
        return  JsonResponse({
                'message': 'success'
            })
    except:
        return JsonResponse({
            'message': 'error'
        })

        