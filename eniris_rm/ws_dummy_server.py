import asyncio
import json
from typing import Any

from websockets.server import WebSocketServerProtocol, serve


async def echo(websocket: WebSocketServerProtocol, path: str) -> None:
    if path != "/s2":
        print(f"Rejected connection on unsupported path: {path}")  # noqa: T201
        await websocket.close()
        return
    print(f"New connection on {path}")  # noqa: T201
    async for message in websocket:
        try:
            data: Any = json.loads(message)
            pretty: str = json.dumps(data, indent=2)
            print(f"Received JSON message:\n{pretty}")  # noqa: T201
        except json.JSONDecodeError:
            print(f"Received text message: {message}")  # noqa: T201

async def _run_server() -> None:
    async with serve(echo, "0.0.0.0", 8000):
        print("WebSocket server started on ws://0.0.0.0:8000 (accepts all paths, only /s2 will be handled)")  # noqa: T201
        await asyncio.Future()  # run forever

def main():
    asyncio.run(_run_server())

if __name__ == "__main__":
    main()
