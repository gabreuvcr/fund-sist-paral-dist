from sys import argv

import grpc

from protos import peer_pb2, peer_pb2_grpc

def run():
    host = ''
    if len(argv) == 2:
        host = argv[1]
    else:
        exit()

    channel = grpc.insecure_channel(host)

    stub = peer_pb2_grpc.PeerServerStub(channel)

    while True:
        command = input()

        if not command:
            break

        if command.startswith('I'):
            if len(command.split(',')) != 3: continue

            _, key, value = command.split(',')
            response = stub.insert(peer_pb2.InsertRequest(key = int(key), value = value))
            print(response.retval)

        elif command.startswith('C'):
            if len(command.split(',')) != 2: continue
            
            _, key = command.split(',')
            response = stub.query(peer_pb2.QueryRequest(key = int(key)))
            print(response.retval)

        elif command.startswith('A'):
            if len(command.split(',')) != 2: continue
            
            _, service = command.split(',')
            response = stub.active(peer_pb2.ActiveRequest(service = service))
            print(response.retval)

        elif command.startswith('T'):            
            response = stub.end(peer_pb2.EmptyRequest())
            print(response.retval)
            break

    channel.close()


if __name__ == '__main__':
    try:
        run()
    except (grpc._channel._InactiveRpcError, EOFError):
        exit()
    except Exception as e:
        print(e.with_traceback())
