from concurrent.futures import ThreadPoolExecutor

import grpc

from items.services import SimilaritySearchService
from protobufs.items_pb2_grpc import add_SimilaritySearchServiceServicer_to_server


def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_SimilaritySearchServiceServicer_to_server(SimilaritySearchService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()
