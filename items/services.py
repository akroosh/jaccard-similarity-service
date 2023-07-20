from uuid import uuid4

from grpc import StatusCode
from sqlalchemy import desc, select

from db import SQLAlchemySessionContextManager
from items.models import Item, SearchResult
from protobufs import items_pb2, items_pb2_grpc
from utils.jaccard_similarity import compute_similarity_for_all_items


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
            results = compute_similarity_for_all_items(request.query, items_dicts)
            search_id = str(uuid4())

            for item_id, similarity in results:
                search_results.append(SearchResult(search_id=search_id, item_id=item_id, similarity=similarity))

            if not search_results:
                context.abort(StatusCode.NOT_FOUND, "No results found")

            session.add_all(search_results)
            session.commit()

        return items_pb2.SearchItemsResponse(search_id=search_id)

    def GetSearchResults(self, request, context):
        with SQLAlchemySessionContextManager() as session:
            items = (
                session.execute(
                    select(Item)
                    .join(SearchResult)
                    .filter(SearchResult.search_id == request.search_id)
                    .order_by(desc(SearchResult.similarity))
                )
                .scalars()
                .all()
            )
            items_dicts = [{"id": item.id, "description": item.description} for item in items]
        return items_pb2.GetSearchResultsResponse(results=items_dicts)
