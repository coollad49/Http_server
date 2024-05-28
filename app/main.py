# Uncomment this to pass the first stage
import socket
import threading
import sys

def handle_request(request):
    """
    we're receiving data from the client using the recv method on the client socket. 
    The recv method reads up to 1024 bytes from the client. We then decode this data from bytes to a string using the decode method,
    which converts it to a format we can work with in Python."""
    data :str = request.decode()
    request_data :list[str] = data.split('\r\n')
    
    request_body = request_data[-1]
    print(f"Request_body: {request_body}")
    
    # sends http status message or code
    # client.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

    """
    we're checking if the path extracted from the HTTP request is anything other than the root path '/'. We do this by splitting the first line of the request data on spaces and looking at the second element, which is the path.
    If the path is not '/', we set the response variable to a string that represents a 404 Not Found HTTP response. This string is then encoded into bytes, which is necessary because network communication is done using bytes rather than strings. If the path is '/', the response remains as the 200 OK response set earlier in the code
    """
    method, path, http_version = request_data[0].split(" ")
    

    print(f"Path is {path}\n")
    if path == '/':
        response :bytes = "HTTP/1.1 200 OK\r\n\r\n".encode()
    elif path == '/user-agent':
        user_agent = [data for data in request_data if data[:5] == 'User-'][0].split(" ")[1]
        response :bytes = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode()
    elif '/files' in path:
        if method == 'GET':
            directory = sys.argv[2]
            print(f"Directory: {directory}")
            filename = path[7:]
            print(f"Filename: {filename}")
            try:
                with open(f"/{directory}/{filename}", 'r') as file:
                    print(f"Opened successfully")
                    content = file.read()
                response :bytes = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(content)}\r\n\r\n{content}".encode()
            except Exception as e:
                print(f"Error: Reading /{directory}/{filename} failed. Exception: {e}")
                response :bytes = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        elif method == 'POST':
            directory = sys.argv[2]
            print(f"Directory: {directory}")
            filename = path[7:]
            print(f"Filename: {filename}")
            try:
                with open(f"/{directory}/{filename}", 'w') as file:
                    print("Opened Successfully")
                    file.writelines(request_body)
                response :bytes = f"HTTP/1.1 201 Created\r\n\r\n".encode()
            except Exception as e:
                print(f"Error: Reading /{directory}/{filename} failed. Exception: {e}")
                response :bytes = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

    elif path.startswith('/echo'):
        encoding_Accepted = "".join([item for item in request_data if item[:8] == "Accept-E"])
        encoding_Accepted = encoding_Accepted.split(" ")
        _, *encodes = encoding_Accepted
        encodes = [item.rstrip(',') for item in encodes]
        unknown_path = path[6:]
        if 'gzip' in encodes:
            response :bytes = f"HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\nContent-Type: text/plain\r\nContent-Length: {len(unknown_path)}\r\n\r\n{unknown_path}".encode()
        else:
            response :bytes = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(unknown_path)}\r\n\r\n{unknown_path}".encode()

    else:
        response :bytes = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

    return response

def handle_clients(client):
    while True:
        request = client.recv(1024)

        if not request:
            break
        response = handle_request(request)
        client.send(response)

    client.close()

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221))
    print("Server started. Listening for connections....")

    while True:
        client, address = server_socket.accept() # wait for client
        print(f"Accepted connection from {address}\n")
        threading.Thread(target=handle_clients, args=(client,)).start()



if __name__ == "__main__":
    main()
