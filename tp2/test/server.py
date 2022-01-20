from concurrent import futures # usado na definição do pool de threads

import grpc

import hello_pb2, hello_pb2_grpc # módulos gerados pelo compilador de gRPC

# Os procedimentos oferecidos aos clientes precisam ser encapsulados
#   em uma classe que herda do código do stub.
class DoStuff(hello_pb2_grpc.DoStuffServicer):

   # A assinatura de todos os procedimentos é igual: um objeto com os
   # parâmetros e outro com o contexto de execução do servidor
   def say_hello(self, request, context):
      print("GRPC server in say_hello, pid =" , str(request.pid))
      return hello_pb2.HelloReply(retval='Hello, %d!' % request.pid)

   # Mesmo princípio para o segundo procedimento.
   def say_hello_again(self, request, context):
      print("GRPC server in say_hello_again, pid =" , str(request.pid))
      return hello_pb2.HelloReply(retval='Hello again, %d!' % request.pid)

def serve():
   # O servidor usa um modelo de pool de threads do pacote concurrent
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
   # O servidor precisa ser ligado ao objeto que identifica os
   #   procedimentos a serem executados.
   hello_pb2_grpc.add_DoStuffServicer_to_server(DoStuff(), server)
   # O método add_insecure_port permite a conexão direta por TCP
   #   Outros recursos estão disponíveis, como uso de um registry
   #   (dicionário de serviços), criptografia e autenticação.
   server.add_insecure_port('localhost:8888')
   # O servidor é iniciado e esse código não tem nada para fazer
   #   a não ser esperar pelo término da execução.
   server.start()
   server.wait_for_termination()

if __name__ == '__main__':
    serve()
