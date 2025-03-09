from ..models.orderbook import OrderBook
from ..models.pricedata import PriceData
from ..models.userstats import UserStats
from ..models.models import Positions, Orders, Users

class LP():
    def __init__(self, username = 'LP1'):
        self.username = username
        self.user = Users.objects.get(name=self.username)
        self.positions = None
        self.pending_orders = None
        self.pending_bids_summary = None
        self.pending_asks_summary = None
        self.memory = None
        
        # Stores the current market spread, midprice, TWAP, VWAP, and volatility (sigma)
        self.market_conditions = {'spread':None,'midprice':None, 'microprice':None, 'sigma-norm':None, 'best_ask':None, 'best_bid':None}
        
        self.update_market_conditions()
        
    def update_market_conditions(self):
        self.memory = self.market_conditions
        u = PriceData()
        self.market_conditions['midprice'] =  u.fetch_midprice()
        self.market_conditions['microprice'] = u.fetch_microprice()
        self.market_conditions['spread'] = u.fetch_spread()
        self.market_conditions['best_ask'] = u.fetch_top_ask_price()
        self.market_conditions['best_bid'] =  u.fetch_top_bid_price()
        
    def _derive_order_ratio(self):
        micro_minus_bid = self.market_conditions['microprice']-self.market_conditions['best_bid']
        numeric_spread = self.market_conditions['spread']
        bid_order_num = int(micro_minus_bid/numeric_spread*100)
        ask_order_num = 100 - bid_order_num
        return {"bids": bid_order_num, "asks": ask_order_num}
    
    def _fetch_inventory_and_pending_orders(self):
        stats = UserStats()
        pending_orders = stats.fetch_pending_orders(self.user)
        self.pending_orders = [{'price':order.price,'quantity':order.quantity} for order in pending_orders]
        positions = stats.fetch_positions(self.user)
        self.positions = [{'price':order.price,'quantity':order.quantity} for order in positions]
        
    def _create_summary_distributions(self):
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
        u = PriceData()
        vol = u.price_vol()
        mu = u.price_mean()
        try:
            self.market_conditions['sigma_norm'] = vol/mu
        except:
            self.market_conditions['sigma_norm'] = 0

    def _order_distribution_shift(self):
        self._find_rel_volatility()
        rel_vol = self.market_conditions['sigma_norm']

        if abs(rel_vol)>0.1:
            return 2
        return 1