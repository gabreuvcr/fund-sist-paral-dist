from concurrent import futures
from sys import argv

import threading
import socket

import grpc

from protos import center_pb2, center_pb2_grpc

class CenterServer(center_pb2_grpc.CenterServerServicer):
    def __init__(self, stop_event):
        self._stop_event = stop_event
        self.dictionary = dict()

    def register(self, request, context):
        #para todas as chaves enviados por um servidor de pares,
        #registra ao seu dict, caso a key ja exista, o valor é sobrescrito
        #retorna o numero de chaves que foram savas
        for key in request.keys:
            self.dictionary[key] = request.service_id
        return center_pb2.IntReply(retval = len(request.keys))

    def mapping(self, request, context):
        #quando um cliente que se conecta ao servidor centralizador
        #requisitar o mapping de uma chave, o servidor irá verificar se a chave
        #já foi cadastrada, retornando para o cliente o string identificador
        #de serviço de um servidor de pares
        if request.key in self.dictionary:
            return center_pb2.StringReply(retval = self.dictionary[request.key])
        #se nao existir a chave, retorna uma string vazia
        return center_pb2.StringReply(retval= '')

    def end(self, request, context):
        #se algum cliente utilizar o comando T, o servidor
        #termina sua execução liberando o stop_event.wait()
        #e retorna o numero de chaves que estavam salvas no seu dict
        self._stop_event.set()
        return center_pb2.IntReply(retval = len(self.dictionary))


def serve():
    #string identificador de serviço
    service_id = socket.getfqdn() + ':' + argv[1]

    server = grpc.server(futures.ThreadPoolExecutor())

    stop_event = threading.Event() #evento para finalizar o servidor

    center_pb2_grpc.add_CenterServerServicer_to_server(CenterServer(stop_event), server)

    server.add_insecure_port(service_id)

    server.start()
    stop_event.wait()
    server.stop(5)

if __name__ == '__main__':
    try:
        serve()
    except Exception as e:
        print(e.with_traceback())
