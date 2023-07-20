import unittest
from unittest.mock import MagicMock
from grpc import StatusCode
from protobufs import items_pb2
from items.services import SimilaritySearchService


class SimilaritySearchServiceTest(unittest.TestCase):
    def setUp(self):
        """Set up the test environment by initializing SimilaritySearchService."""
        self.service = SimilaritySearchService()

    def test_AddItem_Success(self):
        """Test adding an item with success."""
        context = MagicMock()
        request = items_pb2.AddItemRequest(id="200", description="Test item")
        response = self.service.AddItem(request, context)
        self.assertEqual(response.message, "Item successfully created")

    def test_AddItem_AlreadyExists(self):
        """Test adding an item that already exists."""
        context = MagicMock()
        request = items_pb2.AddItemRequest(id="300", description="Test item")
        self.service.session = MagicMock()
        self.service.session.execute().one_or_none.return_value = True

        # add item
        response = self.service.AddItem(request, context)
        self.assertEqual(response.message, "Item successfully created")

        # add item with the same id
        self.service.AddItem(request, context)
        context.abort.assert_called_with(StatusCode.ALREADY_EXISTS, "Item with given id already exists")

    def test_SearchItems_Success(self):
        """Test searching for items with success."""
        context = MagicMock()

        # add items
        request = items_pb2.AddItemRequest(id="400", description="Test item 1")
        self.service.AddItem(request, context)
        request = items_pb2.AddItemRequest(id="401", description="2 testing item")
        self.service.AddItem(request, context)

        # make search query
        request = items_pb2.SearchItemsRequest(query="test 1")
        response = self.service.SearchItems(request, context)

        self.assertIsNotNone(response.search_id)

    def test_GetSearchResults_Success(self):
        """Test getting search results with success."""
        context = MagicMock()

        # add items
        request = items_pb2.AddItemRequest(id="500", description="in test 1")
        self.service.AddItem(request, context)
        request = items_pb2.AddItemRequest(id="501", description="out test 2")
        self.service.AddItem(request, context)

        # make search query
        request = items_pb2.SearchItemsRequest(query="in test")
        response = self.service.SearchItems(request, context)
        self.assertIsNotNone(response.search_id)

        # make get results query
        request = items_pb2.GetSearchResultsRequest(search_id=response.search_id)
        response = self.service.GetSearchResults(request, context)

        # assert that the response results are not empty
        self.assertTrue(response.results)
