import socket, threading
import getpass

def sendrecv():
    while True:
        data = sock.recv(1024)
        if data is not '':
            print data
        else:
            pass

def Main():
    global sock
    sock = socket.socket()
    HOST = 'duke5010.duckdns.org'
    PORT = 8080
    sock.connect((HOST, PORT))
    print ' [+] Connected to server!'
    username = raw_input(' Please Enter your Username: ')
    sock.send(username)
    password =raw_input(' >> ')#getpass.getpass( ' Enter your password: ')
    sock.send(password)
    print ' [+] Authenticating...' 
    if sock.recv(1) == 'S':
        print ' [+] Authentication Sucess!'
    elif sock.recv(1) == 'F':
        quit(' [-] Error!')
    while True:
        thread = threading.Thread(target=sendrecv)
        thread.start()
        msg = raw_input('msg >> ')
        sock.send(msg)
if __name__ == '__main__':
    Main()
