import os
import json
import requests

BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

PRODUCT_FILE = "products.json"


def telegram_gonder(mesaj):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": mesaj
        },
        timeout=20
    )


def main():

    with open(
        PRODUCT_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        urunler = json.load(f)


    mesaj = "📋 Zara Takip Listesi\n\n"


    for i, urun in enumerate(urunler, 1):

        mesaj += (
            f"{i}) {urun['name']}\n"
            f"Beden: {', '.join(urun['sizes'])}\n\n"
        )


    telegram_gonder(mesaj)


if __name__ == "__main__":
    main()
