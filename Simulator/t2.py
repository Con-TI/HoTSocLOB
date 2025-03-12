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
    #     user1 = Users.objects.get(name='test1')
    # except:
    #     user1 = Users.objects.create(name='test1', password='hbgiewjewbrijoekwfbiofewgkigrnik', equity=1000)
    # try:    
    #     user2 = Users.objects.get(name='test2')
    # except:
    #     user2 = Users.objects.create(name='test2', password='jfkjoejwkbejwkbhrjbefkrgfjebwhrbweh', equity=1000)
    # try:    
    #     LP = Users.objects.get(name='whaleLP')
    # except:
    #     LP = Users.objects.create(name='whaleLP', password='erwgjneroiogreignerkwiregkeirberkij', equity=1000000)
    # try:    
    #     LP = Users.objects.get(name='whaleLP2')
    # except:
    #     LP = Users.objects.create(name='whaleLP2', password='erwgjneroiogreignerkwiregkeirberkij', equity=1000000)
    


    # Clear DB
    PriceHistory.objects.filter().delete()
    for i in range(5):
        p = PriceData()
        PriceHistory.objects.create(price=p.fetch_midprice())

    # for u in Users.objects.filter():
    #     u.delete()
    