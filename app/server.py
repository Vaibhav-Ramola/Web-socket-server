
# Tried to code from the base python packages
# Depreciated implementation


import websockets
import asyncio

PORT = 7890     # Port on which the server will run

print(f'Listening on port : {PORT}')

async def echo(websocket, path):
    print("A client connected")
    try:
        async for message in websocket:
            print("Received message from client : " + message)
            await websocket.send("Ping : " + message)
    except websockets.exceptions.ConnectionClosed as e:
        print("Client disconnected")


start_server = websockets.serve(echo, 'localhost', PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()