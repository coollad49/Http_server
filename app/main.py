# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221))
    client, address = server_socket.accept() # wait for client
    print(f"Accepted connection from {address}\n")
    
    """
    we're receiving data from the client using the recv method on the client socket. 
    The recv method reads up to 1024 bytes from the client. We then decode this data from bytes to a string using the decode method,
    which converts it to a format we can work with in Python."""
    data :str = client.recv(1024).decode()
    request_data :list[str] = data.split('\r\n')
    
    # sends http status message or code
    # client.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

    """
    we're checking if the path extracted from the HTTP request is anything other than the root path '/'. We do this by splitting the first line of the request data on spaces and looking at the second element, which is the path.
    If the path is not '/', we set the response variable to a string that represents a 404 Not Found HTTP response. This string is then encoded into bytes, which is necessary because network communication is done using bytes rather than strings. If the path is '/', the response remains as the 200 OK response set earlier in the code
    """
    path = request_data[0].split(" ")[1]
    print(f"Path is {path}\n")
    if path == '/':
        response :bytes = "HTTP/1.1 200 OK\r\n\r\n".encode()
    elif path == '/user-agent':
        user_agent = [data for data in request_data if data[:5] == 'User-'][0].split(" ")[1]
        response :bytes = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode()
    
    elif path.startswith('/echo'):
        unknown_path = path[6:]
        response :bytes = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(unknown_path)}\r\n\r\n{unknown_path}".encode()
    else:
        response :bytes = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
    
    client.send(response)
    client.close()
    server_socket.close()


if __name__ == "__main__":
    main()
