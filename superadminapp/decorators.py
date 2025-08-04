from functools import wraps
from django.core.exceptions import PermissionDenied

def allowed_roles(roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Check if user is an admin or superuser
            if 'admin' in roles and (request.user.roles == 'admin' or request.user.is_superuser):
                return view_func(request, *args, **kwargs)
            # Check if user is an admin or instructor (case-insensitive)
            if 'admin_and_instructor' in roles and (
                request.user.role == 'admin' or 
                request.user.role.lower() == 'instructor'
            ):
                return view_func(request, *args, **kwargs) 
            # Deny access if no condition is met
            raise PermissionDenied  
        
        return _wrapped_view
    return decorator