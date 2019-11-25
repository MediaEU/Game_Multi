#client.py
import socket
import pickle
#test
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

class Client():
    def __init__(self):
        self.response = None
        
 
    def client(self,ip, port, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, port))
            print("type of message ", type(message))
            sock.sendall(message)
            
            
            response = sock.recv(1024)
            response = pickle.loads(response)
            self.response = response
            
            print("Received: {}".format(response))
        return response

if __name__ == "__main__":
    c = Client()
    c.client(HOST, PORT, "Hello World 1")
