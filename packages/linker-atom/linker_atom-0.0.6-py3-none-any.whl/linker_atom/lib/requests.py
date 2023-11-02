import time

import requests

from linker_atom.lib.common import format_long_val
from linker_atom.lib.log import logger


def request(url, method, **kwargs):
    start_time = time.perf_counter()
    pre_log = f"url: {url}, method: {method}\n"
    json_body = kwargs.get("json", {})
    data_body = kwargs.get("data", {})
    if 'timeout' not in kwargs:
        kwargs['timeout'] = 30
    
    if json_body:
        pre_log += f"json_body: {format_long_val(json_body)}\n"
    if data_body:
        pre_log += f"data_body: {format_long_val(data_body)}\n"
    
    logger.info(f"Request summary: {pre_log}")
    response = requests.request(method=method, url=url, **kwargs)
    end_time = time.perf_counter()
    duration = round((end_time - start_time) * 1000, 3)
    post_log = f'Response summary: '
    try:
        post_log += f"{format_long_val(response.json())} "
    except:
        pass
    post_log += f'duration: {duration}ms\n'
    logger.info(post_log)
    return response


def get(url, **kwargs):
    return request(url, method='get', **kwargs)


def post(url, **kwargs):
    return request(url, method='post', **kwargs)
