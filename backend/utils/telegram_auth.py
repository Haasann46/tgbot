import hmac
import hashlib
import urllib.parse
import json


def check_telegram_auth(init_data: str, bot_token: str) -> dict:
    data = dict(urllib.parse.parse_qsl(init_data, strict_parsing=True))

    telegram_hash = data.pop("hash", None)
    if not telegram_hash:
        raise ValueError("hash not found")

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(data.items())
    )

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()

    if calculated_hash != telegram_hash:
        raise ValueError("invalid signature")

    if "user" in data:
        data["user"] = json.loads(data["user"])

    return data
