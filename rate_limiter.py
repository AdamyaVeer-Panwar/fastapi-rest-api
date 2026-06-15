from fastapi import HTTPException

from redis_client import redis_client

REQUEST_LIMIT = 5
WINDOW_SECONDS = 60


async def rate_limiter():

    print("RATE LIMITER CALLED")


    key = "rate_limit:test_user"

    count = await redis_client.incr(key)

    if count == 1:
        await redis_client.expire(
            key,
            WINDOW_SECONDS
        )

    if count > REQUEST_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )