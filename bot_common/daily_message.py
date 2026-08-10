# bot_common/daily_message.py

import asyncio
import random
from datetime import datetime, timedelta
from typing import Awaitable, Callable


async def daily_message_loop(
    *,
    send_message: Callable[[str], Awaitable[None]],
    timezone,
    base_hour: int = 7,
    base_minute: int = 0,
    normal_probability: float = 0.12,
    nebou_probability: float = 0.02,
    hayai_probability: float = 0.02,
    normal_range: tuple[int, int] = (-30, 30),
    nebou_range: tuple[int, int] = (180, 210),
    hayai_range: tuple[int, int] = (-210, -180),
    message_builder: Callable[[str], str] = lambda status: "",
):
    while True:
        now = datetime.now(timezone)

        base_time = now.replace(
            hour=base_hour,
            minute=base_minute,
            second=0,
            microsecond=0,
        )

        probability = random.random()

        if probability < nebou_probability:
            offset = random.randint(*nebou_range)
            status = "nebou"

        elif probability < nebou_probability + hayai_probability:
            offset = random.randint(*hayai_range)
            status = "hayai"

        elif probability < (
            nebou_probability
            + hayai_probability
            + normal_probability
        ):
            offset = random.randint(*normal_range)
            status = "normal"

        else:
            offset = random.randint(*normal_range)
            status = "none"

        target = base_time + timedelta(minutes=offset)

        if target <= now:
            target += timedelta(days=1)

        wait_seconds = (target - now).total_seconds()

        print(
            f"次回の定期メッセージ: "
            f"{target.strftime('%Y-%m-%d %H:%M:%S')} "
            f"status: {status}"
        )

        await asyncio.sleep(wait_seconds)

        if status == "none":
            continue

        message = message_builder(status)

        if message:
            await send_message(message)