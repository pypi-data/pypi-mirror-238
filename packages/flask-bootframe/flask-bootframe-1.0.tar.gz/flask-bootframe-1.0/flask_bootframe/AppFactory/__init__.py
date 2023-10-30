from flask_bootframe.AppFactory.http import HttpFactory
from flask_bootframe.AppFactory.websocket import WebsocketFactory


factories = {
    'websocket': WebsocketFactory(),
    'http': HttpFactory()
}
