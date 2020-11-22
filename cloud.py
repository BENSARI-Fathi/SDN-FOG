"""
Cloud implementation
"""

# import
import socket
from protocole import *

ip = '127.0.0.1'
port = 2000
my_username = "Cloud"
# create cloud socket
socketCloud = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketCloud.connect((ip, port))
# Send our credential
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
socketCloud.send(username_header + username)
nice_print("connexion has been established!")
# receive request from the Fog
data_length = get_length(socketCloud)
print(data_length)
target_service = get_target_service(socketCloud)
print(target_service)
timestamp = get_time(socketCloud)
print(timestamp)
method = get_type(socketCloud)
print(method)
data = extract_data(socketCloud, data_length)
print(data)
if method == 'GET':
    build_dictionary = {
        'length': data_length,
        'time': timestamp,
        'method': method,
        'data': data
    }
    store_file("storage/database", build_dictionary)
else:
    delta_time = delay_value(timestamp)
    store_file('credential.txt', data)
    nice_print(f'Data Stored correctly, time: {delta_time} second')
