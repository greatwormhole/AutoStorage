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
    
    cached = cache.get(key, default)
    
    if cached == default or cached == {} or cached == []:
        return default
    return cache.get(key, default)

def delete_cache_from_dict(key, inner_key):
    
    cached_data = cache.get(key, None)
    
    if cached_data is not None:
        cached_data.pop(inner_key)
    else:
        raise ValueError('The cache is already empty')
    
    if cached_data != {}:
        cache.set(key, cached_data)
    else:
        cache.delete(key)

def delete_cache_from_list(key, data):
    
    cached_data = cache.get(key, None)
    
    if cached_data is not None:
        cached_data.remove(data)
    else:
        raise ValueError('The cache is already empty')
    
    if cached_data != []:
        cache.set(key, cached_data)
    else:
        cache.delete(key)