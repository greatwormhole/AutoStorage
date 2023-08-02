from django.core.cache import cache

def set_crate_cache(data):
    
    cached_crates = cache.get('updated_crates', None)
    
    if cached_crates is not None:
        cached_crates += [data]
    else:
        cached_crates = [data]
        
    cache.set('updated_crates', cached_crates)
    
def get_crate_cache():
    
    return cache.get('updated_crates', None)

def set_subscriber_cache(id):
    
    cache.delete('storage_subscribers')
    cache.delete('updated_crates')
    cached_users = cache.get('storage_subscribers', None)
    
    if cached_users is not None:
        cached_users += [id]
    else:
        cached_users = [id]
        
    cache.set('storage_subscribers', cached_users)
    
def get_subscriber_cache():
    
    return cache.get('storage_subscribers', None)

def delete_subscriber_cache(id):
    
    cached_subscribers = cache.get('storage_subscribers', None)
    
    if cached_subscribers is not None and cached_subscribers != []:
        cached_subscribers.remove(id)
    else:
        raise ValueError('The cache is already empty')
    
    if cached_subscribers != []:
        cache.set('storage_subscribers', cached_subscribers)
    else:
        cache.delete('storage_subscribers')