from kfsd.apps.core.exceptions.api import KubefacetsAPIException
from kfsd.apps.core.utils.http.headers.cookie import Cookie
from kfsd.apps.core.utils.dict import DictUtils


class Response(Cookie):
    def __init__(self):
        self.__response = None

    def getResponse(self):
        return self.__response

    def getJsonResponse(self):
        return self.__response.json()

    def setResponse(self, response):
        self.__response = response
        self.setCookiesHttpObj(response)

    def getStatusCode(self):
        return self.__response.status_code

    def isRespJSON(self):
        if (
            "application/json"
            in self.__response.headers.get("content-type", "").lower()
        ):
            return True
        return False

    def raiseAPIException(self, detail="Unknown error detail", code="unexpected_error"):
        resp = self.getJsonResponse() if self.isRespJSON() else {}
        errorStr = DictUtils.get(resp, "detail", detail)
        errorCode = DictUtils.get(resp, "code", code)
        raise KubefacetsAPIException(errorStr, errorCode, self.getStatusCode())

    def isRespValid(self, expStatusCode):
        if isinstance(expStatusCode, int) and not expStatusCode == self.getStatusCode():
            self.raiseAPIException(
                "Resp code mismatch, expected: {}, obs: {}".format(
                    expStatusCode, self.getStatusCode()
                )
            )

        if (
            isinstance(expStatusCode, list)
            and self.getStatusCode() not in expStatusCode
        ):
            self.raiseAPIException(
                "Resp code mismatch, expected: {}, obs: {}".format(
                    expStatusCode, self.getStatusCode()
                )
            )

        return True
