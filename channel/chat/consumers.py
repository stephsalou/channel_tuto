
from asgiref.sync import async_to_sync , sync_to_async
from channels.generic.websocket import WebsocketConsumer , AsyncWebsocketConsumer 
from channels.db import database_sync_to_async
import json
from . import models

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print(dict(self.scope))
        print('nom du channel',self.channel_name)
        print('nom du salon',self.room_name)
        self.room_group_name = 'chat_%s' % self.room_name
        print('nom du group',self.room_group_name)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print('disconnect close code',close_code,'==================== channel layer:',self.channel_layer)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print('recuperaton du message envoyer par un channel avant le broadcast')
        print('data :',text_data_json)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        print('group populated finished')
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        mess_save = await self.message_save(message)
        print(mess_save)
        print('called chat message were group.send action has callable and send group message through specify channel ')
        print('data :',event)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
        print('channel populated finished')
    @database_sync_to_async
    def message_save(self,message):
        print('is saved?')
        mess = models.Message(message=message)
        mess.save()
        return mess