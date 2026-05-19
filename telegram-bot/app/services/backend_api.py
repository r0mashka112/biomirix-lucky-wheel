import httpx

from app.core.config import settings

class BackendAPI:
    BACKEND_URL = settings.BACKEND_URL

    @classmethod
    async def get_event(cls):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f'{cls.BACKEND_URL}/api/event'
            )

            return response.json()