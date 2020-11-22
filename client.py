"""
client implementation
"""

# import
import socket
from protocole import *

ip = '127.0.0.1'
port = 2000
my_username = input("Username>> ")
cloud_ip = '127.0.0.1'
cloud_port = 2500
# create tcp socket


def tcp_client(ip_cloud, port_cloud):
    """
    :param ip_cloud:
    :param port_cloud:
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip_cloud, port_cloud))
    length = get_length(client)
    timer = get_time(client)
    data_content = extract_data(client, length)
    delta = delay_value(timer)
    nice_print(f'reception complete in {delta} second')
    store_file_client(path, data_content)


# create client socket
socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketClient.connect((ip, port))
# Send our credential
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
socketClient.send(username_header + username)
nice_print("connexion has been established!")
method = set_type()
if method == 'GET':
    data = get_file_name()
    path = save_file_name(data)
else:
    data = post_data()
data = format_data(data)
target_service = set_target_service()
timestamp = time.time()
build_data_packet = build_message_to_server(length=len(data), service=target_service, time=timestamp,
                                            method=method, data=data)
send_data(socketClient, build_data_packet)
# receive answer from the server
if method == 'GET':
    data_length = get_length(socketClient)
    timestamp = get_time(socketClient)
    data = extract_data(socketClient, data_length)
    if target_service == 'True':
        delta_time = delay_value(timestamp)
        nice_print(f'reception complete in {delta_time} second')
        store_file_client(path, data)
    else:
        print(data)
        time.sleep(2)
        tcp_client(cloud_ip, cloud_port)

# socketClient.close()

