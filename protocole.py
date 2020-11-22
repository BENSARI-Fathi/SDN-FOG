import time
import os
import pickle

HEADER_LENGTH = 4096
HEADER_TYPE = 5
HEADER_TIME = 24
HEADER_METHOD = 5


def register_user(client_socket):
    try:

        # Receive our "header" containing message length, it's size is defined and constant
        message_header = client_socket.recv(HEADER_LENGTH)

        # If we received no data, client gracefully closed a connection,
        # for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        if not len(message_header):
            return False

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:

        # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
        # or just lost his connection
        # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR)
        # what sends information about closing the socket (shutdown read/write)
        # and that's also a cause when we receive an empty message
        return False


def get_length(client_socket):
    """
    :param client_socket:
    :return: the length of data
    """
    return int(client_socket.recv(HEADER_LENGTH).decode().strip())


def get_target_service(client_socket):
    """
    :param client_socket:
    :return: the target service (Fog/Cloud)
    """
    return client_socket.recv(HEADER_TYPE).decode().strip()


def get_time(client_socket):
    """
    :param client_socket:
    :return: the timestamp
    """
    timestamp = client_socket.recv(HEADER_TIME).decode().strip()
    return float(timestamp)


def get_type(client_socket):
    """
    :param client_socket:
    :return: type of sended data
    """

    request = client_socket.recv(HEADER_METHOD).decode().strip()
    if request == "POST":
        return "POST"
    else:
        return "GET"


def extract_data(client_socket, length_data):
    """

    :param client_socket:
    :param length_data:
    :return: the received message
    """
    msg = client_socket.recv(HEADER_LENGTH)
    while len(msg) < length_data:
        msg += client_socket.recv(HEADER_LENGTH)
    return msg


def build_message_to_server(**kwargs):
    """
    :param kwargs:
    :return: the full message formatted and ready to be send over network
    """
    length = f"{kwargs['length']:<{HEADER_LENGTH}}"
    target = f"{kwargs['service']:<{HEADER_TYPE}}"
    timestamp = f"{kwargs['time']:<{HEADER_TIME}}"
    method = f"{kwargs['method']:<{HEADER_METHOD}}"
    data = kwargs['data']

    header = (length + target + timestamp + method).encode()
    return header + data


def format_data(data):
    """
    :param data:
    :return: bytes object that contain data
    """
    if type(data) is bytes:
        return data
    else:
        return data.encode()


def send_data(client_socket, data):
    """
    :param client_socket:
    :param data:
    :return: send the data via the network
    """
    client_socket.send(data)


def redirect(device):
    """
    :param device:
    :return: send a message to the client to open a connexion with the cloud
    and tell the cloud to open a server connexion
    """
    if device == "client":
        return b"300 redirected"
    else:
        return b"OPEN SERVER"


def update_time(timestamp):
    """
    :param timestamp:
    :return: update the time
    """
    return time.time() - (time.time() - timestamp)


def delay_value(timestamp):
    """
    :param timestamp:
    :return: get the value of the time taken to receive the data from the target entity
    """
    return time.time() - timestamp


def set_type():
    """
    :return: define the method Get data from service provider or Post data to be stored
    """
    method = input("[+] Do you want to Get or Post data:\n" + "1)GET\n" + "2)POST\n" + ">>")
    if method == "1":
        return "GET"
    elif method == "2":
        return "POST"
    else:
        print("[-] Invalid value please insert 1 or 2")
        return set_type()


def set_target_service():
    """
    :return: select the target service provider (Cloud/Fog)
    """
    data_type = input("[+] Your data is time sensitive ?\n" + "y/n\n" + ">>")
    if data_type == 'y':
        return 'True'

    elif data_type == 'n':
        return 'False'
    else:
        print('[-] Invalid input please retry!')
        return set_target_service()


def get_file_name():
    """
    :return: return the filename to be downloaded
    """
    file_dir = os.listdir('download')
    choice = "[+] Select File to download:\n"
    for i, file in enumerate(file_dir):
        choice += f"{i}) " + file + "\n"
    file_name = input(choice)
    return file_dir[int(file_name)]


def upload_file(path):
    """
    :param path:
    :return:  the content of the file
    """
    with open(path, "rb") as file:
        return file.read()


def store_file(path, data):
    """
    :param path:
    :param data:
    :return: store the received file
    """
    if type(data) is bytes:
        data = pickle.loads(data)
    with open(path, "wb") as file:
        my_pickler = pickle.Pickler(file)
        my_pickler.dump(data)


def nice_print(text):
    """
    :param text:
    :return: give a nice look to our output messages
    """
    print("#"*80)
    print("#" + text.center(78) + "#")
    print("#"*80)


def build_message_to_client(**kwargs):
    """
    :param kwargs:
    :return: the full message formatted and ready to be send over network
    """
    length = f"{kwargs['length']:<{HEADER_LENGTH}}"
    timestamp = f"{kwargs['time']:<{HEADER_TIME}}"
    data = kwargs['data']

    header = (length + timestamp).encode()
    return header + data


def save_file_name(name):
    """
    :param name:
    :return: save the file name selected in string format
    """
    return name


def get_cloud_socket(socket_dictionary):
    """
    :param socket_dictionary:
    :return: the cloud socket
    """
    for i in socket_dictionary:
        if socket_dictionary[i]["data"] == b"Cloud":
            return i


def post_data():
    name = input("what is your name ? >> ")
    surname = input("insert your surname >> ")
    birthday = input("was born on >> ")
    mail = input("insert your mail >> ")
    while True:
        passwd = input("insert your password >> ")
        confirm = input("insert again your password >> ")
        if passwd == confirm:
            break
        else:
            print("wrong password try again !")
    dictionary = {"name": name, "surname": surname, "birthday": birthday, "mail": mail, "passwd": passwd}
    return pickle.dumps(dictionary)


def store_file_client(path, data):
    """
    :param path: file name
    :param data: data received from target service (Cloud/Fog)
    """
    with open(path, 'wb') as file:
        file.write(data)


def extract_data_from_file(path):
    """
    :param path:
    :return: the dictionary that contain data stored in file
    """
    with open(path, 'rb') as file:
        my_depickler = pickle.Unpickler(file)
        return my_depickler.load()
