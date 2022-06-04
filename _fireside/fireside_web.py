from aiohttp.web import Response
from agents import Agent
from aiohttp import WSMsgType


class FiresideWeb(Agent):

    html = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>WebSocket Echo</title>
        </head>
        <body>
            <h1>WebSocket Echo</h1>
            <form action="" onsubmit="sendMessage(event)">
                <input type="text" id="messageText" autocomplete="off"/>
                <button>Send</button>
            </form>
            <ul id='messages'>
            </ul>
            <script>
                var ws = new WebSocket("ws://{}:{}{}");
                ws.onmessage = function(event) {{
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                }};
                function sendMessage(event) {{
                    var input = document.getElementById("messageText")
                    ws.send(input.value)
                    input.value = ''
                    event.preventDefault()
                }}
            </script>
        </body>
    </html>
    """

    def setup(self, host="0.0.0.0", port="8080", ws_route="/ws"):

        self.host = host
        self.port = port
        self.ws_route = ws_route
        self.create_webserver(host, int(port))
        self.create_route("GET", "/", self.echo)
        self.rtx, self.connections = self.create_websocket(
            ws_route
        )  # Note: connections is read only, do not modify
        self.disposables.append(self.rtx.subscribe(self.handle_message))

    def handle_message(self, msg):

        # broadcast message to all connections
        for _id in self.connections.keys():
            if msg.message.type in [WSMsgType.TEXT, WSMsgType.BINARY]:
                self.rtx.on_next(msg.copy(connection_id=_id, request=None))
                self.log.debug(f"sending to {msg.message.data} {_id}")

    async def echo(self, request):
        return Response(
            text=self.html.format(self.host, self.port, self.ws_route),
            content_type="text/html",
        )


if __name__ == "__main__":
    webserver = FiresideWeb()
