if __name__=='__main__':
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    # Added this to fix the environment variable being set up only after service.models is called
    django.setup()
        
from models.models import Orders, Users
from django.db.models import Q


# TODO: When using the OrderBook, we need to return an error for 0 quantity order inputs.
class OrderBook():
    @classmethod
    def match_orders(self):
        # Action: Matches overlapping buy/sell orders
        unique_prices = Orders.objects.values('price').distinct()
        for price in unique_prices:
            p = price['price']
            sell_orders = Orders.objects.filter(Q(quantity__lt=0), price=p).order_by('created_time')
            buy_orders = Orders.objects.filter(Q(quantity__gt=0), price=p).order_by('created_time')
            # If both buy and sell orders exist at a price
            if sell_orders and buy_orders:
                for sell_order in sell_orders:
                    if sell_order.pk is None:
                        continue
                    for buy_order in buy_orders:
                        if buy_order.pk is None:
                            continue
                        # Update quantities
                        trade_quantity = min(abs(sell_order.quantity), buy_order.quantity)
                        sell_order.quantity += trade_quantity
                        buy_order.quantity -= trade_quantity
                        
                        sell_order.save(update_fields=['quantity'])
                        buy_order.save(update_fields=['quantity'])
                        
                        # Update user equities
                        user_id = sell_order.user_id
                        user = Users.objects.get(id=user_id)
                        user.equity += trade_quantity * p
                        user.save(update_fields=['equity'])
                        
                        user_id = buy_order.user_id
                        user = Users.objects.get(id=user_id)
                        user.equity -= trade_quantity * p
                        user.save(update_fields=['equity'])
                        
                        # Delete order if fully filled
                        if sell_order.quantity == 0:
                            sell_order.delete()
                            break
                        if buy_order.quantity == 0:
                            buy_order.delete()                
        
            # Last filter through, seems like sometimes 0 quantity orders are left in the LOB
            orders = Orders.objects.filter(price=p)
            for order in orders:
                if order.quantity == 0:
                    order.delete()

    @classmethod
    def add_buy_order(self, user, price : int, quantity : int):
        Orders.objects.create(
            user = user,
            price = price,
            quantity = quantity,
        )
        
    @classmethod
    def add_sell_order(self, user, price : int, quantity : int):
        Orders.objects.create(
            user = user,
            price = price,
            quantity = -quantity,
        )
        
if __name__ == "__main__":
    # Clear DB
    user = Users.objects.filter()
    for u in user:
        u.delete()
    
    # Trying out the LOB
    # try: 
    #     user = Users.objects.get(name='test')
    # except:
    #     user = Users.objects.create(
    #         name = 'test',
    #         password = 'test',
    #         equity = '1000'
    #     )
    
    # OrderBook.add_buy_order(user=user,price=10,quantity=10)
    # OrderBook.add_buy_order(user=user,price=10,quantity=5) 
    # OrderBook.add_sell_order(user=user,price=10,quantity=5)
    # OrderBook.add_sell_order(user=user,price=10,quantity=10)
    # OrderBook.match_orders()
    
    # Trying out users
    # user1 = Users.objects.create(
    #         name = 'test1',
    #         password = 'test',
    #         equity = '1000'
    #     )
    # user2 = Users.objects.create(
    #     name = 'test1',
    #     password = 'test',
    #     equity = '1000'
    # )
    # OrderBook.add_buy_order(user=user1,price=10,quantity=10)
    # OrderBook.add_sell_order(user=user2,price=10,quantity=10)
    # OrderBook.match_orders()
    