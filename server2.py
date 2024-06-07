import socket
import threading
import os


def handle_request(client_connection):
    request = client_connection.recv(1024).decode()
    print(request)

    # Parsing HTTP request
    request_line = request.splitlines()[0]
    filename = request_line.split()[1]

    # Remove leading slash
    if filename == '/':
        filename = '/index.html'
    filename = filename[1:]

    try:
        # Read the requested file
        with open(filename, 'rb') as f:
            response_body = f.read()
        response_header = 'HTTP/1.1 200 OK\n\n'
    except FileNotFoundError:
        response_header = 'HTTP/1.1 404 Not Found\n\n'
        response_body = b'404 Not Found'

    response = response_header.encode() + response_body
    client_connection.sendall(response)
    
    client_connection.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8003))
    server_socket.listen(5)
    print('Server is running on port 8003...')

    while True:
        client_connection, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_request, args=(client_connection,))
        client_thread.start()


main()
