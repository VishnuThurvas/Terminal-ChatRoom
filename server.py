import socket
import threading
# from encodings.aliases import aliases

host = ${local_machine_ip}
port = ${port_number}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()
clients = []
aliases = []


#this broadcast message is sending a message to all connected clients
def broadcast(message):
    for c in clients:
        c.send(message)


#a func() to get message from clientA and send to clientB
def handle_client(client):
    while True:
        try:
            message = client.recv(1024) #message received  from the client , with a maximum no. of bytes that a server could recv() from a client
            broadcast(message) #sending to all other clients
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room'.encode('utf-8'))
            aliases.remove(alias) # Successfully removed from clientList and aliasesList
            break


#Main function to receive the clients connection
def receive():
    while True:
        print("Server is running and listening......")
        client , address = server.accept()  #returns two parameters
        print(f"Connection is established with {str(address)}")
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        #TO display in my server
        print(f'The alias of this client is {alias}'.encode('utf-8'))

        #Invoke BroadCast - To Say the new client has joined the chatRoom
        broadcast(f'{alias} has connected to the chat room'.encode('utf-8'))

        #From the server to client - Saying You are now Connected
        client.send('You are now connected !'.encode('utf-8'))


#to work with handle_client() we need to run by threading
#Obj creation of thread class
        thread = threading.Thread(target = handle_client , args = ( client, ))
        thread.start()

#invoke that receive
if __name__ == "__main__":
    receive()
