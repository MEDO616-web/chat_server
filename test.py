# text = "Hello"
# data = bytearray(text, "utf-8")  # تحويل النص إلى Bytes
# print(data)  # 🔹 النتيجة: bytearray(b'Hello')
# print()

import asyncio
import websockets

connected_clients = {}  # لتخزين العملاء المتصلين

async def handler(websocket):
    try:
        client_id = await websocket.recv()  # استقبال أول رسالة كـ ID العميل
        connected_clients[client_id] = websocket

        # إرسال قائمة المستخدمين المحدثة للجميع
        await broadcast_users()

        async for message in websocket:
            if message == "GET_USERS":  
                await websocket.send("USERS|" + "|".join(connected_clients.keys()))
            else:
                target_id, msg = message.split("|", 1)
                if target_id in connected_clients:
                    await connected_clients[target_id].send(f"{client_id}: {msg}")
    except:
        pass
    finally:
        if client_id in connected_clients:
            del connected_clients[client_id]
            await broadcast_users()

async def broadcast_users():
    """إرسال قائمة المستخدمين المتصلين للجميع"""
    user_list = "USERS|" + "|".join(connected_clients.keys())
    await asyncio.gather(*(ws.send(user_list) for ws in connected_clients.values()))

async def start_server():
    async with websockets.serve(handler, "0.0.0.0", 80):
        await asyncio.Future()  # إبقاء السيرفر قيد التشغيل

asyncio.run(start_server())
import asyncio
import websockets

connected_clients = {}  # لتخزين العملاء المتصلين

async def handler(websocket):
    try:
        client_id = await websocket.recv()  # استقبال أول رسالة كـ ID العميل
        connected_clients[client_id] = websocket

        # إرسال قائمة المستخدمين المحدثة للجميع
        await broadcast_users()

        async for message in websocket:
            if message == "GET_USERS":  
                await websocket.send("USERS|" + "|".join(connected_clients.keys()))
            else:
                target_id, msg = message.split("|", 1)
                if target_id in connected_clients:
                    await connected_clients[target_id].send(f"{client_id}: {msg}")
    except:
        pass
    finally:
        if client_id in connected_clients:
            del connected_clients[client_id]
            await broadcast_users()

async def broadcast_users():
    """إرسال قائمة المستخدمين المتصلين للجميع"""
    user_list = "USERS|" + "|".join(connected_clients.keys())
    await asyncio.gather(*(ws.send(user_list) for ws in connected_clients.values()))

async def start_server():
    async with websockets.serve(handler, "0.0.0.0", 80):
        await asyncio.Future()  # إبقاء السيرفر قيد التشغيل

asyncio.run(start_server())
