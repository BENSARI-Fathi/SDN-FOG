"""
Cloud Server implementation
"""

# import
import socket
from protocole import *
import select

ip = '127.0.0.1'
port = 2500
DB_FILE = "storage/database"
# create cloud server
cloudServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cloudServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
cloudServer.bind((ip, port))
cloudServer.listen(5)
# sock_client, address = cloudServer.accept()
nice_print(f"server listening on {ip}:{port}")
# List that contain all socket used in this connexion
socketList = [cloudServer]
while True:
    rsocket, wsocket, xsocket = select.select(socketList, [], socketList)
    for notifiedSocket in rsocket:
        if notifiedSocket == cloudServer:
            client_socket, client_address = cloudServer.accept()
            # Add accepted socket to select.select() list
            socketList.append(client_socket)
            request = extract_data_from_file(DB_FILE)
            if request['method'] == 'GET':
                answer = upload_file("download/" + request['data'].decode())
                data = build_message_to_client(length=len(answer), time=request['time'], data=answer)
                send_data(client_socket, data)
            else:
                delta_time = delay_value(request['time'])
                store_file('credential.txt', request['data'])
                nice_print(f'Data Stored correctly, time: {delta_time} second')
        else:
            socketList.remove(notifiedSocket)
            notifiedSocket.close()
            nice_print("Transmission complete!")
# update time is next step

