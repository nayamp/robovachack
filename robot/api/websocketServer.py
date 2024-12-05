import websockets
import asyncio
 
# Creating WebSocket server
async def ws_server(websocket):
    print("WebSocket: Server Started.")
 
    try:
        while True:
            # Receiving values from client
            name = await websocket.recv() 
            # Prompt message when any of the field is missing
            if name == "":
                print("Error Receiving Value from Client.")
                break
            if name =="default":
                continue
            if name =="forward":
                print("nice,forward")
                continue
            if name =="back":
                print("nice,back")
                continue
            if name =="left":
                print("nice,left")
                continue
            if name =="right":
                print("nice,right")
                continue
            else:
                print(name)
            # Printing details received by client
            # Sending a response back to the client
            ##if int(age) < 18:
                ##await websocket.send(f"Sorry! {name}, You can't join the club.")

 
    except websockets.ConnectionClosedError:
        print("Internal Server Error.")
 
 
async def main():
    async with websockets.serve(ws_server, "localhost", 7890):
        await asyncio.Future()  # run forever
 
if __name__ == "__main__":
    asyncio.run(main())