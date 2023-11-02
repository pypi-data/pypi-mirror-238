import os
os.environ["FALCON_API_KEY"] = "eyJraWQiOiJvMU5OWE1jNmtOS29qN1BoekV4NjZCQUZSWFZZblRCbllQVkJLbldhUWg4PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJhZjZmNDk5ZS1kYTMyLTRjODYtOTE0ZC1hMjRkNWJhOTE2NTgiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9WMjhONTZtbmciLCJjbGllbnRfaWQiOiIyaHNoamdobWxxMnVmM2gyMGtoNmd2dmx0aCIsIm9yaWdpbl9qdGkiOiIwOTM5Y2E5Mi0yMzIxLTRlZDYtODlhZC0yZDQ5ZGQ0OWYzYWUiLCJldmVudF9pZCI6ImViMzkyYjcyLTBkZmItNDBhYi04NzUxLTY0NDEzZGVkMTdmMyIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE2OTg4NTk2NjIsImV4cCI6MTY5ODg2MzI2MiwiaWF0IjoxNjk4ODU5NjYyLCJqdGkiOiI2OTA4ZTAwMy0zOTM3LTQzNzYtYThjYi05OWZhMDcxOTc2YTEiLCJ1c2VybmFtZSI6ImFmNmY0OTllLWRhMzItNGM4Ni05MTRkLWEyNGQ1YmE5MTY1OCJ9.tinmlf7hGT5nBuH0KKulw7ukhX46kNJRnykpP-fJs8fzUqbCGy2RVyASH2n3ib3aRXSLLY1EjnaEeFvLBUx9lowRiuRD1ivQQoxjhrIvGaxhAAavnl96Yl2BZqjXlPWawW8rozsr0GmmJLGVeLfc88B1f9qTB0YopRA5m5oUCJzB-x-g0DANyB5GFMS5n278FO9YV-HHIlj36uw1d47mvtfgYSgrZITxOcTQHLsftOdoeV9xEeMFZipwE7xHcCOpClBOgu5BGXNuimaMaGrKJTcHr8nZ6aKP4l-octUEYxCBSirEpJZYlQLdmCb6rX_qywxV8mnt7XbYNrBYl46mlQ"

from unittest import TestCase
from unittest.mock import patch, Mock
import falconai

class TestChat(TestCase): 

    # @patch("falconai.core.requests.requests.post")
    async def test_chat_response(self):
        # Mocking the response from the chat API
        # mock_response = Mock()
        # mock_response.json.return_value = {"response": "Test response"}
        # mock_post.return_value = mock_response
        
        response = await falconai.models.chat(
            query="Write a story about Pakistan",
            model_name="Falcon40B",
            app_type="web",
            params={
                "temperature": 1,
                "stop": ["\n\n"],
                "max_new_tokens": 900,
                "top_p": 1
            },
            context=""
        )
        
        self.assertEqual(response, {"response": "Test response"})
