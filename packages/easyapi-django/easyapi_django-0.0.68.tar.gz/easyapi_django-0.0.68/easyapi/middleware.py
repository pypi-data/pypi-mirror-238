import os
import json

from asgiref.sync import iscoroutinefunction, markcoroutinefunction

from redis import asyncio as aioredis

from settings.env import REDIS_PREFIX
from .tenant.tenant import aset_tenant

REDIS_SERVER = os.environ['REDIS_SERVER']
REDIS_DB = 1


class AuthMiddleware:
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    async def __call__(self, request):
        session_key = request.COOKIES.get('sid')
        request.account_id = None
        request.authenticated = None
        request.session = None

        if session_key:
            redis = await aioredis.Redis(
                host=REDIS_SERVER, db=REDIS_DB, decode_responses=True
            ).client()
            prefix = f'{REDIS_PREFIX}:' if REDIS_PREFIX else ''
            session_key = f'{prefix}sessions:{session_key}'
            session = await redis.get(session_key)
            await redis.close()
            await redis.connection_pool.disconnect()

            if session:
                session = json.loads(session)
                request.user = session['user']
                if session.get('account_id'):
                    await aset_tenant(session['account_id'])
                    request.account_id = session['account_id']
                    request.authenticated = session.get('user', 'false') != 'false'
                    request.session = session

        response = await self.get_response(request)
        return response


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, _, exception):
        try:
            getattr(exception, "render")
        except AttributeError:
            return None

        return exception.render(exception)
