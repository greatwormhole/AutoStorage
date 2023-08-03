from django.core.cache import cache

static_cache_keys = {
    'moving_crates': 'updated_crates',
    'storage_viewers': 'storage_subscribers',
    'blocked_cells': 'blocked_cells',
}

def set_cache(key, data, as_list=True):
    
    cached_data = cache.get(key, None)
    
    if as_list:
        if cached_data is not None:
            cached_data += [data]
        else:
            cached_data = [data]
    else:
        cached_data = data
        
    cache.set(key, cached_data)
    
def get_cache(key, default = None):
    
    return cache.get(key, default)

def delete_cache(key, data):
    
    cached_data = cache.get(key, None)
    
    if cached_data is not None and cached_data != []:
        cached_data.remove(data)
    else:
        raise ValueError('The cache is already empty')
    
    if cached_data != []:
        cache.set(key, cached_data)
    else:
        cache.delete(key)