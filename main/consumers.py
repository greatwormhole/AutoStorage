import time
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

import threading
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

                time.sleep(3)

                message = ['This is socket message']
                

                # data = testsData.objects.all().order_by('-id')[0]
                # message.append(data.status)
                # message.append(data.result)

                self.consumer.send(text_data=json.dumps({
                    'event': "Send",
                    'message': message,
                }))

class ConnectionThread(threading.Thread):

    def __init__(self, *args, **kwargs):

        super(ConnectionThread, self).__init__(*args, **kwargs)

        self._stop = threading.Event()

    def stop(self):

        self._stop.set()

    def stopped(self):

        return self._stop.is_set()

class test(WebsocketConsumer):

    def connect(self):

        self.id = self.scope['url_route']['kwargs']['room']

        self.room_name = 'room_%s' % self.id

        #connectionDict[self.robot_ip] = opcConnection(self.robot_ip).connect()

        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )

        self.accept()

        self.thread = consumerInfinityThread(self)

    def disconnect(self):

        self.thread.infinite_stop()

        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )

  
