from uuid import uuid4

from sqlalchemy import select, desc

from db import SQLAlchemySessionContextManager
from items import items_pb2, items_pb2_grpc
from grpc import StatusCode
from concurrent import futures

import grpc

from items.models import Item, SearchResult
from utils.jaccard_similarity import compute_jaccard_similarity


class SimilaritySearchService(items_pb2_grpc.SimilaritySearchServiceServicer):
    def AddItem(self, request, context):
        with SQLAlchemySessionContextManager() as session:
            item_exists_query = select(1).filter(Item.id == request.id)
            item_exists = session.execute(item_exists_query).one_or_none()
            if item_exists:
                context.abort(StatusCode.ALREADY_EXISTS, "Item with given id already exists")
            else:
                item = Item(id=request.id, description=request.description)
                session.add(item)
                session.commit()
            return items_pb2.AddItemResponse(message="Item successfully created")

    def SearchItems(self, request, context):
        search_results = []
        with SQLAlchemySessionContextManager() as session:
            items = session.execute(select(Item)).scalars().all()
            items_dicts = [{"id": item.id, "description": item.description} for item in items]
            results = compute_jaccard_similarity(request.query, items_dicts)
            search_id = str(uuid4())

            for result in results:
                search_results.append(
                    SearchResult(search_id=search_id, item_id=result[0], similarity=result[1])
                )

            session.add_all(search_results)
            session.commit()
        if not search_results:
            context.abort(StatusCode.NOT_FOUND, "No results found")

        return items_pb2.SearchItemsResponse(search_id=search_id)

    def GetSearchResults(self, request, context):
        with SQLAlchemySessionContextManager() as session:
            items = session.execute(
                select(Item)
                .join(SearchResult)
                .filter(SearchResult.search_id == request.search_id)
                .order_by(desc(SearchResult.similarity))
            ).scalars().all()
            items_dicts = [{"id": item.id, "description": item.description} for item in items]
        return items_pb2.GetSearchResultsResponse(results=items_dicts)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    items_pb2_grpc.add_SimilaritySearchServiceServicer_to_server(
        SimilaritySearchService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
