from ..models.orderbook import OrderBook
from ..models.pricedata import PriceData
from ..models.userstats import UserStats

class LP():
    def __init__(self, user = 'LP1'):
        self.user = user
        self.positions = None
        self.pending_orders = None
        self.memory = None
        
        # Stores the current market spread, midprice, TWAP, VWAP, and volatility (sigma)
        self.market_conditions = {'spread':None,'midprice':None, 'microprice':None, 'sigma':None, 'best_ask':None, 'best_bid':None}
        
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
    
    