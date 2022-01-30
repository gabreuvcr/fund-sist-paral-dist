from sys import argv

import socket
import grpc

from protos import peer_pb2, peer_pb2_grpc

def localhost_to_fqdn(service_id):
    return service_id.replace("localhost", socket.getfqdn())

def run():
    #string identificador de um serviço
    service_id = argv[1]

    #se o service_id passado como argumento for localhost,
    #altera o localhost pelo fqdn
    if service_id.startswith("localhost"):
        service_id = localhost_to_fqdn(service_id)

    channel = grpc.insecure_channel(service_id)

    stub = peer_pb2_grpc.PeerServerStub(channel)

    while True:
        #le o input do usuario
        client_input = input()

        #verifica se o comando é I
        if client_input.startswith('I'):
            #se nao tiver 3 campos separados por virgula, volta para o loop
            if len(client_input.split(',')) != 3: continue

            command, key, value = client_input.split(',')

            #envia para o servidor de pares uma chave e um valor para armazenar
            #no seu dicionario e imprime o valor de retorno
            response = stub.insert(peer_pb2.InsertRequest(key = int(key), value = value))
            print(response.retval)

        #verifica se o comando é C
        elif client_input.startswith('C'):
            #se nao tiver 2 campos separados por virgula, volta para o loop
            if len(client_input.split(',')) != 2: continue
            
            command, key = client_input.split(',')

            #envia para o servidor de pares uma chave e recebe como retorno
            #o valor correspondente, que será impresso
            #se o retorno for um string vazio, imprime apenas uma nova linha vazia
            response = stub.query(peer_pb2.QueryRequest(key = int(key)))
            print(response.retval)

        #verifica se o comando é A
        elif client_input.startswith('A'):
            #se nao tiver 2 campos separados por virgula, volta para o loop
            if len(client_input.split(',')) != 2: continue
            
            command, center_service_id = client_input.split(',')

            #se o service_id passado como input for localhost,
            #altera o localhost pelo fqdn
            if (center_service_id.startswith("localhost")):
                center_service_id = localhost_to_fqdn(center_service_id)

            #envia para o servidor de pares um string indentificador de serviço para
            #que registre suas chaves em um servidor centralizador, imprime o numero de chaves
            #registradas pelo servidor centralizador
            response = stub.active(peer_pb2.ActiveRequest(service_id = center_service_id))
            print(response.retval)

        #verifica se o comando é T
        elif client_input.startswith('T'): 
            #termina a execucao do servidor de pares e imprime 0
            #e finaliza sua execução           
            response = stub.end(peer_pb2.EmptyRequest())
            print(response.retval)
            break

    channel.close()

if __name__ == '__main__':
    try:
        run()
    except (grpc._channel._InactiveRpcError, EOFError):
        #Servidor foi finalizado ou input do client foi um EOF
        exit()
    except Exception as e:
        print(e.with_traceback())
