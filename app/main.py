# Uncomment this to pass the first stage
import socket
import asyncio


async def multi_client():
    server = socket.create_server(("localhost", 6379), reuse_port=True)
    tasks = []
    while True:
        client, _ = await server.accept()
        tasks.append(client)
        while client:
            data = await client.recv(6379)
            if data:
                await client.sendall(b"+PONG\r\n")
            else:
                break
        await asyncio.gather(*tasks)
        

async def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    multi_client()
    

    # conn, addr = server_socket.accept() # wait for client
    # with conn:
    #     print(f"Connected by {addr}")
    #     while True:
    #         data = conn.recv(6379)
    #         if data!=None:

    #             conn.sendall(b"+PONG\r\n")



if __name__ == "__main__":
    main()
