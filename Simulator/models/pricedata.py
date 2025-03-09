if __name__=='__main__':
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    # Added this to fix the environment variable being set up only after service.models is called
    django.setup()
        
from django.db.models import Q
from models.models import Orders, PriceHistory
from numpy import std, mean

class PriceData():
    def summarize_orderbook(self):
        # Note call the function to match all prevailing orders first before calling this
        unique_prices = Orders.objects.values('price').distinct()
        bids = []
        asks = []
        for price in unique_prices:
            qb = 0
            buy_orders = Orders.objects.filter(Q(quantity__gt=0), price = price['price'])
            if buy_orders:
                for order in buy_orders:
                    qb += order.quantity
                bids.append({'price':price['price'],'quantity':qb}) 
            
            qs = 0
            sell_orders = Orders.objects.filter(Q(quantity__lt=0), price = price['price'])
            if sell_orders:
                for order in sell_orders:
                    qs += abs(order.quantity)
                asks.append({'price':price['price'],'quantity':qs}) 
        return {'bids':bids,'asks':asks}
    
    def fetch_midprice(self):
        lob = self.summarize_orderbook()
        bids = lob['bids']
        best_bid = max([level['price'] for level in bids])
        asks = lob['asks']
        best_ask = min([level['price'] for level in asks])
        return (best_bid+best_ask)/2

    def fetch_spread(self):
        lob = self.summarize_orderbook()
        bids = lob['bids']
        best_bid = max([level['price'] for level in bids])
        asks = lob['asks']
        best_ask = min([level['price'] for level in asks])
        abs_spread = best_bid - best_ask
        return (abs_spread, (abs_spread/best_ask)*100)
    
    def fetch_top_ask_vol(self, lob):
        asks = lob['asks']
        best_ask_price = min([level['price'] for level in asks])
        best_ask_vol = [ask['quantity'] for ask in asks if ask['price'] == best_ask_price][0]
        return best_ask_vol
    
    def fetch_top_bid_vol(self, lob):
        bids = lob['bids']
        best_bid_price = max([level['price'] for level in bids])
        best_bid_vol = [bid['quantity'] for bid in bids if bid['price'] == best_bid_price][0]
        return best_bid_vol
    
    def fetch_top_ask_price(self):
        lob = self.summarize_orderbook() 
        asks = lob['asks']
        best_ask_price = min([level['price'] for level in asks])
        return best_ask_price    
        
    def fetch_top_bid_price(self):
        lob = self.summarize_orderbook() 
        bids = lob['bids']
        best_bid_price = max([level['price'] for level in bids])
        return best_bid_price
    
    def fetch_microprice(self):
        lob = self.summarize_orderbook()        
        bids = lob['bids']
        asks = lob['asks']
        best_bid_vol = self.fetch_top_bid_vol(lob=lob)
        best_ask_vol = self.fetch_top_ask_vol(lob=lob)
        best_bid = max([level['price'] for level in bids])
        best_ask = min([level['price'] for level in asks])

        microprice = (best_ask*best_bid_vol+best_bid*best_ask_vol)/(best_bid_vol+best_ask_vol)
        return microprice

    def update_price_history(self):
        current_midprice = self.fetch_midprice()
        PriceHistory.objects.create(
            price = current_midprice
        )
        if PriceHistory.objects.count() > 100:
            oldest_entry = PriceHistory.objects.earliest('created_time')
            oldest_entry.delete()

    def prices_for_plot(self):
        self.update_price_history()
        prices = PriceHistory.objects.filter().order_by('created_time')
        prices = [p.price for p in prices]
        return prices
    
    def price_vol(self):
        price_list = self.prices_for_plot()
        return std(price_list)
    
    def price_mean(self):
        price_list = self.prices_for_plot()
        return mean(price_list)

# TODO: Test out this class
if __name__ == "__main__":
    print(len(PriceHistory.objects.filter()))