import os
import unittest
from unittest import mock

from genomixhub import genomixhub as ghub


# This method will be used by the mock to replace requests.get
def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, json_data=None, text=None):
            self.json_data = json_data
            self.status_code = status_code
            self.text = text

        def json(self):
            return self.json_data

    if args[0] == "http://localhost:8080":  # test_load_frame_valid
        return MockResponse(
            200,
            json_data=[{"rsId": "123", "value": "CC"}, {"rsId": "456", "value": "AT"}],
        )
    else:
        return MockResponse(404, text="Error loading data from backend.")


class TestProdGenomixHub(unittest.TestCase):
    @mock.patch.dict(
        os.environ,
        {
            "GENOMIXHUB_ENVIRONMENT": "PROD",
            "GENOMIXHUB_BACKEND_URL": "http://localhost:8080",
            "GENOMIXHUB_BACKEND_TOKEN": "mytoken",
            "GENOMIXHUB_BACKEND_USERID": "user42",
        },
        clear=True,
    )
    @mock.patch("requests.post", side_effect=mocked_requests_post)
    def test_load_frame_valid(self, mock_post):
        frame = ghub.load(["rs123", "rs456", "rs789"])
        self.assertIsNotNone(frame)
        self.assertIsInstance(frame, ghub._GenomixHubFrameProd)
        self.assertEqual("CC", frame.get_value("rs123"))
        self.assertEqual("AT", frame.get_value("rs456"))
        self.assertIsNone(frame.get_value("rs789"))

        with self.assertRaises(ValueError):
            frame.get_value("rs4242")

        function_call = mock_post.call_args_list[0]
        self.assertEqual("http://localhost:8080", function_call.args[0])
        self.assertEqual(
            "token mytoken", function_call.kwargs["headers"]["Authorization"]
        )
        self.assertEqual("user42", function_call.kwargs["data"]["user_id"])
        self.assertEqual(
            ["rs123", "rs456", "rs789"], function_call.kwargs["data"]["rsIds"]
        )

    @mock.patch.dict(
        os.environ,
        {
            "GENOMIXHUB_ENVIRONMENT": "PROD",
            "GENOMIXHUB_BACKEND_URL": "http://return404:8080",
            "GENOMIXHUB_BACKEND_TOKEN": "mytoken",
            "GENOMIXHUB_BACKEND_USERID": "user42",
        },
        clear=True,
    )
    @mock.patch("requests.post", side_effect=mocked_requests_post)
    def test_load_frame_404_valid(self, mock_post):

        with self.assertRaises(Exception) as context:
            frame = ghub.load(["rs123", "rs456", "rs789"])
        # check that the raised exception is the one we expect
        self.assertEqual(
            "Error loading data from backend. Status code: 404 message Error loading data from backend.",
            str(context.exception.args[0]),
        )


if __name__ == "__main__":
    unittest.main()
