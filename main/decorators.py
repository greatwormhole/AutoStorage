from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
import json

def check_access(action=None):
        
    def inner_func(view_func):

        def wrapper(self, request, *args, **kwargs):
            
            cookie = request.COOKIES.get('AccessKey', None)

            if cookie is not None:
                access_key = json.loads(cookie)
            else:
                cookie = {
                    'id': -1,
                    'name': "NA",
                    'storage_right': False,
                    'plan_right': False,
                    'quality_control_right': False,
                }

                response = redirect('login')
                response.set_cookie(key='AccessKey', value=json.dumps(cookie))

                return response
            
            if action is None or access_key.get(action, False) or access_key.get('name', None) not in ('NA', None):
                return view_func(self, request, *args, **kwargs)
            else:
                raise PermissionDenied('У вас нет прав, чтобы выполнить это действие')

        return wrapper
    
    return inner_func
