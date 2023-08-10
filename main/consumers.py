import time
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
import json
from.WS_cache import WS_CACHE_CONNECTION, WS_CACHE_MESSAGE
import threading


from .caching import delete_cache_from_list, get_cache, set_cache, static_cache_keys,delete_cache_dict

connectionDict = {}
threadList = {}
storage_infinite_thread = []

class consumerInfinityThread(object):

    def __init__(self, obj, kwargs):

        self.threading = ConnectionThread(target=self.HMIThread, kwargs=kwargs)

        self.threading.start()

        self.info = []

        self.consumer = obj

    def infinite_stop(self):

        if self.threading.is_alive():

            self.threading.stop()

            storage_infinite_thread.pop()

    def HMIThread(self, type):

        while not self.threading.stopped():

            time.sleep(30)
            match type:
                case 'get_crates_cache':
                    message = json.dumps(get_cache(static_cache_keys['moving_crates']))
                case _:
                    message = 'true'
            delete_cache_dict(static_cache_keys['moving_crates'])

            if message != 'null':
                async_to_sync (self.consumer.channel_layer.group_send)(self.consumer.room_name, {
                    "type": "chat.message",
                    "room_id": self.consumer.room_name,
                    "message": message,
                })

class ConnectionThread(threading.Thread):

    def __init__(self, *args, **kwargs):

        super(ConnectionThread, self).__init__(*args, **kwargs)

        self._stop = threading.Event()

    def stop(self):

        self._stop.set()

    def stopped(self):

        return self._stop.is_set()


class THDWS(AsyncWebsocketConsumer):

    async def connect(self):

        self.id = self.scope['url_route']['kwargs']['room']

        self.room_name = 'THD_%s' % self.id

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )


    async def receive(self, text_data=None, bytes_data=None):

        text_data_json = json.loads(text_data)

        await self.channel_layer.group_send(self.room_name, {
            "type": "chat.message",
            "room_id": self.room_name,
            "username": self.scope["user"].username,
            "message": text_data,
        })

        print('Receive')
        
        print(f'ws_cache_mess: {WS_CACHE_MESSAGE}')
        print('code: '+ str(text_data_json['code']))

        if text_data_json['code'] == 11:

            WS_CACHE_CONNECTION[text_data_json['data']['ip']] = True
            print(f'ws_cache_conn: {WS_CACHE_CONNECTION}')
            return

        if text_data_json['code'] == 101:

            WS_CACHE_CONNECTION[text_data_json['data']['ip']] = False
            print(f'ws_cache_conn: {WS_CACHE_CONNECTION}')
            return
        
    async def chat_message(self, event):

        await self.send(text_data=json.dumps(
            {
                "room": event["room_id"],
                "username": event["username"],
                "message": event["message"],
            }))

class StorageVisualizingWS(AsyncWebsocketConsumer):
    
    async def connect(self):
        
        self.worker_id = int(self.scope['url_route']['kwargs']['id'])
        self.room_name = 'storage_visualizing'
        
        subs_cache = get_cache(static_cache_keys['storage_viewers'])
        print(f'Started list: {subs_cache}')
        
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

        if len(storage_infinite_thread) == 0:
            try:
                storage_infinite_thread.pop()
            except:
                pass
            storage_infinite_thread.append(consumerInfinityThread(self, kwargs={'type': 'get_crates_cache'}))

        set_cache(static_cache_keys['storage_viewers'], self.worker_id)
    
    async def disconnect(self, close_code):
        
        print(f'Pre-stopped list: {get_cache(static_cache_keys["storage_viewers"])}')
        
        delete_cache_from_list(static_cache_keys['storage_viewers'], self.worker_id)
        
        print(f'Stopped list: {get_cache(static_cache_keys["storage_viewers"])}')
        
        if get_cache(static_cache_keys['storage_viewers']) is None:
            storage_infinite_thread[0].infinite_stop()
        print(storage_infinite_thread)
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )
    async def chat_message(self, event):

        await self.send(text_data=json.dumps(
            {
                "room": event["room_id"],
                "message": event["message"],
            }))

