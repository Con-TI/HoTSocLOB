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
    try: 
        user1 = Users.objects.get(name='test1')
    except:
        user1 = Users.objects.create(name='test1', password='a', equity=1000)
    try:    
        user2 = Users.objects.get(name='test2')
    except:
        user2 = Users.objects.create(name='test2', password='a', equity=1000)
    
    # Clear DB
    # for p in PriceHistory.objects.filter():
    #     p.delete()
    # for u in Users.objects.filter():
    #     u.delete()
    