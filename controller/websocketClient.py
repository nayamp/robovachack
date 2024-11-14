import websockets
import asyncio
import keyboard  # using module keyboard

# The main function that will handle connection and communication
# with the server
async def ws_client():
    print("WebSocket: Client Connected.")
    url = "ws://localhost:7890"
    name="default"
    # Connect to the server
    async with websockets.connect(url) as ws:

        while True:  # making a loop
            name="default"
            try:  # used try so that if user pressed other than the given key error will not be shown
                if keyboard.is_pressed('w'):  # if key 'q' is pressed 
                    name='forward'
                    await ws.send(f"{name}")
                    continue  # finishing the loop
                if keyboard.is_pressed('a'):  # if key 'q' is pressed 
                    name='left'
                    await ws.send(f"{name}")
                    continue  # finishing the loop
                if keyboard.is_pressed('d'):  # if key 'q' is pressed 
                    name='right'
                    await ws.send(f"{name}")
                    continue  # finishing the loop
                if keyboard.is_pressed('s'):  # if key 'q' is pressed 
                    name='back'
                    await ws.send(f"{name}")
                    continue  # finishing the loop
                if name == 'exit':
                    exit()
            except Exception as e:
                print("error,", e)
                break  # if user pressed a key other than the given key the loop will break
 
 
        # Stay alive forever, listen to incoming msgs
        ##while True:
            ##msg = await ws.recv()
            ##print(msg)
 
# Start the connection
asyncio.run(ws_client())