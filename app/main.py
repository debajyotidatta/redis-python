# Uncomment this to pass the first stage
import socket
import threading

def process_resp_string(resp_string):
    resp_string = resp_string.split("\n")
    new_str = []
    for j in resp_string:
        if len(j)>0:
            if j[0]!= '*' and j[0]!= '$':
                new_str.append(j.rstrip('\r'))
    return " ".join(new_str[1:])
        

def handle_client(conn, addr):
    connected = True
    while connected:
        data = conn.recv(6379)
        if data.decode() == "QUIT":
            connected = False
        elif "ECHO" in data.decode():
            output_string = data.decode()
            output_string = process_resp_string(output_string)
            conn.sendall(b"+%s\r\n" % output_string.encode())
        elif data:
            print(data)
            conn.sendall(b"+PONG\r\n")
    conn.close()

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    server = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()
        

    



if __name__ == "__main__":
    main()
