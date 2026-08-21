import asyncio
import random
from pathlib import Path


ICON_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
}


async def change_icon(bot, icon_dir: str | Path = "icon"):
    """
    icon_dir内の「icon」で始まる画像からランダムに1枚選び、
    Botのアイコンを変更する。
    """

    icon_dir = Path(icon_dir)

    if not icon_dir.exists():
        print(f"アイコンフォルダが見つかりません: {icon_dir}")
        return

    icon_files = [
        path
        for path in icon_dir.iterdir()
        if (
            path.is_file()
            and path.name.startswith("icon")
            and path.suffix.lower() in ICON_EXTENSIONS
        )
    ]

    if not icon_files:
        print(f"アイコン画像が見つかりません: {icon_dir}")
        return

    icon_path = random.choice(icon_files)

    try:
        with icon_path.open("rb") as f:
            await bot.user.edit(avatar=f.read())

        print(f"アイコンを変更しました: {icon_path}")

    except Exception as e:
        print(f"アイコンの変更に失敗しました: {e}")


async def icon_loop(
    bot,
    icon_dir: str | Path = "icon",
):
    """
    1週間ごとにBotのアイコンを変更する。
    """

    while True:
        await asyncio.sleep(7 * 24 * 60 * 60)
        await change_icon(bot, icon_dir)