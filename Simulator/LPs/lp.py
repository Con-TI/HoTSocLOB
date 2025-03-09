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

class LP():
    def __init__(self, username = 'LP'):
        self.username = username
        self.user = Users.objects.get(name=self.username)
        self.positions = None
        self.pending_orders = None
        self.pending_bids_summary = None
        self.pending_asks_summary = None
        self.memory = None
        self.poi_params = None
        self.m1 = 0.02
        self.m2 = 0.05
        self.order_ratio = None
        
        # Stores the current market spread, midprice, TWAP, VWAP, and volatility (sigma)
        self.market_conditions = {'spread':None,'midprice':None, 'microprice':None, 'sigma-norm':None, 'best_ask':None, 'best_bid':None}
        
        self.update_market_conditions()
    
    def update_all(self):
        self.update_market_conditions()
        self._fetch_inventory_and_pending_orders()
        self._derive_order_ratio()
        self._poi_param()
        self._create_summary_distributions()
    
    def update_market_conditions(self):
        # Fetches current market conditions
        self.memory = self.market_conditions
        
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
        bid_order_num = min(max(int(micro_minus_bid/numeric_spread*100),10),90)
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
        self.poi_params = {'bid':leaky_relu(order_ratio['bid']),'ask':leaky_relu(order_ratio['ask'])}
        
    def _order_distribution_shift(self):
        # Calculates the distribution shift we apply (adjusts spread)
        self._find_rel_volatility()
        rel_vol = self.market_conditions['sigma_norm']
        
        if abs(rel_vol)>0.1:
            return 2
        return 1
    
    def _bid_generator(self):
        # Generates orders based on order ratio and poisson distribution
        order_ratio = self.order_ratio
        steps_from_mid = np.random.poisson(self.poi_params['bid'],order_ratio['bids']) + self._order_distribution_shift()
        bid_array = self.market_conditions['midprice']-steps_from_mid
        bid_prices = np.unique(bid_array)
        bid_orders = [{'price':price,'quantity':len(bid_array[bid_array==price])} for price in bid_prices]
        return bid_orders

    def _ask_generator(self):
        # Generates orders based on order ratio and poisson distribution
        order_ratio = self.order_ratio
        steps_from_mid = np.random.poisson(self.poi_params['ask'],order_ratio['asks']) + self._order_distribution_shift()
        ask_array = self.market_conditions['midprice']+steps_from_mid
        ask_prices = np.unique(ask_array)
        ask_orders = [{'price':price,'quantity':len(ask_array[ask_array==price])} for price in ask_prices]
        return ask_orders
    
    def _quotes_reset(self):
        # Clear all orders
        self._clear_pending()
        # Bulk fills when we have no orders
        self._poi_param()
        self._derive_order_ratio()
        bid_orders = self._bid_generator()
        ask_orders = self._ask_generator()
        bid_objects = [Orders(price=order['price'], quantity=order['quantity'], user=self.user,) for order in bid_orders]
        ask_objects = [Orders(price=order['price'], quantity=order['quantity'], user=self.user,) for order in ask_orders]
        order_objects = bid_objects + ask_objects
        Orders.objects.bulk_create(order_objects)
    
    def _clear_pending(self):
        # Clear all pending orders
        Orders.objects.filter(user=self.user).delete()
    
        
    
if __name__ == '__main__':
    leaky_relu = lambda x : -0.02*(x-50)+1 if x>=50 else 0.05*(10-x)+3
    print(leaky_relu(30))