if __name__=='__main__':
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    # Added this to fix the environment variable being set up only after service.models is called
    django.setup()

from models.models import Users, Orders, Positions

class UserStats():
    def calc_pnl(self, equity):
        return equity-10000
    
    def fetch_pending_orders(self, user):
        orders = Orders.objects.filter(user=user).order_by('created_time')
        return orders
    
    def fetch_positions(self, user):
        positions = Positions.objects.filter(user=user).order_by('created_time')
        return positions
    
    def calc_unreal_pnl(self, user, midprice):
        orders = self.fetch_positions(user)
        if len(orders) == 0:
            return 0
        orders = [(order.price,order.quantity) for order in orders]
        unreal_pnl = sum([(midprice-price)*quantity for price,quantity in orders])
        return unreal_pnl
    
# TODO: Test out this class
if __name__ == '__main__':
    u = UserStats()
    user = Users.objects.get(name='test2')
    o = u.fetch_pending_orders(user)
    print(o)