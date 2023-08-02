from django.core.cache import cache

def set_crate_cache(data):
    
    cached_crates = cache.get('updated_crates', None)
    
    if cached_crates is not None:
        cached_crates += [data]
    else:
        cached_crates = [data]
        
    cache.set('updated_crates', cached_crates)
    
def get_crate_cache():
    
    return cache.get('updated_crates', [])