#                   Modules
#===============================================
import pygame
#Events and Keys
from pygame import (
    K_DOWN,
    K_RIGHT,
    K_LEFT,
    K_UP,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP
)
#Threading
import threading
#system
import sys
#random library
import random
#System function
from os import system
import socket
import pickle
#                   Colors
#===============================================
LIGHTGREEN = (70,255,70)
GREEN = (0,255,0)
DARKLIGHTGREEN = (70,200,70)
DARKGREEN = (0,200,0)
#                   Settings 
#===============================================
#Display of the game
display = pygame.display.set_mode((700,700))
#Title of the window
pygame.display.set_caption("Snake Game")
#Starting pygame
pygame.init()
#                   Classes
#===============================================
#Head
class Head:
    def __init__(self):
        self.head = ""
        #Head coordenates
        self.x = 0
        self.y = 0
        #Direction
        self.right = True
        self.left = False
        self.up = False
        self.down = False
        self.direction = "Right"
        #Iam first?
        self.first = True
        self.color = GREEN
    def draw(self):
        #If i have a head draw it
        if self.head!="":
            self.head.draw()
        #Drawing myself
        if self.color==GREEN:
            pygame.draw.rect(display,(0,255-self.y/20,0),(self.x,self.y,70,70))
            pygame.draw.rect(display,(0,200-self.y/20,0),(self.x,self.y+50,70,20))
        else:
            pygame.draw.rect(display,(70-self.y/20,255-self.y/20,70-self.y/20),(self.x,self.y,70,70))
            pygame.draw.rect(display,(70-self.y/20,200-self.y/20,70-self.y/20),(self.x,self.y+50,70,20))
        #If iam the first head
        if self.first:
            #Draw face
            if self.right:
                pygame.draw.rect(display,(255,255,255),(self.x+50,self.y,20,20))
                pygame.draw.rect(display,(255,255,255),(self.x+50,self.y+30,20,20))
                pygame.draw.rect(display,(0,0,0),(self.x+60,self.y+10,10,10))
                pygame.draw.rect(display,(0,0,0),(self.x+60,self.y+30,10,10))
            elif self.left:
                pygame.draw.rect(display,(255,255,255),(self.x,self.y,20,20))
                pygame.draw.rect(display,(255,255,255),(self.x,self.y+30,20,20))
                pygame.draw.rect(display,(0,0,0),(self.x,self.y+10,10,10))
                pygame.draw.rect(display,(0,0,0),(self.x,self.y+30,10,10))
            elif self.up:
                pygame.draw.rect(display,(255,255,255),(self.x,self.y,25,20))
                pygame.draw.rect(display,(255,255,255),(self.x+45,self.y,25,20))
                pygame.draw.rect(display,(0,0,0),(self.x+45,self.y,15,15))
                pygame.draw.rect(display,(0,0,0),(self.x+10,self.y,15,15))
            else:
                pygame.draw.rect(display,(255,255,255),(self.x,self.y+30,25,20))
                pygame.draw.rect(display,(255,255,255),(self.x+45,self.y+30,25,20))
                pygame.draw.rect(display,(0,0,0),(self.x+45,self.y+35,15,15))
                pygame.draw.rect(display,(0,0,0),(self.x+10,self.y+35,15,15))
            for apple in apples:
                if apple.x==self.x and apple.y==self.y+70 and self.down:
                    pygame.draw.rect(display,(0,0,0),(self.x+25,self.y+50,20,20))
    def update(self,x=0,y=0):
        #Direction
        if self.right:
            self.direction="Right"
        elif self.left:
            self.direction="Left"
        elif self.up:
            self.direction="Up"
        else:
            self.direction="Down"
        #Index of apples
        i = 0
        for apple in apples:
            #If first head is on an apple, add a head,delete the apple
            if apple.x==self.x and apple.y==self.y and self.first==True:
                self.food()
                apples.pop(i)
            #Increment apples index
            i+=1
        #If i have a head,update the head
        if self.head!="":
            self.head.update(self.x,self.y)
        #If i am the first move to directions
        if self.first == True:
            if self.right == True:
                self.x+=70
            elif self.left == True:
                self.x-=70
            elif self.up == True:
                self.y-=70
            elif self.down == True:
                self.y+=70
        #I use my firstest head coords
        else:
            self.x = x
            self.y = y
        #If the first head is out of the game, restart game
        if self.x>=700 or self.x<0 or self.y>=700 or self.y<0:
            start()
        #No description
        if self.first==True and self.head!="":
            if self.head.over_body(self.x,self.y)==True:
                start()
    def food(self):
        #If i have a head i call the self.head.food function
        if self.head!="":
            self.head.food()
        #Else i create a head and i call food function
        else:
            global score
            score+=1
            self.head = Head()
            self.head.first = False
            if self.color==GREEN:
                self.head.color=LIGHTGREEN
            food()
    def over_body(self,x,y):
        if self.x==x and self.y==y:
            return True
        elif self.head!="":
            return self.head.over_body(x,y)
        else:
            return False
#Apple
class Apple:
    def __init__(self,x,y):
        self.x = x
        self.y = y
#                   Variables
#===============================================
#head
head = Head()
#Array of apples
apples = []
#Speed 
Speed=1000
#Menu
menu = "Main Menu"
icon = pygame.image.load("icono.png")
pygame.display.set_icon(icon)
score = 0
#Multiplayer settings
ip = "127.0.0.1"
port = 7777
socket_player = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#                   Draw Text
#===============================================
def draw_text(surface,text,x,y):
    smallfont = pygame.font.SysFont("Corbel",25)
    text = smallfont.render(text,True,(255,255,255))
    surface.blit(text,(x,y))
#                 Draw objects
#===============================================
def draw():
    global menu
    while True:
        #               Main menu
        #=====================================
        if menu=="Main Menu":
            width = display.get_width()
            height = display.get_height()
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == MOUSEBUTTONUP:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    #Button iniciar
                    if x>=width/2-35 and x<=width/2-35+70 and y>=height/2-35 and y<=height/2-35+30:
                        menu = "Game"  
                    elif x>=width/2-35 and x<=width/2-35+70 and y>=height/2-35+70 and y<=height/2-35+100:
                        sys.exit()
                    elif x>=width/2-35 and x<=width/2-35+140 and y>=height/2-35+140 and y<=height/2-35+170:
                        menu="Wifi"
            display.fill((255,255,255))
            #Buttons
            pygame.draw.rect(display,(25,25,25),(width/2-35,height/2-35,70,30))
            draw_text(display,"Iniciar",width/2-35,height/2-35)
            pygame.draw.rect(display,(25,25,25),(width/2-35,height/2-35+70,70,30))
            draw_text(display,"Cerrar",width/2-35,height/2-35+70)
            pygame.draw.rect(display,(25,25,25),(width/2-35,height/2-35+140,70,30))
            draw_text(display,"Wifi",width/2-35,height/2-35+140)
            #Update Display
            pygame.display.update()
        #              Wifi Menu
        #=====================================
        elif menu=="Wifi":
            #Width and height of the display
            width = display.get_width()
            height = display.get_height()
            #Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == MOUSEBUTTONUP:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    if x>=width/2-35 and x<=width/2-35+100 and y>=height/2-35+70 and y<=height/2-35+30+70:
                        menu="Main Menu"
                    elif x>=width/2-35 and x<=width/2-35+100 and y>=height/2-105 and y<=height/2-105+30:
                        create_server()
                        acceptConnectionsThread.start()
                        recieve_serverThread.start()
                    elif x>=width/2-35 and x<=width/2-35+100 and y>=height/2-72 and y<=height/2-72+30:
                        join_server()
            display.fill((255,255,255))
            #Buttons
            pygame.draw.rect(display,(25,25,25),(width/2-35,height/2-35+70,100,30))
            draw_text(display,"Aceptar",width/2-35,height/2-35+70)
            pygame.draw.rect(display,(25,25,25),(width/2-35,height/2-35-70,100,30))
            draw_text(display,"Crear",width/2-35,height/2-35-70)
            pygame.draw.rect(display,(25,25,25),(width/2-35,height/2-72,100,30))
            draw_text(display,"Buscar",width/2-35,height/2-35-37)
            #Update Display
            pygame.display.update()
        #              Game Menu
        #=====================================
        else:
            #Events 
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_DOWN and head.direction!="Up":
                        head.down = True
                        head.up = False
                        head.left = False
                        head.right = False
                    if event.key == K_UP and head.direction!="Down":
                        head.down = False
                        head.up = True
                        head.left = False
                        head.right = False
                    if event.key == K_RIGHT and head.direction != "Left":
                        head.down = False
                        head.up = False
                        head.left = False
                        head.right = True
                    if event.key == K_LEFT and head.direction != "Right":
                        head.down = False
                        head.up = False
                        head.left = True
                        head.right = False
                if event.type == QUIT:
                    sys.exit()
            #Set the color of the window
            for y in range(10):
                for x in range(10):
                    pygame.draw.rect(display,(20-y*2,20-y*2,20-y*2),(x*70,y*70,70,70))
            #Draw the apples
            for apple in apples:
                pygame.draw.rect(display,(255-apple.y/10,0,0),(apple.x,apple.y,70,50))
                pygame.draw.rect(display,(200-apple.y/10,0,0),(apple.x,apple.y+50,70,20))
                pygame.draw.rect(display,(0,255-apple.y/10,0),(apple.x+25,apple.y+20,25,25))
            #Draw the head
            head.draw()
            #Draw the players
            if host:
                for player in players:
                    player["head"].draw()
            else:
                server_player.draw()
            #Draw Score
            draw_text(display,"Score:"+str(score),0,0)
            #Update display
            pygame.display.update()
        #Wait 10 milliseconds
        pygame.time.wait(10)
#                  Update Game
#===============================================
def update():
    while True:
        if menu!="Main Menu":
            #Update the head
            head.update()
            #Wait 1 second
            pygame.time.wait(Speed)
#                Generate apples
#===============================================
def food():
    global Speed
    if Speed>270:
        Speed -= 70
    x = random.randrange(0,10)
    y = random.randrange(0,10)
    apples.append(Apple(x*70,y*70))
#            Start of the program
#===============================================
def start(x=0,y=0):
    #Setting score to 1
    global score
    score = 0
    #Setting Speed to 1000
    global Speed
    Speed = 1000
    #Restart coords
    head.x = x
    head.y = y
    #Restart direction
    head.right=True
    head.left=False
    head.up=False
    head.down=False
    #Deleting heads
    head.head = ""
    #Deleting apples
    for i in range(len(apples)):
        apples.pop(i)
    #Setting the first apple
    food()
#Multiplayer
host = False
players = []
def accept_connections():
    full = False
    while full==False:
        connection,addres = socket_player.accept()
        players.append({head:"","connection":connection})
        full = True
        global menu
        start()
        menu = "Game"
server_player = head
def recieve_data_from_server():
    while True:
        data = socket_player.recv(100000)
        if data:
            data = pickle.loads(data)
            global server_player
            server_player = data
            data = head
            data = pickle.dumps(data)
            socket_player.send(data)    
def recieve_data_from_client():
    while True:
        if len(players)>0:
            for player in players:
                #Enviar coordenadas al cliente
                player["connection"].send(pickle.dumps(head))
                #Recibir coordenadas
                data = player["connection"].recv(100000)
                if data:
                   data = pickle.loads(data)
                   player["head"]=data
                   print(data) 
def create_server():
    global host
    try:
        socket_player.bind((ip,port))
        socket_player.listen(1)
        host = True
        print("Servidor creado!")
    except:
        print("Error en conexión")
def join_server():
    global menu
    try:
        socket_player.connect((ip,port))
        start(0,70)
        menu = "Game"
        recieve_clientThread.start()
        print("Unido al servidor")
    except:
        system("msg * Error en conexión")
        print("Error en conexión")
#                   Threads
#===============================================
updateThread = threading.Thread(target=update)
updateThread.daemon = True
recieve_serverThread = threading.Thread(target=recieve_data_from_client)
recieve_serverThread.daemon = True
recieve_clientThread = threading.Thread(target=recieve_data_from_server)
recieve_clientThread.daemon = True
acceptConnectionsThread = threading.Thread(target=accept_connections)
acceptConnectionsThread.daemon = True
#Starting variables
start()
updateThread.start()
draw()