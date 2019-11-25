#server.py
#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
player1 = None
player2 = None

import socket
import threading
import socketserver
import pickle
import time

# assume 2 players
players = []
loc_A = []
loc_B = []
port_A = None
port_B = None
ip_A = None
ip_B = None
last_positions = []

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # cur_thread2 = threading.current_thread() #get current thread
        # print("current_thread2.name = ", cur_thread2.name)
        data = self.request.recv(1024)
        data = pickle.loads(data)   #type list
        print("self.server = ",self.server.fileno())
        print("data recv = ",data)
        cli_addr = self.client_address  #get client address in TCP connection
        # print("Address ", cli_addr[0])
       
        
        # data.insert(len(data), cli_addr[0])
        # data.insert(len(data), cli_addr[1])
        self.add_players(data)
        print("loc_A ******", loc_A)
        # time.sleep(1)
        #all other threads
        cur_thread = threading.current_thread() #get current thread fd
        print("current_thread.name = ", cur_thread.name)
        # response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
        # response = pickle.dumps(data)
        # self.request.sendall(response)
        self.before_sendall()
        print("----------------------------------------------------")
        
    def before_sendall(self):
        print("loc_A &&&&", loc_A)
        gamestate = []
        gamestate.extend((loc_A,loc_B))
        print("gamestate",gamestate)
        response = pickle.dumps(gamestate)
        self.request.sendall(response)
        
    def add_players(self, addr_data):
        # print("players list = ", players)
        print("addr_data =", addr_data)
        print("addr_data[0]", addr_data[0]) #players name
        if len(players) == 2:
            self.loop_over_list(addr_data)
        elif len(players) < 2:
            if addr_data[0] not in players:
                players.append(addr_data[0])
            pos_index_players = players.index(addr_data[0])
            print("pos_index_players =", pos_index_players)
            if pos_index_players == 0:
                global loc_A
                loc_A.clear()
                loc_A.extend(addr_data[:])
                # print("33333333addr_data[1:]", addr_data[1:])
                print("loc_A ", loc_A)
            elif pos_index_players == 1:
                global loc_B
                loc_B.clear()
                loc_B.extend(addr_data[:])
    
    def loop_over_list(self, addr_data):
        print("inside loop_over_list")
        pos_index_players = players.index(addr_data[0])
        print("pos_index_players =", pos_index_players)
        if pos_index_players == 0:
            global loc_A
            loc_A.clear()
            loc_A.extend(addr_data[:])
            # print("33333333addr_data[1:]", addr_data[1:])
            print("loc_A ", loc_A)
        elif pos_index_players == 1:
            global loc_B
            loc_B.clear()
            loc_B.extend(addr_data[:])
            
            
            
            
        
        
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer): pass
   
if __name__ == "__main__":
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

    ip, port = server.server_address
    print("ip = ", ip, " port = ", port)
    print("file descriptor nr = ", server.fileno())
    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = False
    
    server_thread.start()
    
    print("Server loop running in thread:", server_thread.name)

    # client(ip, port, "Hello World 1")
    # client(ip, port, "Hello World 2")
    # client(ip, port, "Hello World 3")
    # server.server_close()
    # server.shutdown()
