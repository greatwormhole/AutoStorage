import time
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from.WS_cache import WS_CACHE_CONNECTION, WS_CACHE_MESSAGE
import threading
from channels.layers import get_channel_layer

connectionDict = {}
threadList = {}

class consumerInfinityThread(object):

    def __init__(self, obj):

        self.threading = ConnectionThread(target=self.HMIThread)

        self.threading.start()

        self.info = []

        self.consumer = obj

    def infinite_stop(self):

        if self.threading.is_alive():

            self.threading.stop()

    def HMIThread(self):

        while not self.threading.stopped():

                time.sleep(30)

                message = 'true'

                # data = testsData.objects.all().order_by('-id')[0]
                # message.append(data.status)
                # message.append(data.result)

                self.consumer.send(text_data=message)

class ConnectionThread(threading.Thread):

    def __init__(self, *args, **kwargs):

        super(ConnectionThread, self).__init__(*args, **kwargs)

        self._stop = threading.Event()

    def stop(self):

        self._stop.set()

    def stopped(self):

        return self._stop.is_set()


class THDWS(WebsocketConsumer):

    def connect(self):

        self.id = self.scope['url_route']['kwargs']['room']

        self.room_name = 'THD_%s' % self.id

        #connectionDict[self.robot_ip] = opcConnection(self.robot_ip).connect()

        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )

        self.accept()


    def disconnect(self, close_code):

        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )


    def receive(self, text_data=None, bytes_data=None):

        text_data_json = json.loads(text_data)

        async_to_sync(self.channel_layer.group_send)(self.room_name, {
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
        
    def chat_message(self, event):

        self.send(text_data=json.dumps(
            {
                "room": event["room_id"],
                "username": event["username"],
                "message": event["message"],
            }))

class StorageVisualizing(WebsocketConsumer):
    
    def connect(self):
        
        self.room_name = 'TEST'
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )
        
        self.accept()
    
    def disconnect(self, code):
        
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )
    
    def receive(self, text_data=None, bytes_data=None):
        return super().receive(text_data, bytes_data)