from sys import argv

import grpc

from protos import center_pb2, center_pb2_grpc, peer_pb2, peer_pb2_grpc

def run():
    service_id = argv[1]

    channel = grpc.insecure_channel(service_id)

    stub = center_pb2_grpc.CenterServerStub(channel)

    while True:
        client_input = input()

        if not client_input:
            break

        if client_input.startswith('C'):
            if len(client_input.split(',')) != 2: continue
            
            command, key = client_input.split(',')

            response = stub.mapping(center_pb2.MappingRequest(key = int(key)))
            if response.retval == '': continue
            
            channel_peer = grpc.insecure_channel(response.retval)
            stub_peer = peer_pb2_grpc.PeerServerStub(channel_peer)

            response_peer = stub_peer.query(peer_pb2.QueryRequest(key = int(key)))

            print(f"{response.retval}:{response_peer.retval}")

        elif client_input.startswith('T'):            
            response = stub.end(center_pb2.EmptyRequest())
            print(response.retval)
            break

    channel.close()


if __name__ == '__main__':
    try:
        run()
    #Servidor foi finalizado ou input do client foi um EOF
    except (grpc._channel._InactiveRpcError, EOFError):
        exit()
    except Exception as e:
        print(e.with_traceback())
