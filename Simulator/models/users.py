if __name__=='__main__':
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    # Added this to fix the environment variable being set up only after service.models is called
    django.setup()

from models.models import Users

'''user = Users.objects.filter()
for u in user:
    u.delete()
Users.objects.create(
    name = 'test1',
    password = 'a',
    equity = 1000  
)'''

#get
#t = Users.objects.get(name='test2')
#print(t)
#Users.objects.filter(...=...)

def Add_User(name, password):
    try: 
        Users.objects.get(name=name)
        return False
    except:
        Users.objects.create(
            name = name,
            password = password,
            equity = 1000 
        )
        return True

def Check_Login(name, password):
    try:
        user = Users.objects.get(name = name)
        if user.password != password:
            return False
        return True
        
    except:
        return False