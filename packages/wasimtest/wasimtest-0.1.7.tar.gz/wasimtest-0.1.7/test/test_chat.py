import os
from unittest import TestCase
from unittest.mock import patch, Mock

from falconai import chat

class TestChat(TestCase):
    
    def setUp(self):
        # Set this token for testing purpose, but in real scenarios, 
        # please keep this confidential and not hardcoded.
        os.environ["FALCONAI_AUTH_TOKEN"] = "YOUR_TEST_TOKEN_HERE"

    @patch("falconai.models.chat.requests.post")
    def test_chat_response(self, mock_post):
        # Mocking the response from the chat API
        mock_response = Mock()
        mock_response.json.return_value = {"response": "Test response"}
        mock_post.return_value = mock_response
        
        response = chat(
            query="Write a story about Pakistan",
            model_type="Falcon40B",
            app_type="web",
            plugin_ids=[5, 6, 8]
        )
        
        self.assertEqual(response, {"response": "Test response"})
    
    @patch("falconai.models.chat.requests.post")
    def test_chat_api_error(self, mock_post):
        # Simulating an error from the API
        mock_post.side_effect = Exception("API Error")
        
        with self.assertRaises(Exception) as context:
            chat(
                query="Write a story about Pakistan",
                model_type="Falcon40B",
                app_type="web",
                plugin_ids=[5, 6, 8]
            )
        
        self.assertEqual(str(context.exception), "API Error")
