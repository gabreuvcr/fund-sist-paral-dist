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
        for key in request.keys:
            self.dictionary[key] = request.service
        return center_pb2.IntReply(retval = len(request.keys))

    def mapping(self, request, context):
        if request.key in self.dictionary:
            return center_pb2.StringReply(retval = self.dictionary[request.key])
        return center_pb2.StringReply(retval= '')

    def end(self, request, context):
        self._stop_event.set()
        return center_pb2.IntReply(retval = len(self.dictionary))


def serve():
    addr = socket.gethostbyname(socket.getfqdn())
    port = ''

    if len(argv) >= 2: port = argv[1] 

    server = grpc.server(futures.ThreadPoolExecutor())

    stop_event = threading.Event()

    center_pb2_grpc.add_CenterServerServicer_to_server(CenterServer(stop_event), server)

    server.add_insecure_port(f"{addr}:{port}")

    server.start()
    stop_event.wait()
    server.stop(5)

if __name__ == '__main__':
    try:
        serve()
    except Exception as e:
        print(e.with_traceback())
