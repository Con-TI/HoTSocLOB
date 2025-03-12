from celery import shared_task
from models.pricedata import PriceData
from LPs.lp import LP

@shared_task
def update_database_task():
    # No need for the time check - Celery's scheduler will handle timing
    u = PriceData()
    u.update_price_history()
    l = LP()
    l.update_all()
    # l = BlockLP()
    # l.update_all()
    return "Database updated successfully"