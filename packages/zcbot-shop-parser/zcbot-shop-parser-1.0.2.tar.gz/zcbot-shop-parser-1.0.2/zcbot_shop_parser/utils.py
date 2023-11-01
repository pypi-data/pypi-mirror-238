from functools import wraps


def singleton(cls):
    _instance = {}

    @wraps(cls)
    def _singlenton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singlenton


def clean_url(url):
    """
    链接非法字符清理
    """
    fix_err = {
        '&amp;': '&',
        'amp;': '',
        '＆': '&',
        ' ': ''
    }
    _url = url
    if _url:
        for key in fix_err:
            if key in _url:
                _url = _url.replace(key, fix_err.get(key))

    return _url
