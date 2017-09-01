import socket, threading
from ScrolledText import ScrolledText
import getpass
import sys
from solography import *
from Tkinter import *
import ttk
import GUI_support
from pygame import mixer

def play():
    mixer.init()
    sound = mixer.Sound('notify.wav')
    sound.play()

w = None
def destroy_Solo_Client():
    global w
    w.destroy()
    w = None
    
global username, password

def Authenticate(user, password):
    global username
    username = user
    sock.send(user)
    sock.send(password)
    print sock.recv(1224)
    opt = sock.recv(1024)
    global opt
    print opt
    if opt == 'S':
        print ' [+] Connected!'
        login.destroy()
        Main()
        while True:
            msg = sock.recv(1024)
            print msg
            print msg
            statemsg(msg)
        return True
    elif opt == 'F':
        print ' [-] Failed'
        return False

sock = socket.socket()
host = '127.0.0.1'
port = 8080
sock.connect((host, port))

def asend(a='Null'):
    data = top.Entry1.get()
    data = data.rstrip(' ')
    data = data.lstrip(' ')
    if data is not '':
        data = encrypt(username + ' >> ' +data, 12)
        sock.send(data)
        print data
        top.Text1.yview(END)
        top.Entry1.delete(0, END)
        top.Entry1.insert(0, '')
    else:
        pass

class Solo_Client:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85'
        top.iconbitmap(r'icon.ico')
        top.geometry("346x463+655+389")
        top.title("Solo Client")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")
        top.resizable(True, True)
        top.bind('<Return>', asend)
        self.menubar = Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.Entry1 = Entry(top)
        self.Entry1.place(relx=0.03, rely=0.91, relheight=0.06, relwidth=0.71)
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(highlightbackground="#d9d9d9")
        self.Entry1.configure(highlightcolor="black")
        self.Entry1.configure(insertbackground="black")
        self.Entry1.configure(selectbackground="#c4c4c4")
        self.Entry1.configure(selectforeground="black")

        self.Button1 = Button(top)
        self.Button1.place(relx=0.78, rely=0.91, height=34, width=67)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Send''')
        self.Button1.configure(command = asend)


        self.Text1 = ScrolledText(top)
        self.Text1.place(relx=0.03, rely=0.02, relheight=0.87, relwidth=0.93)
        self.Text1.configure(background="white")
        self.Text1.configure(font="TkTextFont")
        self.Text1.configure(foreground="black")
        self.Text1.configure(highlightbackground="#d9d9d9")
        self.Text1.configure(highlightcolor="black")
        self.Text1.configure(insertbackground="black")
        self.Text1.configure(insertborderwidth="3")
        self.Text1.configure(selectbackground="#c4c4c4")
        self.Text1.configure(selectforeground="black")
        self.Text1.configure(undo="1")
        self.Text1.configure(width=10)
        self.Text1.configure(wrap=NONE)

        
def statemsg(msg):
    top.Text1.configure(state=NORMAL)
    top.Text1.insert(END, msg+'\n')
    top.Text1.configure(state=DISABLED)

def sendrecv():
    while True:
        data = decrypt(sock.recv(1024), 12)
        if data is not '':
            print '\n' + data
            statemsg(data)
            play()
        else:
            pass

def Main():
    iThread = threading.Thread(target=sendrecv)
    iThread.start()
    vp_start_gui()

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root, top
    root = Tk()
    top = Solo_Client (root)
    GUI_support.init(root, top)
    root.mainloop()

def loginbutton():
    username = login.entry_1.get()
    password = login.entry_2.get()
    if Authenticate(username, password) == True:
        Main()
        login.destroy()
    else:
        quit()
    Main()

login = Tk()
login.title('Login.')
login.geometry('250x150')
login.label_1 = Label(text="Username")
login.label_2 = Label(text="Password")
login.entry_1 = Entry()
login.entry_2 = Entry(show="*")
login.label_1.grid(row=0, sticky=E)
login.label_2.grid(row=1, sticky=E)
login.entry_1.grid(row=0, column=1)
login.entry_2.grid(row=1, column=1)
login.logbtn = Button( text="Login", command = loginbutton)
login.logbtn.grid(columnspan=2)
login.mainloop()
