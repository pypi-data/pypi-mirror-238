import base64
import json
from concurrent.futures import as_completed, ThreadPoolExecutor
from io import BytesIO
from itertools import zip_longest
from typing import Callable, Dict, List, Union

import cv2
import numpy as np
import requests
from PIL import Image

from linker_atom.lib.common import catch_exc
from linker_atom.lib.exception import VqlError
from linker_atom.lib.log import logger
from linker_atom.lib.share_memory import MmapManager

FETCH_TIMEOUT = 15


def local_to_pil(path: str) -> Image.Image:
    return Image.open(path).convert("RGB")


def base64_to_pil(b64_str: str) -> Image.Image:
    return Image.open(BytesIO(base64.b64decode(b64_str))).convert("RGB")


def url_to_pil(url: str) -> Image.Image:
    content = None
    for _ in range(3):
        response = requests.get(url, timeout=FETCH_TIMEOUT)
        content = response.content
        if content:
            break
    if content is None:
        return
    return Image.open(BytesIO(content)).convert("RGB")


def mmap_to_pil(value: Union[str, dict]):
    if isinstance(value, str):
        value = json.loads(value)
    path, position, size, height, width = (
        str(value.get("path")),
        int(value.get("position")),
        int(value.get("size")),
        int(value.get("height")),
        int(value.get("width")),
    )
    mm = MmapManager(path)
    buffer = mm.read(position, size)
    return Image.open(BytesIO(buffer)).convert("RGB")


def file_to_base64(path: str, mode="rb") -> bytes:
    with open(path, mode) as f:
        return base64.b64encode(f.read())


@catch_exc()
def url_to_np(url: str):
    content = None
    for _ in range(3):
        response = requests.get(url, timeout=FETCH_TIMEOUT)
        content = response.content
        if content:
            break
    if content is None:
        return
    img = np.asarray(bytearray(content), dtype=np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


@catch_exc()
def local_to_np(path: str):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


@catch_exc()
def base64_to_np(data: str):
    img_string = base64.b64decode(data)
    img = np.frombuffer(img_string, np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


@catch_exc()
def mmap_to_np(value: Union[str, dict]):
    if isinstance(value, str):
        value = json.loads(value)
    path, position, size, height, width = (
        str(value.get("path")),
        int(value.get("position")),
        int(value.get("size")),
        int(value.get("height")),
        int(value.get("width")),
    )
    mm = MmapManager(path)
    buffer = mm.read(position, size)
    try:
        nparr = np.frombuffer(buffer=buffer, dtype=np.uint8)
        img = nparr.reshape((height, width, 3))
    except Exception as e:
        logger.error(e)
        np_array = np.ndarray(
            (height, width, 3), dtype=np.uint8, buffer=buffer
        )
        img = np.ndarray((height, width, 3), dtype=np.uint8)
        img[:] = np_array[:]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def chunked(it, n):
    marker = object()
    for group in (list(g) for g in zip_longest(*[iter(it)] * n, fillvalue=marker)):
        yield filter(lambda x: x is not marker, group)


SRC_TYPE_MAP = {
    "url": url_to_np,
    "local": local_to_np,
    "base64": base64_to_np,
    "mmap": mmap_to_np,
}


def load_image(src_type: str, data: List, func_map: Dict[str, Callable] = SRC_TYPE_MAP):
    if not data or src_type == "stream":
        return []
    
    if len(data) == 1:
        match_func = func_map.get(src_type)
        if not match_func:
            raise VqlError(504)
        result = match_func(data[0])
        return [result]
    
    tasks = dict()
    results = []
    with ThreadPoolExecutor(thread_name_prefix="LoadImage") as e:
        for index, data in enumerate(data):
            match_func = func_map.get(src_type)
            if not match_func:
                raise VqlError(504)
            tasks[e.submit(match_func, data)] = index
    for task in as_completed(tasks):
        result = task.result()
        if result is None:
            raise VqlError(503)
        index = tasks[task]
        results.append(dict(index=index, result=result))
    results.sort(key=lambda x: x["index"])
    return [item["result"] for item in results]
