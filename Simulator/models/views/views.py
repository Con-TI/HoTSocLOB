from django.shortcuts import render
from ..orderbook import OrderBook
from ..pricedata import PriceData
from ..userstats import UserStats
from django.http import JsonResponse
from models.models import Users
from ..users import Add_User, Check_Login
import pandas as pd
from datetime import datetime
import math
from LPs.lp import LP

# GUI Views.
# Login will serve as both a login page and a registration page. 
# If the user inputs new details, they make a new account.
# If the user inputs existing details, they login to their account
# If the user inputs an existing user but incorrect password, generate an alert
def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def complete_login(request):
    #this is the one im working on to try and get login working
   user =  request.GET.get('username')
   password = request.GET.get('password')

def index(request):
    return render(request,'index.html')

# Functions.
def buy_order(request):
    if request.method == 'GET':
        price = int(request.GET.get('price'))
        quantity = int(request.GET.get('quantity'))
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
        price = int(request.GET.get('price'))
        quantity = int(request.GET.get('quantity'))
        user = request.GET.get('user')
        try:
            u = Users.objects.get(name=user)
        except:
            return JsonResponse({
                'message': 'error'
            })
        o = OrderBook()
        o.add_sell_order(user=u,price=price,quantity=quantity)
        o.match_orders()
        return  JsonResponse({
            'message': 'success'
        })

def get_user_stats(request):
    try:
        username = str(request.GET.get('user'))
        user = Users.objects.get(name=username)
        equity = int(user.equity)
        u = UserStats()
        pnl = u.calc_pnl(equity)
        p = PriceData()
        midprice = p.fetch_midprice()
        unreal_pnl = u.calc_unreal_pnl(user, midprice)
        pending_orders = u.fetch_pending_orders(user)
        pending_orders = [{'price':order.price, 'quantity':order.quantity} for order in pending_orders]
        positions = u.fetch_positions(user)
        positions = [{'price':pos.price,'quantity':pos.quantity} for pos in positions]
        return_dict = {
        'equity':equity,
        'pnl':pnl,
        'unreal_pnl':unreal_pnl,
        'pending_orders':pending_orders,
        'positions':positions}
        return JsonResponse(return_dict)
    except:
        return JsonResponse({'message':'error','equity':equity})    

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

def login_py(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        password = request.GET.get('password')
        boo = Check_Login(name, password)
        if boo:
            return JsonResponse(
                {'message':'success'}
            )
        else:
            return JsonResponse(
                {'message':'error'}
            )
        
def signup_py(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        password = request.GET.get('password')
        boo = Add_User(name, password)
        if boo:
            return JsonResponse(
                {'message':'success'}
            )
        else:
            return JsonResponse(
                {'message':'error'}
            )
            
def fetch_orderbook(request):
    if request.method == "GET":
        p = PriceData()
        orderbook = p.summarize_orderbook()
        return JsonResponse(orderbook)
    
def chart_py(request):
    now = datetime.now()
    elapsed_time = now - init_time
    elapsed_time = elapsed_time.total_seconds()
    if request.method == 'GET':
        u = PriceData()
        prices = u.prices_for_plot()
        return_dict = {"prices":prices,"labels":[i for i in range(100)]}
        return JsonResponse(return_dict)

#time of start of simulation
init_time = datetime(2025, 3, 10, 14, 00, 0) #datetime(2025, 3, 9, 20, 0, 0)
#interval in hours (for testing in seconds) between question updates
interval = 4

qanda = pd.read_csv('models/views/QandA.csv')

def questions_py(request):
    now = datetime.now()
    elapsed_time = now - init_time
    elapsed_time = elapsed_time.total_seconds()
    #converting to hours when proper
    elapsed_time = elapsed_time/3600
    index = math.floor(elapsed_time/interval)
    if request.method == 'GET':
        qs = qanda['Question'].to_list()
        ques = qs[index%len(qs)]
        q_dict = {'question':ques}
        return JsonResponse(q_dict)
    
def answers_py(request):
    now = datetime.now()
    elapsed_time = now - init_time
    elapsed_time = elapsed_time.total_seconds()
    elapsed_time = elapsed_time/3600
    time_to_ans = interval/2 - (elapsed_time%interval)
    #time_to_q = interval/2 - ((elapsed_time%interval)-2)
    time_to_ans_str = str(round(time_to_ans, 2)) + ' hours to next answer release'
    #time_to_q_str = ' '+ str(round(time_to_q, 2)) + ' hours to next question release'
    
    index = math.floor(elapsed_time/interval)
    if request.method == 'GET':
        try:
            if (elapsed_time%interval)>=(interval/2):
                ans = qanda['Answer'].to_list()
                ans = ans[index%len(ans)]
                #ans_string = ans + time_to_q_str #this is what we need to change
                ans_dict = {'answer':ans}
                return JsonResponse(ans_dict)
            return JsonResponse(
                {'answer': time_to_ans_str}
                )
        except:
            return JsonResponse(
                {'message':'error'}
            )
    
def clear_pending_orders(request):
    if request.method == "GET":
        try:
            username = request.GET.get('user')
            user = Users.objects.get(name=username)
            OrderBook.clear_pending_orders(user)
            return JsonResponse({'message':'success'})
        except:
            return JsonResponse({'message':'error'})
        
# Starting celery task
from models.tasks import update_database_task

# Trigger the background task
def my_view(request):
    update_database_task.delay()    