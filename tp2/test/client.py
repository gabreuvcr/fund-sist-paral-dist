from __future__ import print_function # usado internamente nos stubs
import os # para usar getpid

import grpc

import hello_pb2, hello_pb2_grpc # módulos gerados pelo compilador de gRPC

def run():
    # Primeiro, é preciso abrir um canal para o servidor
    channel = grpc.insecure_channel('localhost:8888')
    # E criar o stub, que vai ser o objeto com referências para os
    # procedimentos remotos (código gerado pelo compilador)
    stub = hello_pb2_grpc.DoStuffStub(channel)

    my_pid = os.getpid()

    # Primeira chamada: é preciso serializar o parâmetro usando
    #   o código gerado pelo compilador
    # A desserialização do valor de retorno é feita internamente pelo stub
    response = stub.say_hello(hello_pb2.HelloRequest(pid=my_pid))
    print("GRPC client received: " + response.retval)

    # Segunda chamada: mesmo princípio
    response = stub.say_hello_again(hello_pb2.HelloRequest(pid=my_pid))
    print("GRPC client received: " + response.retval)
    
    # Ao final o cliente pode fechar o canal para o servidor.
    channel.close()


if __name__ == '__main__':
    run()
