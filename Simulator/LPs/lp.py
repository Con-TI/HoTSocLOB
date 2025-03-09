class LP():
    def __init__(self, user = 'LP1'):
        self.user = user
        self.inventory = None
        self.pending_orders = None
        self.memory = None
        
        # Stores the current market spread, midprice, TWAP, VWAP, and volatility (sigma)
        self.market_conditions = {'spread':None,'midprice':None,'TWAP':None, 'VWAP':None, 'sigma':None}