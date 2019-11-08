from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
import blog.routing
from django.urls import path , include
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(blog.routing.websocket_urlpatterns)
        # URLRouter(blog.routing.websocket_urlpatterns,chat.routing.websocket_urlpatterns)
    ),
})