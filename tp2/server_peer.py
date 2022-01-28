from concurrent import futures
from sys import argv

import threading
import socket

import grpc

from protos import peer_pb2, peer_pb2_grpc, center_pb2, center_pb2_grpc

class PeerServer(peer_pb2_grpc.PeerServerServicer):
    def __init__(self, stop_event, service_id, flag):
        self._stop_event = stop_event
        self.service_id = service_id
        self.flag = flag
        self.dictionary = dict()

    def insert(self, request, context):
        #se a key já estiver no dict, retorna -1
        if request.key in self.dictionary: 
            return peer_pb2.IntReply(retval = -1)

        #se não estiver no dict, entao armazena a chave e valor
        #e retorna 0
        self.dictionary[request.key] = request.value
        return peer_pb2.IntReply(retval = 0)

    def query(self, request, context):
        #se a key existir no dict, retorna o valor associado
        if request.key in self.dictionary:
            return peer_pb2.StringReply(retval = self.dictionary[request.key])
        
        #se nao existir, retorna uma string nula
        return peer_pb2.StringReply(retval = '')
    
    def active(self, request, context):
        #se o programa tiver apenas um argumento, retorna 0
        if not self.flag:
            return peer_pb2.IntReply(retval = 0)

        #caso tenha 2 ou mais argumentos, entao abre uma conexao
        #com o servidor centralizador e registra suas keys associadas ao
        #string identificador do seu serviço, retorna o valor de 
        #keys que foram registradas
        channel_center = grpc.insecure_channel(request.service_id)
        stub_center = center_pb2_grpc.CenterServerStub(channel_center)

        response_center = stub_center.register(center_pb2.RegisterRequest(service_id = self.service_id, keys = self.dictionary.keys()))
        return peer_pb2.IntReply(retval = response_center.retval)

    def end(self, request, context):
        #se algum cliente utilizar o comando T, o servidor
        #termina sua execução liberando o stop_event.wait() e retorna 0
        self._stop_event.set()
        return peer_pb2.IntReply(retval = 0)


def serve():
    #string identificador de um serviço
    service_id = socket.getfqdn() + ':' + argv[1]
    flag = False

    if len(argv) > 2: flag = True #verifica se há dois ou mais argumentos

    server = grpc.server(futures.ThreadPoolExecutor())

    stop_event = threading.Event() #evento para finalizar o servidor

    peer_pb2_grpc.add_PeerServerServicer_to_server(PeerServer(stop_event, service_id, flag), server)

    server.add_insecure_port(service_id)

    server.start()
    stop_event.wait()
    server.stop(5)

if __name__ == '__main__':
    try:
      serve()
    except Exception as e:
        print(e.with_traceback())
