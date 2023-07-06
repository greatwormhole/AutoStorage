from django.core.exceptions import PermissionDenied
import json

def check_access(action):
        
    def inner_func(view_func):

        def wrapper(self, request, *args, **kwargs):
            
            try:
                cookie = json.loads(request.COOKIES.get('AccessKey'))
                print(cookie)
            except:
                raise PermissionDenied('У вас нет прав, чтобы выполнить это действие')

            if cookie.get(action):
                return view_func(self, request, *args, **kwargs)
            else:
                raise PermissionDenied('У вас нет прав, чтобы выполнить это действие')

        return wrapper
    
    return inner_func
