# Uncomment this to pass the first stage
import socket
import threading
import time

def process_resp_string(resp_string):
    resp_string = resp_string.split("\n")
    new_str = []
    for j in resp_string:
        if len(j)>0:
            if j[0]!= '*' and j[0]!= '$':
                new_str.append(j.rstrip('\r'))
    return " ".join(new_str[1:])

# def process_get(resp_string, result_dict):
#     resp_string = resp_string.split("\n")
#     new_str = []
#     for j in resp_string:
#         if len(j)>0:
#             if j[0]!= '*' and j[0]!= '$':
#                 new_str.append(j.rstrip('\r'))
#     if new_str[1] in result_dict:
#         return result_dict[new_str[1]]
#     else:
#         return "nil"

# def process_set(resp_string, result_dict):
#     resp_string = resp_string.split("\n")
#     new_str = []
#     for j in resp_string:
#         if len(j)>0:
#             if j[0]!= '*' and j[0]!= '$':
#                 new_str.append(j.rstrip('\r'))
#     result_dict[new_str[1]] = new_str[2]
#     return "OK"



def process_get(resp_string, result_dict, time_dict):
    """Process GET command. Return value if key exists, otherwise return nil.
    But make sure key not expired in time_dict which also stores the time,
    when the key was set"""
    resp_string = resp_string.split("\n")
    new_str = []
    for j in resp_string:
        if len(j)>0:
            if j[0]!= '*' and j[0]!= '$':
                new_str.append(j.rstrip('\r'))
    if new_str[1] in result_dict:
        if new_str[1] in time_dict:
            if time_dict[new_str[1]] > time.time():
                return result_dict[new_str[1]]
            else:
                return "nil"
        else:
            return result_dict[new_str[1]]
    else:
        return "nil"
    

def process_set(resp_string, result_dict, time_dict):
    """Process SET command. Return OK if key was set successfully.
    But make sure to store the time when the key was set in time_dict"""
    resp_string = resp_string.split("\n")
    new_str = []
    for j in resp_string:
        if len(j)>0:
            if j[0]!= '*' and j[0]!= '$':
                new_str.append(j.rstrip('\r'))
    result_dict[new_str[1]] = new_str[2]
    if len(new_str) == 5:
        time_dict[new_str[1]] = time.time() + int(new_str[4])
    return "OK"
        

def handle_client(conn, addr):
    connected = True
    result_dict = {}
    time_dict = {}
    while connected:
        data = conn.recv(6379)
        if data.decode() == "QUIT":
            connected = False
        elif ("ECHO" in data.decode()) or ("echo" in data.decode()):
            output_string = data.decode()
            output_string = process_resp_string(output_string)
            conn.sendall(b"+%s\r\n" % output_string.encode())
        elif ("GET" in data.decode()) or ("get" in data.decode()):
            output_string = data.decode()
            output_string = process_get(output_string, result_dict, time_dict)
            # print(result_dict)
            conn.sendall(b"+%s\r\n" % output_string.encode())
        elif ("SET" in data.decode()) or ("set" in data.decode()):
            output_string = data.decode()
            output_string = process_set(output_string, result_dict, time_dict)
            # print(result_dict)
            conn.sendall(b"+%s\r\n" % output_string.encode())
        elif data:
            # print(data)
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
