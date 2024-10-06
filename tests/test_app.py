import unittest
from unittest.mock import patch, AsyncMock
from app import create_app
import json


class TestGameInfoAPI(unittest.TestCase):

    def setUp(self):
        """Set up test client and initialize any required resources."""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    @patch("app.routes.get_relevant_context")
    @patch("app.routes.generate_response", new_callable=AsyncMock)
    def test_query_game_info_valid(
        self, mock_generate_response, mock_get_relevant_context
    ):
        """Test for valid input and a successful response from OpenAI."""
        # Mock the relevant context and OpenAI response
        mock_get_relevant_context.return_value = "Some relevant game context"
        mock_generate_response.return_value = "Mocked OpenAI Response"

        # Simulate sending a valid POST request
        response = self.client.post(
            "/query",
            data=json.dumps({"query": "Tell me about the game"}),
            content_type="application/json",
        )

        # Assert the response status code and content
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["response"], "Mocked OpenAI Response")

    def test_query_game_info_missing_query_field(self):
        """Test for missing 'query' field in the request."""
        # Simulate sending a POST request without the 'query' field
        response = self.client.post(
            "/query", data=json.dumps({}), content_type="application/json"
        )

        # Assert that the request was rejected with a 400 status
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "Invalid input. 'query' field is required.")

    @patch("app.routes.get_relevant_context")
    def test_query_game_info_no_relevant_info_found(self, mock_get_relevant_context):
        """Test for case when no relevant information is found."""
        # Mock the relevant context to return an empty string
        mock_get_relevant_context.return_value = ""

        # Simulate sending a valid POST request but no relevant context is found
        response = self.client.post(
            "/query",
            data=json.dumps({"query": "Unknown game"}),
            content_type="application/json",
        )

        # Assert that the request returned a 404 error
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(
            data["error"], "No relevant information found for the given query."
        )

    @patch("app.routes.get_relevant_context")
    def test_query_game_info_internal_server_error(self, mock_get_relevant_context):
        """Test for internal server error caused by an exception."""
        # Mock get_relevant_context to raise an exception
        mock_get_relevant_context.side_effect = Exception("Unexpected error")

        # Simulate sending a valid POST request but an exception is raised internally
        response = self.client.post(
            "/query",
            data=json.dumps({"query": "Tell me about the game"}),
            content_type="application/json",
        )

        # Assert that the request returned a 500 error
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Unexpected error")


if __name__ == "__main__":
    unittest.main(verbosity=2)
