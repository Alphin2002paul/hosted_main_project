from django.utils.decorators import decorator_from_middleware
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control

cache_control_no_cache = cache_control(no_cache=True, no_store=True, must_revalidate=True)

def nocache(view_func):
    decorated_view_func = cache_control_no_cache(view_func)
    return decorated_view_func

# For class-based views
def nocache_class_view(view):
    return method_decorator(nocache, name='dispatch')(view)