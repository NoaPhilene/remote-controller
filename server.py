import asyncio
import json
import ctypes

import websockets
import pyautogui

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

CLIENTS = set()

SCROLLBAR_X_MARGIN = 8
TOP_MARGIN = 120
BOTTOM_MARGIN = 120

scrollbar_dragging = False


def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))


def get_scrollbar_position(progress: float):
    screen_w, screen_h = pyautogui.size()

    x = screen_w - SCROLLBAR_X_MARGIN
    top_y = TOP_MARGIN
    bottom_y = screen_h - BOTTOM_MARGIN

    if bottom_y <= top_y:
        bottom_y = top_y + 1

    progress = clamp(progress, 0.0, 1.0)
    y = int(top_y + (bottom_y - top_y) * progress)

    return x, y


def lock_windows():
    ctypes.windll.user32.LockWorkStation()


async def handle(websocket):
    global scrollbar_dragging

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

            elif action == "scrollbar_start":
                progress = float(data.get("progress", 0))
                x, y = get_scrollbar_position(progress)
                pyautogui.moveTo(x, y, _pause=False)
                pyautogui.mouseDown(button="left", _pause=False)
                scrollbar_dragging = True

            elif action == "scrollbar_move":
                if scrollbar_dragging:
                    progress = float(data.get("progress", 0))
                    x, y = get_scrollbar_position(progress)
                    pyautogui.moveTo(x, y, _pause=False)

            elif action == "scrollbar_end":
                if scrollbar_dragging:
                    pyautogui.mouseUp(button="left", _pause=False)
                    scrollbar_dragging = False

            elif action == "lock":
                lock_windows()

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
        if scrollbar_dragging:
            pyautogui.mouseUp(button="left", _pause=False)
            scrollbar_dragging = False

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