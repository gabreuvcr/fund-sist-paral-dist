# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from protos import peer_pb2 as protos_dot_peer__pb2


class PeerServerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.insert = channel.unary_unary(
                '/peer.PeerServer/insert',
                request_serializer=protos_dot_peer__pb2.InsertRequest.SerializeToString,
                response_deserializer=protos_dot_peer__pb2.IntReply.FromString,
                )
        self.query = channel.unary_unary(
                '/peer.PeerServer/query',
                request_serializer=protos_dot_peer__pb2.QueryRequest.SerializeToString,
                response_deserializer=protos_dot_peer__pb2.StringReply.FromString,
                )
        self.active = channel.unary_unary(
                '/peer.PeerServer/active',
                request_serializer=protos_dot_peer__pb2.ActiveRequest.SerializeToString,
                response_deserializer=protos_dot_peer__pb2.IntReply.FromString,
                )
        self.end = channel.unary_unary(
                '/peer.PeerServer/end',
                request_serializer=protos_dot_peer__pb2.EmptyRequest.SerializeToString,
                response_deserializer=protos_dot_peer__pb2.IntReply.FromString,
                )


class PeerServerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def insert(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def query(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def active(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def end(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PeerServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'insert': grpc.unary_unary_rpc_method_handler(
                    servicer.insert,
                    request_deserializer=protos_dot_peer__pb2.InsertRequest.FromString,
                    response_serializer=protos_dot_peer__pb2.IntReply.SerializeToString,
            ),
            'query': grpc.unary_unary_rpc_method_handler(
                    servicer.query,
                    request_deserializer=protos_dot_peer__pb2.QueryRequest.FromString,
                    response_serializer=protos_dot_peer__pb2.StringReply.SerializeToString,
            ),
            'active': grpc.unary_unary_rpc_method_handler(
                    servicer.active,
                    request_deserializer=protos_dot_peer__pb2.ActiveRequest.FromString,
                    response_serializer=protos_dot_peer__pb2.IntReply.SerializeToString,
            ),
            'end': grpc.unary_unary_rpc_method_handler(
                    servicer.end,
                    request_deserializer=protos_dot_peer__pb2.EmptyRequest.FromString,
                    response_serializer=protos_dot_peer__pb2.IntReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'peer.PeerServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PeerServer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def insert(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/peer.PeerServer/insert',
            protos_dot_peer__pb2.InsertRequest.SerializeToString,
            protos_dot_peer__pb2.IntReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def query(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/peer.PeerServer/query',
            protos_dot_peer__pb2.QueryRequest.SerializeToString,
            protos_dot_peer__pb2.StringReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def active(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/peer.PeerServer/active',
            protos_dot_peer__pb2.ActiveRequest.SerializeToString,
            protos_dot_peer__pb2.IntReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def end(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/peer.PeerServer/end',
            protos_dot_peer__pb2.EmptyRequest.SerializeToString,
            protos_dot_peer__pb2.IntReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
