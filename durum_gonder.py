import os
import json
from datetime import datetime
import requests


BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

PRODUCT_FILE = "products.json"
STATE_FILE = "stock_state.json"


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

    with open(PRODUCT_FILE, "r", encoding="utf-8") as f:
        urunler = json.load(f)


    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            durumlar = json.load(f)

    except:
        durumlar = {}


    mesaj = "📊 Zara Durum Raporu\n\n"


    for urun in urunler:

        mesaj += f"🛍 {urun['name']}\n"

        for beden in urun["sizes"]:

            anahtar = (
                urun["name"]
                + "_"
                + beden
            )

            if durumlar.get(anahtar):

                mesaj += f"{beden} ✅ Stokta\n"

            else:

                mesaj += f"{beden} ❌ Stok yok\n"


        mesaj += "\n"


    mesaj += (
        "Son kontrol:\n"
        + datetime.now().strftime("%d.%m.%Y %H:%M")
    )


    telegram_gonder(mesaj)


if __name__ == "__main__":
    main()
