if __name__=='__main__':
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    # Added this to fix the environment variable being set up only after service.models is called
    django.setup()
        
from django.db.models import Q
from models.models import Orders, PriceHistory

class PriceData():
    def summarize_orderbook(self):
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

# TODO: Test out this class
if __name__ == "__main__":
    print(len(PriceHistory.objects.filter()))