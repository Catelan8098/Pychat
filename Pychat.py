import socket
import threading
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            print(message)
        except Exception as e:
            print(e)
            break

def send_file(client_socket, filepath):
    try:
        with open(filepath, "rb") as file:
            file_data = file.read(1024)
            while file_data:
                client_socket.send(file_data)
                file_data = file.read(1024)
    except FileNotFoundError:
        print("Arquivo não encontrado.")

def start_client():
    host = "192.168.0.11"
    port = 58729

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
    except Exception as e:
        print(f"Erro ao conectar ao servidor: {e}")
        return

    # Escolher entre cadastro ou login
    response = input(client.recv(1024).decode("utf-8"))
    client.send(response.encode("utf-8"))

    if response.lower() == 'login':
        username = input(client.recv(1024).decode("utf-8"))
        client.send(username.encode("utf-8"))

        password = input(client.recv(1024).decode("utf-8"))
        hashed_password = hash_password(password)
        client.send(hashed_password.encode("utf-8"))

    elif response.lower() == 'cadastro':
        new_username = input(client.recv(1024).decode("utf-8"))
        client.send(new_username.encode("utf-8"))

        new_password = input(client.recv(1024).decode("utf-8"))
        hashed_password = hash_password(new_password)
        client.send(hashed_password.encode("utf-8"))

    else:
        print("Opção inválida. Desconectando...")
        client.close()
        return

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    while True:
        message = input()
        if message.startswith("/sendfile"):
            _, filepath = message.split(" ", 1)
            send_file(client, filepath)
        else:
            client.send(message.encode("utf-8"))

if __name__ == "__main__":
    start_client()
