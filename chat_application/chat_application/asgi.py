import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_application.settings')
django.setup()


from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat.routing


application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    "websocket": AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))
})
