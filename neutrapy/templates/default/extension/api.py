import os
import uuid
import json
from .utils import NEU_TOKEN, LOGGER

class API:

    def __init__(self, ws):
        self.ws = ws

    def send(self, event, data):
        LOGGER.info("[send] %s (%s)", event, data)
        self.ws.send(json.dumps({
            "id": str(uuid.uuid4()),
            "method": "app.broadcast",
            "accessToken": NEU_TOKEN,
            "data": {"event": event, "data": data}
        }))

    def on_windowclose(self, data):
        LOGGER.info("[on_windowclose] %s", data)
        self.ws.close()
        os._exit(0)

    def on_windowfocus(self, data):
        LOGGER.info("[on_windowfocus] %s", data)

    def on_windowblur(self, data):
        LOGGER.info("[on_windowblur] %s", data)

    def on_extclientconnect(self, data):
        LOGGER.info("[on_extclientconnect] %s", data)

    def on_appclientconnect(self, data):
        LOGGER.info("[on_appclientconnect] %s", data)

    def on_appclientdisconnect(self, data):
        LOGGER.info("[on_appclientdisconnect] %s", data)

    def on_clientconnect(self, data):
        LOGGER.info("[on_clientconnect] %s", data)

    def on_clientdisconnect(self, data):
        LOGGER.info("[on_clientdisconnect] %s", data)
        self.ws.close()
        os._exit(0)

    def on_fromapptoextension(self, data):
        LOGGER.info("[on_fromapptoextension] %s", data)
        import ast
        code = ast.parse(data, mode="exec")
        last = ast.Expression(code.body.pop().value)
        _globals, _locals = {}, {}
        try:
            exec(compile(code, "<string>", "exec"), _globals, _locals)
            out = eval(compile(last, "<string>", "eval"), _globals, _locals)
        except Exception as e:
            out = f"{type(e).__name__}: {e}"

        self.send("fromExtensionToApp", str(out))

    def on_message(self, message):
        # the typical message sent from the neu application is a string
        # in the form {"data": value, "event": "dispatchedEventName"}
        # so we parse the data here
        if not isinstance(message, str):
            raise TypeError("Message must be a string")

        message = json.loads(message)

        # some messages received do not have the "event" key, so safely ignore ethose
        if "event" not in message:
            return

        event = message["event"].lower()

        try:
            fn = getattr(self, f"on_{event}")
        except AttributeError:
            raise ValueError(f"Event handler not defined with api: {event}")

        fn(message["data"])

    def on_error(self, error):
        LOGGER.info("[on_error] %s", error)

    def on_close(self, close_status_code, close_msg):
        LOGGER.info("[on_close] %s (%s)", close_msg, close_status_code)
        # Make sure to exit the extension process when WS extension is closed
        # (when Neutralino app exits)
        os._exit(0)

    def on_open(self):
        LOGGER.info("[on_open] Connection has been established")

    def handler(self, event):
        """Produces the event handler to WebSocketApp"""
        fn = getattr(self, f"on_{event}")

        def _handler(ws, *args, **kwargs):
            if self.ws is not ws:
                raise ValueError("WebSocketApp instance mismatch")

            fn(*args, **kwargs)

        return _handler
