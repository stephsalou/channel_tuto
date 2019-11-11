from asgiref.sync import async_to_sync , sync_to_async
from channels.generic.websocket import WebsocketConsumer , AsyncWebsocketConsumer 
from channels.db import database_sync_to_async
import json
from .models import Message
from datetime import datetime

class notifConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'notification'
        print(dict(self.scope))
        print('nom du channel',self.channel_name)
        print('nom du salon',self.room_name)
        self.room_group_name = 'receiver'
        print('nom du group',self.room_group_name)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        mess = await self.get_all_message()
        
        for  m in mess:
            data = {
                'message':m.message,
                'is_read':m.is_read,
                'status':m.status,
                'date_add':m.date_add.strftime('%d%m%Y'),
                'date_upd':m.date_upd.strftime('%d%m%Y'),
            }
            await self.send(text_data=json.dumps(data))

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
        if 'message' in text_data_json and 'is_read' in text_data_json:
            message = text_data_json['message']
            is_read = text_data_json['is_read']
            if is_read :
                is_del = await self.del_message(message)
            else:
                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'is_read':False
                    }
                )
                mess = await self.message_save(message)
        elif 'mode' in text_data_json and 'message' in text_data_json:
            mode = text_data_json['mode']
            message = text_data_json['message']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':mode,
                    'message':message,
                }
            )
            if mode == 'switch':
                print('sending request ======================== ')
                await self.send(text_data=json.dumps({
                    'refresh':True
                }))
        print('group populated finished')
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        is_read = event['is_read']
        print('called chat message were group.send action has callable and send group message through specify channel ')
        print('data :',event)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'is_read':is_read
        }))
        print('channel populated finished')
    async def switch(self,event):
        msg = event['message']
        print('called chat message were group.send action has callable and send group message through specify channel ')
        print('data :',event)
        msg = await self.take_message(msg)
        await self.switch_message(msg)
    print('channel populated finished')
    @database_sync_to_async
    def message_save(self,message):
        print('is saved?')
        mess = Message(message=message)
        mess.save()
        return mess
    @database_sync_to_async
    def del_message(self,message):
        mess = Message.objects.get(message=message)
        mess.delete()
        mess.save()
        return True
    @database_sync_to_async
    def get_message(self):
        return Message.objects.filter(is_read=False)
    
    @database_sync_to_async
    def get_all_message(self):
        return Message.objects.all().order_by('date_upd')
    @database_sync_to_async
    def take_message(self,message):
        return Message.objects.filter(message=message)[:1].get() or None
    @database_sync_to_async 
    def switch_message(self,message):
        message.is_read=True
        message.save()