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
        if request.key in self.dictionary: 
            return peer_pb2.IntReply(retval = -1)
        
        self.dictionary[request.key] = request.value
        return peer_pb2.IntReply(retval = 0)

    def query(self, request, context):
        if request.key in self.dictionary:
            return peer_pb2.StringReply(retval = self.dictionary[request.key])
        
        return peer_pb2.StringReply(retval = '')
    
    def active(self, request, context):
        if not self.flag:
            return peer_pb2.IntReply(retval = 0)

        channel = grpc.insecure_channel(request.service_id)
        stub = center_pb2_grpc.CenterServerStub(channel)

        response = stub.register(center_pb2.RegisterRequest(service_id = self.service_id, keys = self.dictionary.keys()))
        return peer_pb2.IntReply(retval = response.retval)

    def end(self, request, context):
        self._stop_event.set()
        return peer_pb2.IntReply(retval = 0)


def serve():
    service_id = socket.gethostbyname(socket.getfqdn()) + ':' + argv[1]
    flag = False

    if len(argv) > 2: flag = True

    server = grpc.server(futures.ThreadPoolExecutor())

    stop_event = threading.Event()

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
