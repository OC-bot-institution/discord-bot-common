
import random
import asyncio
import re
from itertools import product
import unicodedata

from pathlib import Path
import json
def load_json(filename):
    path = Path(__file__).parent / filename
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# 待ち時間設定
base = 0.8
per_char = 0.1


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.lower()
    text = re.sub(r"[!！?？〜～ー\-…・、。,\.\s]", "", text)
    return text


def expand_keys(keys: list[str], keywords: dict) -> list[str]:
    expanded = []

    for key in keys:

        # &で始まるキーワードをすべて取得
        tokens = re.findall(r"&([^&]+)&", key)

        if not tokens:
            expanded.append(key)
            continue

        # 各トークンの候補一覧
        candidates = []
        for token in tokens:
            if token in keywords:
                candidates.append(keywords[token])
            else:
                # 定義されていないものはそのまま残す
                candidates.append([f"&{token}&"])

        # 全組み合わせを生成
        for words in product(*candidates):
            result = key
            for token, word in zip(tokens, words):
                result = result.replace(f"&{token}&", word, 1)
            expanded.append(result)

    return expanded

def get_user_name(
    message,
    names: dict[str, str]
) -> str:

    user_id = str(message.author.id)

    if user_id in names:
        return names[user_id]

    return message.author.display_name


async def mention_reply(message, mentions, user_name):
    reply = random.choice(mentions["replies"])
    reply = reply.replace("&user&", user_name)

    await message.reply(
        reply,
        mention_author=False
    )
    return

#共通関数
async def special_reply(message, rules, keywords, user_name, judge):
    text = normalize(message.content)

    for rule in rules:

        if random.random() > rule["probability"]:
            continue
        keys = expand_keys(rule["keys"], keywords)
        if any(judge(text, normalize(key)) for key in keys):
            reply = random.choice(rule["replies"])
            reply = reply.replace("&user&", user_name)
            wait = base + len(reply) * per_char + random.uniform(0, 1.2)
            
            async with message.channel.typing():
                await asyncio.sleep(wait)
            await message.reply(
                reply,
                mention_author=False
            )

            return True

    return False

#完全一致
async def special_reply_exact(message, rules, keywords, user_name):
    return await special_reply(
        message,
        rules,
        keywords,
        user_name,
        lambda t, k: t == k
    )

#部分一致

async def special_reply_contains(message, rules, keywords, user_name):
    return await special_reply(
        message,
        rules,
        keywords,
        user_name,
        lambda t, k: k in t
    )


async def special_reply_endswith(message, rules, keywords, user_name):
    return await special_reply(
        message,
        rules,
        keywords,
        user_name,
        lambda t, k: t.endswith(k)
    )


async def special_reply_ordered(message, rules, keywords, user_name):
    return await special_reply(
        message,
        rules,
        keywords,
        user_name,
        contains_in_order
    )


def contains_in_order(text: str, pattern: str) -> bool:
    if not pattern:
        return False
    index = 0
    for ch in text:
        if ch == pattern[index]:
            index += 1
            if index == len(pattern):
                return True
    return False

