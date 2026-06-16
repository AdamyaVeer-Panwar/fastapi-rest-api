import asyncio
import json

from redis_client import redis_client
import asyncio

async def start_subscriber():

    pubsub = redis_client.pubsub()

    await pubsub.subscribe("task_created")

    print("Notification Service is listening...")

    while True:

        message = await pubsub.get_message(
            ignore_subscribe_messages=True
        )

        if message:

            data = json.loads(
                message["data"]
            )

            print(
                "Notification received:",
                data
            )

        await asyncio.sleep(0.1)



if __name__ == "__main__":
    asyncio.run(start_subscriber())