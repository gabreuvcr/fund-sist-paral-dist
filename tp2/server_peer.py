from concurrent import futures
from sys import argv

import threading
import socket

import grpc

from protos import peer_pb2, peer_pb2_grpc, center_pb2, center_pb2_grpc

class PeerServer(peer_pb2_grpc.PeerServerServicer):
    def __init__(self, stop_event, host, two_arg):
        self._stop_event = stop_event
        self.host = host
        self.two_arg = two_arg
        self.dictionary = dict()

    def insert(self, request, context):
        if request.key in self.dictionary: 
            return peer_pb2.IntReply(retval = -1)
        
        self.dictionary[request.key] = request.value.strip()
        return peer_pb2.IntReply(retval = 0)

    def query(self, request, context):
        if request.key in self.dictionary:
            return peer_pb2.StringReply(retval = self.dictionary[request.key])
        
        return peer_pb2.StringReply(retval = '')
    
    def active(self, request, context):
        if not self.two_arg:
            return peer_pb2.IntReply(retval = 0)

        channel = grpc.insecure_channel(request.service)
        stub = center_pb2_grpc.CenterServerStub(channel)

        response = stub.register(center_pb2.RegisterRequest(service = self.host, keys = self.dictionary.keys()))
        return peer_pb2.IntReply(retval = response.retval)

    def end(self, request, context):
        self._stop_event.set()
        return peer_pb2.IntReply(retval = 0)


def serve():
    addr = socket.gethostbyname(socket.getfqdn())
    port = ''
    two_arg = False

    if len(argv) >= 2: port = argv[1] 

    if len(argv) > 2: two_arg = True

    server = grpc.server(futures.ThreadPoolExecutor())

    stop_event = threading.Event()
    host = f"{addr}:{port}"

    peer_pb2_grpc.add_PeerServerServicer_to_server(PeerServer(stop_event, host, two_arg), server)

    server.add_insecure_port(host)

    server.start()
    stop_event.wait()
    server.stop(5)

if __name__ == '__main__':
    try:
      serve()
    except Exception as e:
        print(e.with_traceback())
