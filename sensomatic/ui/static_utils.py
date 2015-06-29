import asyncio
import logging
from aiohttp import web
import os
from react import jsx


logger = logging.getLogger('static')


@asyncio.coroutine
def static_handler(request):
    path = request.match_info['path']
    full_path = os.path.join(os.path.dirname(__file__), 'static', path)
    content = open(full_path, 'br').read()
    if full_path.endswith('.jsx'):
        logger.debug("JSX->JS conversion of {} ({})".format(path, full_path))
        transformer = jsx.JSXTransformer()
        content = transformer.transform_string(content.decode()).encode()

    return web.Response(body=content)
