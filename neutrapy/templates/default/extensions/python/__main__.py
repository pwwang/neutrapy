import websocket
import rel
from .api import API
from .utils import NEU_URL


if __name__ == "__main__":

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(NEU_URL)
    api = API(ws)
    ws.on_open = api.handler("open")
    ws.on_message = api.handler("message")
    ws.on_error = api.handler("error")
    ws.on_close = api.handler("close")

    # Set dispatcher to automatic reconnection
    ws.run_forever(dispatcher=rel, skip_utf8_validation=True)
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
