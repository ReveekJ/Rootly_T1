import grpc
from concurrent import futures
import time

# Generated from the .proto file
import log_pb2 as terraformlogviewer_pb2
import log_pb2_grpc as terraformlogviewer_pb2_grpc
from sqlalchemy.util import await_only

from backend.rabbitmq.parser.producer import process_parsing


class LogParserService(terraformlogviewer_pb2_grpc.LogParserServiceServicer):
    def ParseLogs(self, request, context):
        # In a real implementation you would read the log file identified by request.log_id,
        # parse each line and fill LogEntry messages.
        # Here we return a static example.


class UploadService(terraformlogviewer_pb2_grpc.UploadServiceServicer):
    def UploadLogs(self, request, context):
        # Store the uploaded bytes somewhere (e.g., a temp file or DB) and generate an ID.
        # For demo purposes we just return a fixed ID.
        print(request)
        # You would normally write request.log_file to storage here.
        # return terraformlogviewer_pb2.UploadLogsResponse(log_id=log_id)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    terraformlogviewer_pb2_grpc.add_LogParserServiceServicer_to_server(
        LogParserService(), server
    )
    terraformlogviewer_pb2_grpc.add_UploadServiceServicer_to_server(
        UploadService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server listening on 0.0.0.0:50051")
    try:
        while True:
            time.sleep(86400)  # keep alive
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
