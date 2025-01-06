import threading
import socket

alias = input("Choose an alias >>> ")
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1' , 59000))
# create two funct()
# 1) to recv messages from other clients through the server
# 2) to send  messages from other clients through the server
# encode for send and decode for receive
def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "alias?":
                client.send(alias.encode('utf-8'))
            else:
                print(message)
        except:
            print("Error!")
            client.close()
            break

#sending func()
def client_send():
    while True:
        message = f'{alias} : {input("")}'
        client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target= client_send)
send_thread.start()