import threading
import socket

# Lista de clientes conectados ao servidor
clients = dict()

# Função para lidar com as mensagens de um cliente
def handle_client(client, receiver):
  while True:
      try:
          msg = client.recv(2048)
          single(msg, client, receiver)
      except:
          remove_client(client)
          break

# Função para transmitir mensagens para todos os clientes
def broadcast(msg, sender):
  for client in clients:
      if client != sender:
          try:
              client.send(msg)
          except:
              remove_client(client)

# Função para transmitir mensagens apenas para um cliente
def single(msg, sender, receiver):
  for name in clients:
      if clients[name] != sender and name == receiver:
          try:
              clients[name].send(msg)
          except:
              remove_client(name)

# Função para remover um cliente da lista
def remove_client(client):
  clients.pop(client)

# Função principal
def main():
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  print("Iniciou o servidor de bate-papo")

  try:
      server.bind(("localhost", 7777))
      server.listen()
  except:
      return print('\nNão foi possível iniciar o servidor!\n')

  while True:
      client, addr = server.accept()
      username = client.recv(2048)
      clients[username.decode('utf-8')] = client
      print(f'Cliente conectado com sucesso. IP: {addr}')

      nomes = ''
      for name in clients:
        nomes += f'{name}\n'

      client.send(nomes.encode('utf-8'))
        
      receiver = client.recv(2048)

      # Inicia uma nova thread para lidar com as mensagens do cliente
      thread = threading.Thread(target=handle_client, args=(client, receiver.decode('utf-8')))
      thread.start()

# Executa o programa
main()