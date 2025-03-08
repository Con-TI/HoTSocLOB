from models.models import Users, Orders

class UserStats():
    @classmethod
    def calc_pnl(user):
        return 1000-user.equity
    
    @classmethod
    def fetch_pending_orders(user):
        orders = Orders.objects.filter(name=user.name).order_by('created_time')
        return [(order.price,order.quantity) for order in orders]
    
    @classmethod
    def calc_unreal_pnl(self, user, midprice):
        orders = self.fetch_pending_orders(user)
        return sum([(midprice-price,quantity) for price,quantity in orders])