import grpc
from grpc_interceptor import ClientCallDetails, ClientInterceptor
from profiles_rudderstack.tunnel.tunnel_pb2_grpc import WhtServiceStub

WhtService = None

def init_wht_service(goRpcAddress, token):
    interceptors = [ClientTokenAuthInterceptor(token)]
    channel = grpc.insecure_channel(goRpcAddress)
    intercept_channel = grpc.intercept_channel(channel, *interceptors)
    global WhtService
    WhtService = WhtServiceStub(intercept_channel)
    return WhtService, channel


class ClientTokenAuthInterceptor(ClientInterceptor):
    def __init__(self, token):
        self.token = token

    def intercept(self, method, request_or_iterator, call_details: grpc.ClientCallDetails):
        new_details = ClientCallDetails(
            call_details.method,
            call_details.timeout,
            [("authorization", self.token)],
            call_details.credentials,
            call_details.wait_for_ready,
            call_details.compression,
        )

        return method(request_or_iterator, new_details)