# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import procedures_pb2 as procedures__pb2


class DictionaryStorageStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.insert = channel.unary_unary(
                '/procedures.DictionaryStorage/insert',
                request_serializer=procedures__pb2.InsertRequest.SerializeToString,
                response_deserializer=procedures__pb2.IntReply.FromString,
                )
        self.query = channel.unary_unary(
                '/procedures.DictionaryStorage/query',
                request_serializer=procedures__pb2.QueryRequest.SerializeToString,
                response_deserializer=procedures__pb2.StringReply.FromString,
                )
        self.active = channel.unary_unary(
                '/procedures.DictionaryStorage/active',
                request_serializer=procedures__pb2.ActiveRequest.SerializeToString,
                response_deserializer=procedures__pb2.IntReply.FromString,
                )
        self.end = channel.unary_unary(
                '/procedures.DictionaryStorage/end',
                request_serializer=procedures__pb2.EmptyRequest.SerializeToString,
                response_deserializer=procedures__pb2.IntReply.FromString,
                )


class DictionaryStorageServicer(object):
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


def add_DictionaryStorageServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'insert': grpc.unary_unary_rpc_method_handler(
                    servicer.insert,
                    request_deserializer=procedures__pb2.InsertRequest.FromString,
                    response_serializer=procedures__pb2.IntReply.SerializeToString,
            ),
            'query': grpc.unary_unary_rpc_method_handler(
                    servicer.query,
                    request_deserializer=procedures__pb2.QueryRequest.FromString,
                    response_serializer=procedures__pb2.StringReply.SerializeToString,
            ),
            'active': grpc.unary_unary_rpc_method_handler(
                    servicer.active,
                    request_deserializer=procedures__pb2.ActiveRequest.FromString,
                    response_serializer=procedures__pb2.IntReply.SerializeToString,
            ),
            'end': grpc.unary_unary_rpc_method_handler(
                    servicer.end,
                    request_deserializer=procedures__pb2.EmptyRequest.FromString,
                    response_serializer=procedures__pb2.IntReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'procedures.DictionaryStorage', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DictionaryStorage(object):
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
        return grpc.experimental.unary_unary(request, target, '/procedures.DictionaryStorage/insert',
            procedures__pb2.InsertRequest.SerializeToString,
            procedures__pb2.IntReply.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/procedures.DictionaryStorage/query',
            procedures__pb2.QueryRequest.SerializeToString,
            procedures__pb2.StringReply.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/procedures.DictionaryStorage/active',
            procedures__pb2.ActiveRequest.SerializeToString,
            procedures__pb2.IntReply.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/procedures.DictionaryStorage/end',
            procedures__pb2.EmptyRequest.SerializeToString,
            procedures__pb2.IntReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)