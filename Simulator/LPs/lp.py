if __name__ == '__main__':
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    # Added this to fix the environment variable being set up only after service.models is called
    django.setup()

from models.orderbook import OrderBook
from models.pricedata import PriceData
from models.userstats import UserStats
from models.models import Positions, Orders, Users
import numpy as np
import scipy.stats as stats


class LP():
    def __init__(self, username = 'whaleLP'):
        self.username = username
        self.user = Users.objects.get(name=self.username)
        self.positions = None
        self.pending_orders = None
        self.pending_bids_summary = None
        self.pending_asks_summary = None
        self.memory = []
        self.poi_params = None
        self.m1 = 0.01
        self.m2 = 0.05
        self.order_ratio = None
        
        # Stores the current market spread, midprice, TWAP, VWAP, and volatility (sigma)
        self.market_conditions = {'spread':None,'midprice':None, 'microprice':None, 'sigma_norm':None, 'best_ask':None, 'best_bid':None}

    def initialize(self):
        self._update_market_conditions()
        self._fetch_inventory_and_pending_orders()
        self._derive_order_ratio()
        self._poi_param()
        self._create_summary_distributions()
        self._quotes_reset()        
    
    def update_all(self):
        self._update_market_conditions()
        self._fetch_inventory_and_pending_orders()
        self._derive_order_ratio()
        self._poi_param()
        self._create_summary_distributions()
        self._order_distribution_shift()
        self._update_pending()

    def _update_market_conditions(self):
        # Fetches current market conditions
        self.memory.append(self.market_conditions)
        if len(self.memory)>10:
            self.memory.pop(0)
        
        # Interacting with DB
        u = PriceData()
        self.market_conditions['midprice'] =  u.fetch_midprice()
        self.market_conditions['microprice'] = u.fetch_microprice()
        self.market_conditions['spread'] = u.fetch_spread()
        self.market_conditions['best_ask'] = u.fetch_top_ask_price()
        self.market_conditions['best_bid'] =  u.fetch_top_bid_price()
        
        # Updating rel_vol
        self._find_rel_volatility()
        
    def _derive_order_ratio(self):
        # Calculates order ratio based off of microprice and spread
        micro_minus_bid = self.market_conditions['microprice']-self.market_conditions['best_bid']
        numeric_spread = self.market_conditions['spread']
        if numeric_spread == 0:
            numeric_spread = 1
        bid_order_num = min(max(int(micro_minus_bid/numeric_spread*100),30),70)
        ask_order_num = 100 - bid_order_num
        self.order_ratio = {"bids": bid_order_num, "asks": ask_order_num}
    
    def _fetch_inventory_and_pending_orders(self):
        # Fetches inventory and pending orders of the LP
        stats = UserStats()
        pending_orders = stats.fetch_pending_orders(self.user)
        self.pending_orders = [{'price':order.price,'quantity':order.quantity} for order in pending_orders]
        positions = stats.fetch_positions(self.user)
        self.positions = [{'price':order.price,'quantity':order.quantity} for order in positions]
        
    def _create_summary_distributions(self):
        # Takes pending orders and creates an empirical frequency distribution of bids and asks
        pending_orders = self.pending_orders
        pending_bids = [order for order in pending_orders if order['quantity']>0]
        pending_bid_prices = list(set([order['price'] for order in pending_bids]))
        pending_bid_summary = []
        for price in pending_bid_prices:
            bid_vol = sum([order['quantity'] for order in pending_bids if order['price']==price])
            pending_bid_summary.append({'price':price, 'quantity':bid_vol})
        self.pending_bids_summary = pending_bid_summary
            
        pending_asks = [order for order in pending_orders if order['quantity']<0]
        pending_ask_prices = list(set([order['price'] for order in pending_asks]))
        pending_ask_summary = []
        for price in pending_ask_prices:
            ask_vol = sum([order['quantity'] for order in pending_asks if order['price']==price])
            pending_bid_summary.append({'price':price, 'quantity':ask_vol})
        self.pending_asks_summary = pending_ask_summary

    def _find_rel_volatility(self):
        # Calculates relative volatility
        u = PriceData()
        vol = u.price_vol()
        mu = u.price_mean()
        try:
            self.market_conditions['sigma_norm'] = vol/mu
        except:
            self.market_conditions['sigma_norm'] = 0
            
    def _poi_param(self):
        # Calculates the poisson parameter given orderbook imbalance
        order_ratio = self.order_ratio
        leaky_relu = lambda x : self.m1*(50-x)+1 if x>=50 else self.m2*(10-x)+3
        self.poi_params = {'bid':leaky_relu(order_ratio['bids']),'ask':leaky_relu(order_ratio['asks'])}
        
    def _order_distribution_shift(self):
        # Calculates the distribution shift we apply (adjusts spread)
        rel_vol = self.market_conditions['sigma_norm']
        
        if abs(rel_vol)>0.1:
            return 2
        return 1
    
    def _bid_generator(self):
        # Generates orders based on order ratio and poisson distribution
        order_ratio = self.order_ratio
        steps_from_mid = np.random.poisson(self.poi_params['bid'],order_ratio['bids']) + self._order_distribution_shift()
        bid_array = self.market_conditions['midprice']-steps_from_mid
        bid_array = bid_array[bid_array>0]
        bid_prices = np.unique(bid_array)
        bid_orders = [{'price':price,'quantity':len(bid_array[bid_array==price])} for price in bid_prices]
        return bid_orders

    def _ask_generator(self):
        # Generates orders based on order ratio and poisson distribution
        order_ratio = self.order_ratio
        steps_from_mid = np.random.poisson(self.poi_params['ask'],order_ratio['asks']) + self._order_distribution_shift()
        ask_array = self.market_conditions['midprice']+steps_from_mid
        ask_prices = np.unique(ask_array)
        ask_orders = [{'price':price,'quantity':-len(ask_array[ask_array==price])} for price in ask_prices]
        return ask_orders
    
    def _quotes_reset(self):
        # Clear all orders
        self._clear_pending()
        # Bulk fills when we have no orders
        bid_orders = self._bid_generator()
        ask_orders = self._ask_generator()
        bid_objects = [Orders(price=order['price'], quantity=order['quantity'], user=self.user,) for order in bid_orders]
        ask_objects = [Orders(price=order['price'], quantity=order['quantity'], user=self.user,) for order in ask_orders]
        order_objects = bid_objects + ask_objects
        Orders.objects.bulk_create(order_objects)
        book = OrderBook()
        try:
            book.match_orders()
        except:
            pass
    
    def _clear_pending(self):
        # Clear all pending orders
        Orders.objects.filter(user=self.user).delete()

    def _update_pending(self):
        pending_bids = self.pending_bids_summary
        pending_bids_total = sum([order['quantity'] for order in pending_bids])
        desired_bids = self._bid_generator()
        desired_bid_prices = [order['price'] for order in desired_bids]
        diff = 0
        for order in pending_bids:
            p = order['price']
            if p in desired_bid_prices:
                desired_order = [order for order in desired_bids if order['price'] == p][0]
                quantity_difference = abs(desired_order['quantity']-order['quantity'])
                diff += quantity_difference
            else:
                diff += order['quantity']
                
        pending_asks = self.pending_asks_summary
        pending_ask_total = sum([order['quantity'] for order in pending_asks])
        desired_asks = self._bid_generator()
        desired_ask_prices = [order['price'] for order in desired_asks]
        for order in pending_asks:
            p = order['price']
            if p in desired_ask_prices:
                desired_order = [order for order in desired_asks if order['price'] == p][0]
                quantity_difference = abs(desired_order['quantity']-order['quantity'])
                diff += quantity_difference
            else:
                diff += order['quantity']
        if diff >= 20 or (pending_ask_total+pending_bids_total)<70:
            self._quotes_reset()

from datetime import datetime
import pandas as pd
import math

class trend_setter(LP):
    def __init__(self):
        super().__init__(username="whaleLP2")

    def _update_market_conditions(self):
        # Fetches current market conditions
        self.memory.append(self.market_conditions)
        if len(self.memory)>10:
            self.memory.pop(0)
        
        
        # Interacting with DB
        u = PriceData()
        self.market_conditions['midprice'] =  self.trend_midprice()
        self.market_conditions['microprice'] = self.market_conditions['midprice']
        self.market_conditions['spread'] = u.fetch_spread()
        self.market_conditions['best_ask'] = u.fetch_top_ask_price()
        self.market_conditions['best_bid'] =  u.fetch_top_bid_price()
        
        # Updating rel_vol
        self._find_rel_volatility()

    def trend_midprice(self):
        qanda = pd.read_csv('models/views/QandA.csv')
        p = PriceData()
        true_mid = p.fetch_midprice() 

        time_now = datetime.now()
        init_time = datetime(2025, 3, 10, 14, 00, 0)
        elapsed_time = time_now - init_time
        elapsed_time = elapsed_time.total_seconds()
        elapsed_time = elapsed_time/3600
        interval = 4
        index = math.floor(elapsed_time/interval)

        if (elapsed_time%interval)>=(interval/2):
            ans = qanda['Answer'].to_list()
            ans = ans[index%len(ans)]
            return ans
        elif (elapsed_time%interval)>=(interval/4):
            ans = qanda['Answer'].to_list()
            ans_old = ans[index%len(ans)-1]
            ans_new = ans[index%len(ans)]
            ans_dif = ans_new-ans_old

            price = lambda x: ans_dif*x + ans_old

            return price(elapsed_time%interval-interval/4) + np.random.randint(int(-(true_mid*0.05)), int(true_mid*0.05)+1)
        
        return true_mid + np.random.randint(int(-true_mid*0.05), int(true_mid*0.05)+1)
    
if __name__ == '__main__':
    #l = BlockLP()
    # reverting
    #l._clear_pending()
    pass
    # for u in Users.objects.filter():
    #     u.delete()
    
    # user = Users.objects.get(name='test1')
    # Orders.objects.create(user=user,price=95,quantity=10)
    # user = Users.objects.get(name='test2')
    # Orders.objects.create(user=user,price=105,quantity=-10)
    
    # user = Users.objects.get(name='whaleLP')
    # orders = Orders.objects.filter(user= user)
    # for order in orders:
    #     print(order.price, order.quantity)