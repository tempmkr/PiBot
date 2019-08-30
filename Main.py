import threading
from Sense import *
from DataLink import *
from Move import *
from DataLink import *
import time


'''
3 classes holding the 3 threads that will be running
Move will decide upon movement 
Sense will retreive sensor Data
Data will deliver Data to Server


More Threads:

- Battery voltage thread
- Current usage thread
- Periphery Control thread : lights, guns, etc.
- Second or more sensing thread : rotary encoder

'''




'''
A 100 long array of Measurement values will be created and
updated, so that the newest value is at the very end. 

[ [l,m,r], [l,m,r], ... , ... ]

Initially the program will accumulate a list of 100 measurements without removing any
after that it will enter a while-loop that will always pop element 0 after an element is added.
The idea is to dynamically limit the list to 100 elements. 
Otherwise it would become huge!

'''


class senseThread1(threading.Thread):

    def run(self):
        sensor = Sensor(26, 19, 13, 21, 20, 16)

        global senseData
        senseData = []

        counter = 0

        while counter < 100:
            senseData.append(sensor.distance_us())
            counter += 1

        while True:
            senseData.append()
            senseData.pop(0)

'''
class dataThread(threading.Thread):

    def run(self):
        socketStart()

'''

class moveThread(threading.Thread):

    def run(self):
        M = Move(8, 25, 24, 23, 27, 22, 18)

        time.sleep(1)

        tmp = senseData[-1]

        if tmp[0] > 10 and tmp[1] > 10 and tmp[2] > 10:
            M.straight()
            tmp = senseData[-1]

        while tmp[0] > 10 and tmp[1] > 10 and tmp[2] > 10:
            tmp = senseData[-1]
            print (tmp)

        M.stop()

        print(tmp)


class dataSendLink(threading.Thread):
    def run(self):


        '''
        This thread will be continuously sending data over to any client
        that conects to it
        Argument 1 : IPV4 or whatever protocoll, no idea why that name...
        Argument 2 : TCP/UDP or whatever protocoll, chose TCP
        '''
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        '''
        this might return 127.0.0.1 which would be useless. 
        so maybe us the function below
        '''

        IP = socket.gethostname()

        '''
        IP = get_ip()
        '''

        PORT = 3000
        HEADERSIZE = 10

        #trying to bind the port and ip to the socket

        try:
            s.bind((IP, PORT))
            print("binding successfull")

        except socket.error as msg:

            print("Binding failed. Error Code: " + str(msg[0]) + " Message: " + msg[1])
            sys.exit()

        s.listen(5)
        print(f"listening for connections on port : {PORT}")

        connectedAddresse = []

        while True:

            '''
            continuously sending the last senseData to the client
            tupple unpacking: reference clientSocket to object clientsocket
            And keeping the address for security and debugging
            '''

            clientSocket, address = s.accept()
            connectedAddresse.append(address)

            print("Connection from " + address + " has been established!")

            data = {"senseData": senseData[-1]}

            #pickle so that the data can easily be used on client,
            # no need to convert strings and bytes, especially interesting
            # for more and different data

            msg = pickle.dumps(data)

            #converting the overhead to bytes.
            #the header will store the message length and be of a fixed size.
            #aftert the header the will be the message.

            msg = bytes('{:<10}'.format(len(msg)), "utf-8") + msg

            #sending the message over to the connected socket. clientSocket
            clientSocket.send(msg)





class interrupt(threading.Thread):

    def run(self):
        k = input()

        move.join()
        senseDistance.join()


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


senseDistance = senseThread1()
move = moveThread()
dataL = dataSendLink()

senseDistance.start()
dataL.start()
move.start()







