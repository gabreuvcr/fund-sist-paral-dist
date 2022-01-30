from sys import argv

import socket
import grpc

from protos import center_pb2, center_pb2_grpc, peer_pb2, peer_pb2_grpc

def localhost_to_fqdn(service_id: str):
    return service_id.replace("localhost", socket.getfqdn())

def run():
    #string identificador de serviço
    service_id = argv[1]

    #se o service_id passado como argumento for localhost,
    #altera o localhost pelo fqdn
    if service_id.startswith("localhost"):
        service_id = localhost_to_fqdn(service_id)

    channel = grpc.insecure_channel(service_id)

    stub = center_pb2_grpc.CenterServerStub(channel)

    while True:
        #le o input do usuario
        client_input = input()

        #verifica se o comando é C
        if client_input.startswith('C'):
            #se nao tiver 2 campos separados por virgula, volta para o loop
            if len(client_input.split(',')) != 2: continue
            
            command, key = client_input.split(',')
            
            #envia para o servidor centralizador a chave que deseja consultar,
            #caso ela não exista, receberá um string vazio, imprimindo uma
            #nova linha vazia e voltando para o loop, se existir, receberá o 
            #string identificador de serviço de um servidor de pares
            response = stub.mapping(center_pb2.MappingRequest(key = int(key)))
            
            #se o retorno for um string vazio, imprime uma nova linha vazia
            #e segue para o proximo comando
            if response.retval == '':
                print('')
                continue

            #se conecta ao servidor de pares com o string
            #identificador retornado pelo servidor centralizador
            #e realiza uma consulta enviando a mesma chave, recebendo o valor
            channel_peer = grpc.insecure_channel(response.retval)
            stub_peer = peer_pb2_grpc.PeerServerStub(channel_peer)

            response_peer = stub_peer.query(peer_pb2.QueryRequest(key = int(key)))

            #imprime o string do serviço e o valor retornado pelo servidor de pares
            print(f"{response.retval}:{response_peer.retval}")

        #verifica se o comando é T
        elif client_input.startswith('T'): 
            #termina a execucao do servidor centralizador, imprime o numero
            #de chaves que estavam salvas no servidor e finaliza sua execução              
            response = stub.end(center_pb2.EmptyRequest())
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
