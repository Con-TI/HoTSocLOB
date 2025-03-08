if __name__=='__main__':
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    # Added this to fix the environment variable being set up only after service.models is called
    django.setup()
    
from models.models import Users, Orders, PriceHistory
from models.pricedata import PriceData
if __name__ == '__main__':
    # Create a new user
    # try: 
    #     user1 = Users.objects.get(name='test2')
    # except:
    #     user1 = Users.objects.create(name='test2', password='a', equity=1000)
    # try:    
    #     user2 = Users.objects.get(name='test3')
    # except:
    #     user2 = Users.objects.create(name='test3', password='a', equity=1000)
    
    # Orders.objects.create(user=user1, price=10, quantity=10)
    # Orders.objects.create(user=user2, price=20, quantity=-10)
    # p = PriceData()
    # midprice = p.fetch_midprice()
    # PriceHistory.objects.create(price=80)
    u = PriceData()
    print(u.summarize_orderbook())
    # for p in PriceHistory.objects.filter():
    #     p.delete()
    