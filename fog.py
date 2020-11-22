"""

fog implementation

"""

# import
import socket
import select
from protocole import *
# Creation of socket server

ip = '127.0.0.1'
port = 2000
socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socketServer.setblocking(False)
socketServer.bind((ip, port))
socketServer.listen(5)

nice_print(f"server listening on {ip}:{port}")

# dictionary that contain the client socket
clients = {}

# List that contain all socket used in this connexion
socketList = [socketServer]


while True:
    rsocket, wsocket, xsocket = select.select(socketList, [], socketList)
    for notifiedSocket in rsocket:
        if notifiedSocket == socketServer:
            client_socket, client_address = socketServer.accept()

            # Client should send his name right away, receive it
            user = register_user(client_socket)
            if user is False:
                print("there was an error")
            # Add accepted socket to select.select() list
            socketList.append(client_socket)

            # Also save username and username header
            clients[client_socket] = user

            display_message = f'Accepted new connection from {client_address[0]}:{client_address[1]},' \
                              f' username: {user["data"].decode()}'
            nice_print(display_message)
        else:
            try:
                # receive request from the client
                data_length = get_length(notifiedSocket)
                print(data_length)
                target_service = get_target_service(notifiedSocket)
                print(target_service)
                timestamp = get_time(notifiedSocket)
                print(timestamp)
                method = get_type(notifiedSocket)
                print(method)
                data = extract_data(notifiedSocket, data_length)
                print(data)
                # check the target service (Fog/Cloud)
                if target_service == 'True':
                    # check the request method (Get/Post)
                    if method == 'GET':
                        # send answer
                        data = data.decode()
                        answer = upload_file("download/" + data)
                        build_data_packet = build_message_to_client(length=len(answer), time=timestamp, data=answer)
                        send_data(notifiedSocket, build_data_packet)
                    else:
                        delta_time = delay_value(timestamp)
                        store_file('credential.txt', data)
                        nice_print(f'Data Stored correctly, time: {delta_time} second')
                else:
                    client_message = redirect("client")
                    redirect_to_client = build_message_to_client(length=len(client_message), time=timestamp,
                                                                 data=client_message)
                    send_data(notifiedSocket, redirect_to_client)
                    cloud_message = build_message_to_server(length=len(data), service=target_service, time=timestamp,
                                                            method=method, data=data)
                    cloud_socket = get_cloud_socket(clients)
                    send_data(cloud_socket, cloud_message)
            except:
                socketList.remove(notifiedSocket)
                del clients[notifiedSocket]
                notifiedSocket.close()
