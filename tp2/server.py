from concurrent import futures
from sys import argv

import threading
import socket

import grpc

import procedures_pb2, procedures_pb2_grpc

dictionary = dict()

class DictionaryStorage(procedures_pb2_grpc.DictionaryStorageServicer):
    def __init__(self, stop_event):
        self._stop_event = stop_event

    def insert(self, request, context):
        if request.key in dictionary: 
            return procedures_pb2.IntReply(retval = -1)
        
        dictionary[request.key] = request.value.strip()
        return procedures_pb2.IntReply(retval = 0)

    def query(self, request, context):
        if request.key in dictionary:
            return procedures_pb2.StringReply(retval = dictionary[request.key])
        
        return procedures_pb2.StringReply(retval = None)
    
    def active(self, request, context):
        return procedures_pb2.IntReply(retval = 0)

    def end(self, request, context):
        self._stop_event.set()
        return procedures_pb2.IntReply(retval = 0)


def serve():
    addr = socket.gethostbyname(socket.getfqdn())
    port = ''

    if len(argv) == 2:
        port = argv[1] 
    else: 
        exit()
    
    if not port.isnumeric() or len(port) != 4: exit()
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    stop_event = threading.Event()

    procedures_pb2_grpc.add_DictionaryStorageServicer_to_server(DictionaryStorage(stop_event), server)

    server.add_insecure_port(f"{addr}:{port}")

    server.start()
    stop_event.wait()
    server.stop(5)

if __name__ == '__main__':
    try:
        serve()
    except Exception as e:
        print(e.with_traceback())
