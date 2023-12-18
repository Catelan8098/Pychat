import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            print(message)
        except Exception as e:
            print(e)
            break

def start_client():
    host = "127.0.0.1"
    port = 58712

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    username = input(client.recv(1024).decode("utf-8"))
    client.send(username.encode("utf-8"))

    password = input(client.recv(1024).decode("utf-8"))
    client.send(password.encode("utf-8"))

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    while True:
        message = input()
        client.send(message.encode("utf-8"))


start_client()
