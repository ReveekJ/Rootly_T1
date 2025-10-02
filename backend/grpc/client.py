import grpc

import log_pb2
import log_pb2_grpc


def main():
    with grpc.insecure_channel('drawing:8080') as channel:
        stub = log_pb2_grpc.UploadServiceStub(channel)

        stub.UploadLogs(log_pb2.Up(log_file="test.log"))