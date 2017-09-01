import socket
import threading
import os, sys
import time
from solography import *

address = '192.168.1.100'
PORT = 8080
global save_file
save_file = 'logs.log'
authfilepath = 'auth.solo'

def processtuple(tupleobj):
    tupleobj = str(tupleobj)
    dat = tupleobj.rstrip(')')
    dat = tupleobj.lstrip('(')
    addr = dat.split(', ')[0]
    port = dat.split(', ')[1]
    return addr, port

def processdata(data):
    data = data.rstrip(' ')
    data = data.lstrip(' ')
    return data
    
if os.path.isfile(save_file) == False:
    open(save_file, 'w').write('')
if os.path.isfile(authfilepath) == False:
    open(authfilepath).write('')

def shutdown():
    writelog(' [-] Shutting down at %s' % str(time.ctime()))
    writelog('\n\n')
    writelog('\n\n============================================================================\n\n')
    sock.close()
    print ' [.] Shutting down at %s' % str(time.ctime())

def writelog(data):
                log_file = open('logs.log', 'r')
                buf = log_file.read()
                log_file.close()
                log_file = open('logs.log', 'w')
                buf += data+'\n'
                log_file.write(buf)
writelog('\n\n============================================================================\n\n')

writelog(' Started at '+str(time.ctime()))
def authenticate(c, addr):
    addr, port = processtuple(addr)
    writelog(' [*] Connection from ' + str(addr)+ port + ' at ' + str(time.ctime()))
    print ' [*] Authentication request from ' + str(addr)
    USER = c.recv(1024).rstrip('\n\r')
    print 'user : ' + USER
    PASSWORD = c.recv(1024).rstrip('\n\r')
    print 'pass : ' + PASSWORD
    c.sendall(' Authentication under process...')
    authname = USER+':'+PASSWORD
    authfile = open(authfilepath, 'r')
    authentication_status = False
    print authname
    for lines in authfile:
        lines = lines.rstrip('\n')
        if (lines == authname) == True:
            print ' [+] Found!'
            authentication_status = True
            break
        else:
            print 'user not found'
    if authentication_status == False:
        writelog(' [*] Authentication failed for user %s ' % str(addr))
        c.sendall('F')
        print 'Authentication Failed! for user ' + str(addr)
        return False
    elif authentication_status == True:
        iThread = threading.Thread(target = newrecv, args = (c, addr))
        iThread.start()
        addrlist.append(addr)
        writelog('Authentication sucess for user ' + str(addr) + ' at ' + str(time.ctime()))
        print ' [+] Authentication sucessful for user ' + str(addr)
        c.sendall('S')
        return True
        
def send():
        while True:
                msg = raw_input('msg >> ')
                if msg == '':
                    pass
                elif msg == 'shutdown code 000':
                    for connection in connections:
                        try:
                            connection.send('\n Server is Shutting down at %s \n Have a Nice Day! :) ' % str(time.ctime()))
                        except:
                            print ' [!] Error sending to Connection ', connection
                            print ' [*] Removing from Conn list'
                            numbr = connections.index(connection)
                            connections.remove(connection)
                            addrlist.pop(numbr)
                    shutdown()
                else:
                    writelog(' Admin >> ' + msg)
                    for connection in connections:
                        try:
                            connection.send('\nAdmin: ' + str(msg).rstrip('\n'))
                        except:
                            print ' [!] Error sending to Connection ', connection
                            print ' [*] Removing from Conn list'
                            numbr = connections.index(connection)
                            connections.remove(connection)
                            addrlist.pop(numbr)

def newrecv(conn, addr):
    while True:
                data = decrypt(conn.recv(1024), 12)
                data = processdata(data)
                datafrom = str(addrlist[connections.index(c)])
                writelog(' [*] ' + str(addrlist[connections.index(c)]) + ' : ' + str(data))
                if data == '':
                            print ' [!] Error sending to Connection ', e
                            writelog(' [*] ' + datafrom + ' Have exited the chat room! \n')
                            print ' [*] Removing from Conn list'
                            numbr = connections.index(connection)
                            connections.remove(connection)
                            addrlist.pop(numbr)
                if data is not '' or '\n' or '\r':    
                    print '\n ' + data
                    for connection in connections:
                        try:
                            connection.send(encrypt(data, 12))
                        except Exception as e:
                            print ' [!] Error sending to Connection ', e
                            #writelog(' [-] Error! Removing user ' + str(addrlist(int(connections.index(c)))))
                            print ' [*] Removing from Conn list'
                            numbr = connections.index(connection)
                            connections.remove(connection)
                            addrlist.pop(numbr)
def sendrecv():
    while True:
        for connection in connections:
            try:
                data = connection.recv(1024)
                data = processdata(data)
                datafrom = str(addrlist[connections.index(c)])
                writelog(' [*] ' + str(addrlist[connections.index(c)]) + ' : ' + str(data))
                if data == '':
                            print ' [!] Error sending to Connection ', e
                            writelog(' [*] ' + datafrom + ' Have exited the chat room! \n')
                            print ' [*] Removing from Conn list'
                            numbr = connections.index(connection)
                            connections.remove(connection)
                            addrlist.pop(numbr)
                if data is not '' or '\n' or '\r':    
                    print '\n ' + data
                    for connection in connections:
                        try:
                            connection.send(data)
                        except Exception as e:
                            print ' [!] Error sending to Connection ', e
                            #writelog(' [-] Error! Removing user ' + str(addrlist(int(connections.index(c)))))
                            print ' [*] Removing from Conn list'
                            numbr = connections.index(connection)
                            connections.remove(connection)
                            addrlist.pop(numbr)
            except:
                pass
                
def listener():
        global c, addrlist, connections, useraddr
        addrlist = []
	sock = socket.socket()
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	address = 'localhost'
	sock.bind((address, PORT))
	connections = []
	useraddr = {}
	sock.listen(100)
	print ' [*] Listening...'
	try:
                while True:
                	c, addr = sock.accept()
                	if authenticate(c, addr) == True:
                            useraddr.update({c:str(addr)})
                            connections.append(c)
                            #thread = threading.Thread(target=sendrecv)
                            #thread.start()
                            #3thread1 = threading.Thread(target=send)
                            #thread1.start()
                        else:
                            pass
        except KeyboardInterrupt:
                sock.close()
                print (' [!] Quitting...')
                sys.exit[-1]
if __name__ == '__main__':
    listener()
