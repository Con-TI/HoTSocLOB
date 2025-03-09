if __name__=='__main__':
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    # Added this to fix the environment variable being set up only after service.models is called
    django.setup()
    
from models.models import Users, Orders, PriceHistory
from models.pricedata import PriceData
if __name__ == '__main__':
    '''from datetime import datetime
    init_time = datetime(2025, 3, 9, 1, 0, 0)
    now = datetime.now()
    elapsed_time = now - init_time
    elapsed_time = elapsed_time.total_seconds()
    elapsed_time = elapsed_time/3600
    print("Elapsed time:", elapsed_time, "hours")'''

    
