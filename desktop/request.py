import json
import requests
from data import LocalStorage

method_dict = {
    'post': requests.post,
    'put': requests.put,
    'patch': requests.patch,
    'get': requests.get,
    'delete': requests.delete,
}


def send_request(method, url, data, func, result_label):
    local_storage = LocalStorage()
    method_func = method_dict[method]

    headers = {'Content-Type': 'application/json'}

    token = local_storage.get_token()

    if token:
        headers['Authorization'] = f'Token {token}'

    data = json.dumps(data)

    try:
        response = method_func(url, data=data, headers=headers)

        if 200 <= response.status_code < 300:
            func(response)
        else:
            result_label.config(text=f"Error: {response.status_code} - {response.text}")

    except requests.RequestException as e:
        result_label.config(text=f"Error: {e}", wraplength=400)
