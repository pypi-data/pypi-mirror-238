import re
import time
from typing import Callable

from fastapi import APIRouter, Request, Response
from fastapi.routing import APIRoute

from linker_atom.lib.common import catch_exc, format_long_val
from linker_atom.lib.log import logger

octet_stream_pattern = re.compile('application/octet-stream')
urlencoded_pattern = re.compile('application/x-www-form-urlencoded')
json_pattern = re.compile('application/json')
form_data_pattern = re.compile('multipart/form-data')
xml_pattern = re.compile(r'.*?/xml')
text_pattern = re.compile('text/plain')


@catch_exc()
async def handle_start(request: Request):
    params_log = f'>>>{dict(request.headers.items())}|{request.client.host}|' \
                 f'{request.method}|{request.url.path}\n'
    params = request.query_params
    if params:
        params_log += f"Query: {dict(params.items())}\n"
    body = await request.body()
    if body:
        content_type = request.headers.get("content-type")
        if re.match(json_pattern, content_type):
            json_params = await request.json()
            params_log += f"Json: {format_long_val(json_params)}\n"
        elif any([
            re.match(form_data_pattern, content_type),
            re.match(urlencoded_pattern, content_type)
        ]):
            form_params = dict((await request.form()).items())
            params_log += f'Form: {form_params}\n'
        elif re.match(xml_pattern, content_type):
            params_log += f'Xml: {body.decode()}\n'
        elif re.match(text_pattern, content_type):
            params_log += f'Text: {body.decode()}\n'
        else:
            pass
    logger.info(params_log[:-1])


class ContextAPIRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()
        
        async def handle_end(request: Request) -> Response:
            await handle_start(request)
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = round((time.time() - before) * 1000, 3)
            logger.info(f'<<<{request.client.host}|{request.method}|{request.url.path}|process: {duration}ms\n')
            return response
        
        return handle_end


class UdfAPIRoute(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, route_class=ContextAPIRoute, **kwargs)
