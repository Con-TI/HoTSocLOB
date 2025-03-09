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
        self.market_conditions = {'spread':None,'midprice':None,'TWAP':None, 'VWAP':None, 'sigma':None}
        
    def _fetch_mid(self):
        u = PriceData()
        self.market_conditions['midprice'] =  u.fetch_midprice()
    
    def _calc_spread(self):
        u = PriceData()
        self.market_conditions['spread'] = u.fetch_spread()
        