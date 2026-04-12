import asyncio
import json

import websockets
import pyautogui

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

CLIENTS = set()


async def handle(websocket):
    CLIENTS.add(websocket)
    print(f"[+] Client connected ({len(CLIENTS)} total)")

    try:
        async for message in websocket:
            data = json.loads(message)
            action = data.get("action")

            if action == "move":
                dx = data.get("dx", 0)
                dy = data.get("dy", 0)
                pyautogui.moveRel(dx, dy, _pause=False)

            elif action == "click":
                btn = data.get("button", "left")
                pyautogui.click(button=btn, _pause=False)

            elif action == "doubleclick":
                pyautogui.doubleClick(_pause=False)

            elif action == "rightclick":
                pyautogui.rightClick(_pause=False)

            elif action == "scroll":
                amount = data.get("amount", 0)
                pyautogui.scroll(amount, _pause=False)

            elif action == "keydown":
                key = data.get("key", "")
                if key:
                    pyautogui.keyDown(key, _pause=False)

            elif action == "keyup":
                key = data.get("key", "")
                if key:
                    pyautogui.keyUp(key, _pause=False)

            elif action == "type":
                text = data.get("text", "")
                if text:
                    pyautogui.write(text, interval=0.02)

            elif action == "hotkey":
                keys = data.get("keys", [])
                if keys:
                    pyautogui.hotkey(*keys, _pause=False)

    except websockets.ConnectionClosed:
        pass
    finally:
        CLIENTS.discard(websocket)
        print(f"[-] Client disconnected ({len(CLIENTS)} total)")


async def main():
    host = "0.0.0.0"
    port = 8765
    print(f"WebSocket server starting on ws://{host}:{port}")

    async with websockets.serve(handle, host, port):
        print("Server running. Press Ctrl+C to stop.")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())