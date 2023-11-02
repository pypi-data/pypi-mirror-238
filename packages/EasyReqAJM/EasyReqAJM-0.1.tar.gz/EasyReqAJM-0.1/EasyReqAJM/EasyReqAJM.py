"""
EasyReqAJM.py

Wrapper for Requests module to make my life easier.

"""
from json import JSONDecodeError
from logging import Logger
import requests
from requests import RequestException


class InvalidRequestMethod(RequestException):
    ...


class EasyReq:
    def __init__(self, logger: Logger = None, **kwargs):
        self._kwargs = None
        self._fail_http_400s = True
        if kwargs:
            self._kwargs = kwargs
            if 'fail_http_400s' in self._kwargs:
                self._fail_http_400s = self._kwargs['fail_http_400s']
        self._valid_request_methods = ["GET", "POST"]
        if logger:
            self._logger = logger
        else:
            self._logger = Logger("Dummy_logger")

    def MakeReq(self, method, url, headers: dict, payload) -> requests.Response:
        if method.lower() not in [x.lower() for x in self._valid_request_methods]:
            raise InvalidRequestMethod(
                f"{method} is not a valid request method "
                f"(Options are: {', '.join(self._valid_request_methods)})")

        try:
            response = requests.request(method, url, headers=headers, data=payload)
        except requests.RequestException as e:
            self._logger.error(e, exc_info=True)
            raise e
        if response.ok:
            return response
        else:
            if response.status_code == 429:
                response.reason = "Too many requests sent too quickly"
            try:
                raise requests.RequestException(f"response was {response.status_code} {response.reason},"
                                                f" with the following (if any) message: "
                                                f"{response.json()['message'].split('Authorization=')[0]}")
            except JSONDecodeError as e:
                try:
                    raise requests.RequestException(f"response was {response.status_code} {response.reason},"
                                                    f" with the following (if any) message: "
                                                    f"{response.text.split('Authorization=')[0]}") from None
                except requests.RequestException as e:
                    self._logger.error(e, exc_info=True)
                    if not self._fail_http_400s:
                        if response.status_code == 403 or response.status_code == 401:
                            self._logger.warning(f"response code {response.status_code} returned. "
                                                 f"Returning response for further processing")
                            return response
                        else:
                            raise e
                    else:
                        raise e
            except requests.RequestException as e:
                self._logger.error(e, exc_info=True)
                if not self._fail_http_400s:
                    if response.status_code == 403 or response.status_code == 401:
                        self._logger.warning(f"response code {response.status_code} returned. "
                                             f"Returning response for further processing")
                        return response
                    else:
                        raise e
                else:
                    raise e
