# The python extension

We need to do it in python, since the extension is written in python. We use `websocket-client` to implement this.

## Connecting to the server

We need to enable `exportAuthInfo` in `[neutralino]` in `neutrapy.toml` to get connection information exported to `.tmp/auth_info.json`

With this information, we can connect using:

```
ws://127.0.0.1:<PORT>?extensionId=<EXTENSION_ID>
```

`websocket.WebSocketApp()` accepts 4 handlers:

- `on_open` - called when the connection is established
- `on_message` - called when a message is received
- `on_error` - called when an error occurs
- `on_close` - called when the connection is closed

With `on_message`, there are custom events, which are separated into different methods with `utils.API` class.

## Writing event handlers

The available event handlers can be found in `utils.API` class. You can also subclass `utils.API` and pass it to `WebSocketApp` (see `__main__.py`).  This way you don't have to implement all the event handlers, but use the default ones from `utils.API`.

## Sending messages to the app

You can send messages to the app using `api.send()`, which actually wraps `websocket.send()`, but the `id` and `accessToken` are automatically added to the message.

See also: https://neutralino.js.org/docs/how-to/extensions-overview#sending-a-message-from-the-extension-to-app
