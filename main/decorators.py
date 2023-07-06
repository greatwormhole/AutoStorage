from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
import json

def check_access(action=None, redirect_to='login'):
        
    def inner_func(view_func):

        def wrapper(self, request, *args, **kwargs):
            
            cookie = request.COOKIES.get('AccessKey', None)

            if cookie is not None:
                access_key = json.loads(cookie)
            else:
                return redirect(redirect_to)
            
            if action is None or access_key.get(action):
                return view_func(self, request, *args, **kwargs)
            else:
                raise PermissionDenied('У вас нет прав, чтобы выполнить это действие')

        return wrapper
    
    return inner_func
