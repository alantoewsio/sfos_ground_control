from requests import Request, Response
from requests.utils import dict_from_cookiejar as _dict_from_cookiejar


def resp2dict(response: Response, _root: bool = True):
    response_dict = {}
    try:
        response_dict = {
            "text": response.text,
            "headers": dict(sorted(response.headers.items())),
            "cookies": dict(sorted(_dict_from_cookiejar(response.cookies).items())),
            "status_code": response.status_code,
            "request": {
                "url": response.request.url,
                "method": response.request.method,
                "headers": dict(sorted(response.request.headers.items())),
                "path_url": response.request.path_url,
                "body": response.request.body,
            },
        }
        if _root:
            response_dict["history"] = [resp2dict(h, False) for h in response.history]

    except Exception as e:
        msg = f"resp2dict Exception: type='{type(e)}' msg='{e}'"
        print(msg)
        response_dict["exception"] = msg
    return response_dict


def req2dict(request: Request):
    d = {
        "url": request.url,
        "method": request.method,
        "headers": dict(request.headers),
        "cookies": _dict_from_cookiejar(request.cookies),
        "params": request.params,
        "data": request.data,
    }
    return d
