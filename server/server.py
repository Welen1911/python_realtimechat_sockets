import threading
import socket

# Lista de clientes conectados ao servidor
clientsSingle = dict()
clientsBroad = dict()

# Função para lidar com as mensagens de um cliente
def handle_client_single(client, receiver):
  while True:
      try:
          msg = client.recv(2048)
          single(msg, client, receiver)
      except:
          remove_client_single(client)
          break

def handle_client_broadcast(client):
  while True:
      try:
          msg = client.recv(2048)
          broadcast(msg, client)
      except:
          remove_client_broad(client)
          break


# Função para transmitir mensagens para todos os clientes
def broadcast(msg, sender):
  for client in clientsBroad:
      if clientsBroad[client] != sender:
          try:
              clientsBroad[client].send(msg)
          except:
              remove_client_broad(client)

# Função para transmitir mensagens apenas para um cliente
def single(msg, sender, receiver):
  for name in clientsSingle:
      if clientsSingle[name] != sender and name == receiver:
          try:
              clientsSingle[name].send(msg)
          except:
              remove_client_single(name)

# Função para remover um cliente da lista
def remove_client_single(client):
  clientsSingle.pop(client)

def remove_client_broad(client):
  clientsBroad.pop(client)

# Função principal
def main():
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  print("Iniciou o servidor de bate-papo")

  try:
      server.bind(("0.0.0.0", 7777))
      server.listen()
  except:
      return print('\nNão foi possível iniciar o servidor!\n')

  while True:
      client, addr = server.accept()
      type = client.recv(2048)
      client.send(('ok').encode('utf-8'))
     
      if (type.decode('utf-8') == 'single'):
         
        username = client.recv(2048)
        clientsSingle[username.decode('utf-8')] = client
        print(f'Cliente conectado com sucesso. IP: {addr}')
      
        nomes = ''
        for name in clientsSingle:
            nomes += f'{name}\n'

        client.send(nomes.encode('utf-8'))
        
        receiver = client.recv(2048)

        # Inicia uma nova thread para lidar com as mensagens do cliente
        thread = threading.Thread(target=handle_client_single, args=(client, receiver.decode('utf-8')))
        thread.start()
      
      else :
            
         username = client.recv(2048)
         clientsBroad[username.decode('utf-8')] = client
         print(f'Cliente conectado com sucesso. IP: {addr}')

         thread = threading.Thread(target=handle_client_broadcast, args=(client,))
         thread.start()
         

# Executa o programa
main()