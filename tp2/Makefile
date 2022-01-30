run_serv_pares_1: grpc_all
	@python server_peer.py $(arg)

run_serv_pares_2: grpc_all
	@python server_peer.py $(arg) qqcoisa

run_cli_pares: grpc_peer
	@python client_peer.py $(arg)

run_serv_central: grpc_center
	@python server_center.py $(arg)

run_cli_central: grpc_all
	@python client_center.py $(arg)

grpc_peer:
	@python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. protos/peer.proto

grpc_center:
	@python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. protos/center.proto

grpc_all: grpc_peer grpc_center

clean:
	rm protos/peer_pb2.py protos/peer_pb2_grpc.py protos/center_pb2.py protos/center_pb2_grpc.py
	rm -r protos/__pycache__
