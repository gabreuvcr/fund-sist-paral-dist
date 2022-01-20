from sys import argv

import grpc

from protos import center_pb2, center_pb2_grpc, peer_pb2, peer_pb2_grpc

def run():
    host = ''
    if len(argv) == 2:
        host = argv[1]
    else:
        exit()

    channel = grpc.insecure_channel(host)

    stub = center_pb2_grpc.CenterServerStub(channel)

    while True:
        command = input()

        if not command:
            break

        if command.startswith('C'):
            if len(command.split(',')) != 2: continue
            
            _, key = command.split(',')
            response = stub.mapping(center_pb2.MappingRequest(key = int(key)))
            if response.retval == '':
                continue
            
            channel_peer = grpc.insecure_channel(response.retval)
            stub_peer = peer_pb2_grpc.PeerServerStub(channel_peer)

            response_peer = stub_peer.query(peer_pb2.QueryRequest(key = int(key)))

            print(f"{response.retval}:{response_peer.retval}")

        elif command.startswith('T'):            
            response = stub.end(center_pb2.EmptyRequest())
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
