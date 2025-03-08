from django.db.models import Q
from models.models import Orders

class PriceData():
    def summarize_orderbook():
        # Note call the function to match all prevailing orders first before calling this
        unique_prices = Orders.objects.values('price').distinct()
        bids = {}
        asks = {}
        for price in unique_prices:
            qb = 0
            buy_orders = Orders.objects.filter(Q(quantity__gt=0), price = price['price'])
            for order in buy_orders:
                qb += order.quantity
            bids[price['price']] = qb
            
            qs = 0
            sell_orders = Orders.objects.filter(Q(quantity__lt=0), price = price['price'])
            for order in sell_orders:
                qs += abs(order.quantity)
            asks[price['price']] = qs
        return {'bids':bids,'asks':asks}
    
    def fetch_midprice(self):
        lob = self.summarize_orderbook()
        bids = lob['bids']
        best_bid = max([price for price in bids])
        asks = lob['asks']
        best_ask = min([price for price in asks])
        return (best_bid+best_ask)/2

# TODO: Test out this class