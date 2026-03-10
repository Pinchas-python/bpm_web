import requests


def http_request(_sla_name, url: str, method, headers=None, auth=None):
    if headers is None:
        headers = {}

    headers['content-type'] = 'application/json'

    session = requests.session()
    session.auth = auth
    try:
        normalized_method = str(method).strip().lower()
        if normalized_method == 'get':
            return session.get(url, headers=headers)
        if normalized_method == 'post':
            return session.post(url, headers=headers)
        if normalized_method == 'put':
            return session.put(url, headers=headers)
        if normalized_method == 'delete':
            return session.delete(url, headers=headers)
        raise ValueError(f"Unsupported HTTP method: {method}")
    finally:
        session.close()