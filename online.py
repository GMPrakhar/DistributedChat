from socket import *
import time
from threading import *
import json
from tkinter import *

new_users = []

def sendMessage():
    message = {'type':'message', 'from': name, 'message': sendtext.get("1.0", END)}
    message = json.dumps(message)
    cs.sendto(bytes(message, 'utf8'), ('255.255.255.255', 12345))
    sendtext.delete("1.0", END)

def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=200,height=600)


def estabish_connect(user):
    pass

def keep_recieving(s):
    #users.append('Heroshipma')
    #print(users)
    while True:
        m=s.recvfrom(12345)
        incoming_json = json.loads(m[0])
        if incoming_json['type'] == 'connect' and incoming_json['name'] not in [user['name'] for user in users] and incoming_json['name'] not in [user['name'] for user in new_users]:
            print(incoming_json['name'] + " Connected")
            new_users.append({'name': incoming_json['name'], 'time': time.time(), 'socket': m[1]}) 
            ##----------Add users to new_user list if it is not currently added-------

        elif incoming_json['type'] == 'connect':
            for i in range(0, len(users)):
                if users[i]['name'] == incoming_json['name']:
                    users[i]['time'] = time.time()

        elif incoming_json['type'] == 'message':
            txt.insert(END, incoming_json['from']+": "+incoming_json['message'] + " \n")

def ping_network(cs):
    while True:
        cs.sendto(bytes(initialize, 'utf8'), ('255.255.255.255', 12345))
        time.sleep(0.5)

noLabel = None

def draw():
    # if len(users) < 5:
    #     users.append('HIBAMBE')
    # main_window.update()

    for i in range(0, len(users)):
        if time.time() - users[i]['time'] > 5:
            print(users[i]['name'] + " Disconnected")
            users.pop(i)
            main_frame.winfo_children()[i].destroy()

    while len(new_users) != 0:
        new_user = new_users.pop()
        user_btn = Button(main_frame, text = new_user['name'], width=25)
        user_btn.bind('<Button>', lambda connect: estabish_connect(new_user))
        user_btn.pack()
        users.append(new_user)
    
    main_window.after(500, draw)
    

name = input('Enter your Name : ')
#name = "Prakhar"
initialize = json.dumps({"type": "connect", "name": name})
cs = socket(AF_INET, SOCK_DGRAM)
cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
ping_network_thread = Thread(target=ping_network, args=(cs,))
ping_network_thread.start()

s=socket(AF_INET, SOCK_DGRAM)
s.bind(('',12345))

thread = Thread(target=keep_recieving, args=(s,))
thread.start()



users = []

#---------------      GUI      ----------------------------------------------

main_window = Tk()
sizex = 900
sizey = 600
posx  = 100
posy  = 100
main_window.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

left_frame = Frame(main_window, width=50, height=600, bd=1)
left_frame.pack(side="left")

canvas = Canvas(left_frame)
main_frame = Frame(canvas, bg="#FFFFFF")


myscrollbar=Scrollbar(left_frame,orient="vertical",command=canvas.yview, bg="#FFFFFF")
canvas.configure(yscrollcommand=myscrollbar.set)

myscrollbar.pack(side="right",fill="y")
canvas.pack(side="left", expand=1, fill=BOTH)
canvas.create_window((0,0),window=main_frame,anchor='nw')
main_frame.bind("<Configure>",myfunction)

#message_frame = Frame(main_window, size)
main_window.title('Users online')
for user in users:
        user_btn = Button(main_frame, text = user, width=25)
        user_btn.pack()

right_frame = Frame(main_window)
right_frame.pack(side="right")

message_area = Frame(right_frame,bg="#FFFFFF")
message_area.pack(expand=1, fill=BOTH)

scrollbar = Scrollbar(message_area)
scrollbar.pack(side=RIGHT, fill=Y)
txt = Text(message_area, wrap=WORD) # wrap=CHAR, wrap=NONE
txt.pack(expand=1, fill=BOTH)
txt.bind("<Key>", lambda e: "break")
txt.insert(END, "Welcome to Distributed Group Chat! On the left you can see connected users, while in this box you can see incoming messages.\n")

txt.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=txt.yview)

send_area = Frame(right_frame)
send_area.pack()

entryscroll = Scrollbar(send_area)
entryscroll.pack(side=RIGHT, fill=Y)
sendtext = Text(send_area, wrap=WORD, height=6) # wrap=CHAR, wrap=NONE
sendtext.pack(expand=1, fill=BOTH)

sendtext.config(yscrollcommand=entryscroll.set)
entryscroll.config(command=sendtext.yview)

sendbtn = Button(right_frame, text="Send", command=sendMessage)
sendbtn.pack()

main_window.after(500, draw)
main_window.mainloop()
