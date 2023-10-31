import os
os.environ["FALCON_API_KEY"] = "YOUR_TEST_TOKEN_HERE"

from unittest import TestCase
from unittest.mock import patch, Mock
import falconai

class TestChat(TestCase): 

    @patch("falconai.core.requests.requests.post")
    def test_chat_response(self, mock_post):
        print("test wasim")
        # Mocking the response from the chat API
        mock_response = Mock()
        mock_response.json.return_value = {"response": "Test response"}
        mock_post.return_value = mock_response
        
        response = falconai.models.plugin_chat(
            query="Write a story about Pakistan",
            model_type="Falcon40B",
            app_type="web",
            plugin_ids=[5, 6, 8]
        )
        
        self.assertEqual(response, {"response": "Test response"})
    
    @patch("falconai.core.requests.requests.post")
    def test_chat_api_error(self, mock_post):
        # Simulating an error from the API
        mock_post.side_effect = Exception("API Error")
        
        with self.assertRaises(Exception) as context:
            falconai.models.plugin_chat(
                query="Write a story about Pakistan",
                model_type="Falcon40B",
                app_type="web",
                plugin_ids=[5, 6, 8]
            )
        
        self.assertEqual(str(context.exception), "API Error")
