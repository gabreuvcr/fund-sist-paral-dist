from sys import argv

import grpc

from protos import peer_pb2, peer_pb2_grpc

def run():
    service_id = argv[1]

    channel = grpc.insecure_channel(service_id)

    stub = peer_pb2_grpc.PeerServerStub(channel)

    while True:
        client_input = input()

        if not client_input:
            break

        if client_input.startswith('I'):
            if len(client_input.split(',')) != 3: continue

            command, key, value = client_input.split(',')
            response = stub.insert(peer_pb2.InsertRequest(key = int(key), value = value))
            print(response.retval)

        elif client_input.startswith('C'):
            if len(client_input.split(',')) != 2: continue
            
            command, key = client_input.split(',')
            response = stub.query(peer_pb2.QueryRequest(key = int(key)))
            print(response.retval)

        elif client_input.startswith('A'):
            if len(client_input.split(',')) != 2: continue
            
            command, center_service_id = client_input.split(',')
            response = stub.active(peer_pb2.ActiveRequest(service_id = center_service_id))
            print(response.retval)

        elif client_input.startswith('T'):            
            response = stub.end(peer_pb2.EmptyRequest())
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
