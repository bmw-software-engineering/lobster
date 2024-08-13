from typing import Dict

import responses


class MockHttpServerWithoutCallback:
    """This is a http server mocker without a callback"""

    def __init__(
        self, response_method: str, server_url: str, status_code: int, headers: Dict = {}, body: bytes = ""
    ) -> None:
        self.response_method = response_method
        self.server_url = server_url
        self.status_code = status_code
        self.headers = headers
        self.body = body

    def start(self) -> None:
        """
        This function is a convenient way to mock http servers according to given server url, response method
        To use these mocked responses in your tests, remember to decorate your function with @responses.activate !

        Parameters
        ----------
        server_url: str
            url of the mock http server

        response_method: str
            http method

        status_code: int
            status code that will be returned with http response

        """
        responses.add(
            self.response_method,
            self.server_url,
            status=self.status_code,
            headers=self.headers,
            body=self.body,
        )
