#game.py
from tkinter import Tk, Canvas, Button, Entry, StringVar, Label
import time
from client import Client
import pickle

class Gui():
    def __init__(self, master):
        self.master = master
        self.str_var = StringVar()
        self.create_widgets()
        self.player = None
        self.player_pos = None
        self.enemy = None
        self.enemy_pos = None
        self.list_pos_player = None
        self.run = True
        self.cli = Client()
        self.HOST = '127.0.0.1'  # The server's hostname or IP address
        self.PORT = 65432        # The port used by the server
        self.player_name = None
        
        
    def create_widgets(self):
        self.can = Canvas(self.master)
        self.can.pack()
        self.butt_left = Button(self.master, text="left",
                                command=self.move_left)
        self.butt_left.pack(side="left")
        self.butt_right = Button(self.master, text="right",
                                command=self.move_right)
        self.butt_right.pack(side="right")
        self.butt_start = Button(self.master, text="Start",
                                command=self.start)
        self.butt_start.pack()
        self.ent_name = Entry(self.master, textvariable=self.str_var)
        self.ent_name.pack()
        self.info = Label(self.master, text="None")
        self.info.pack()
        self.ent_name.focus()
        
    def start(self):
        if self.str_var.get() == "":
            print("str_var is empty")
            self.info.configure(text="set players name first")
            return
        if self.player:
            print("player exist")
            return
        else:
            self.player = self.can.create_rectangle(50, 25, 150, 75, fill="blue")
            print("self.player begin", self.player)
            self.player_name = self.str_var.get()
            self.enemy = self.can.create_rectangle(50, 25, 150, 75, fill="red")
            print("self.enemy",self.enemy)
            print("player created")
            
    def parse_response(self, response):
        """get and set postion of player and enemy"""
        print("-----------++++++++++", self.player_name)
        print("response =", response)
        # index = response[0][0].index(self.player_name)
        if self.player_name in response[0]:
            print("yes it is 1")
            self.list_pos_player = 0
            self.player_pos = response[0][1:]
            print("self.player_pos = ",self.player_pos)
            if response[1]:
                self.enemy_pos = response[1][1:]
            
        elif self.player_name in response[1]:
            print("yes it is 2")
            self.list_pos_player = 1
            if not response[1]:
                print("list is empty")
                return
            else:
                self.player_pos = response[1][1:]
                self.enemy_pos = response[0][1:]
   

        print("self.player position = ", )
        print("self.enemy position = ", )
        
    def get_pos(self, id):
        return self.can.coords(id)
    
    def set_pos(self, pos, pos2):
        self.can.move(self.player, pos)
        self.can.move(self.enemy, pos2)
    
    def send_data(self):
        pos = self.get_pos(self.player)
        pos.insert(0,self.str_var.get())
        data=pickle.dumps(pos)
        try:
            response = self.cli.client(self.HOST, self.PORT, data) #send and recieved
            print("+++++++++++++")
            self.parse_response(response)
            print("middle")
            print("sefl.player 455", self.player)
            self.set_all_g_objects()
            print("+++++++++++++")
        except Exception as e:
            print("Connection problems, App shutted down", e)
            self.master.destroy()
            
    def set_all_g_objects(self):
        
        print("self.player_pos 33333", self.player_pos)
        print("player set_all_g_objects", self.player, type(self.player))
        print("self.player_pos", self.player_pos)
        try:
            l = [10,20]
            self.can.coords(self.player, self.player_pos[0], self.player_pos[1],
                            self.player_pos[2], self.player_pos[3])
            if self.enemy_pos:                
                self.can.coords(self.enemy, self.enemy_pos[0], self.enemy_pos[1],
                                self.enemy_pos[2], self.enemy_pos[3])
        except Exception as e:
            print(e)
        
        
    def get_player_name(self):
        pass
        
    def passing(self):
        pass
    
    def get_enemy_pos(self):
        pass
        
    def move_right(self):
        print("+right")
        if self.player:
            self.can.move(self.player, 10,0)  
            pass
        self.send_data()
        
    def move_left(self):
        print("+left")
        if self.player:
            print("player id =", self.player)
            self.can.move(self.player, -10,0)  
        self.send_data()
        
    def loop(self):
        while self.run:
            processInput();
            update();
            render();
            time.sleep(160)
        
if __name__ == "__main__":
    root = Tk()
    app = Gui(root)
    root.mainloop()