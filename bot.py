import os
import json
import requests

BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")

PRODUCT_FILE = "products.json"


def telegram_get_updates(offset=None):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

    params = {}

    if offset:
        params["offset"] = offset

    return requests.get(
        url,
        params=params,
        timeout=30
    ).json()


def mesaj_gonder(chat_id, text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": chat_id,
            "text": text
        },
        timeout=20
    )


def urunleri_oku():

    with open(
        PRODUCT_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def urunleri_yaz(urunler):

    with open(
        PRODUCT_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            urunler,
            f,
            ensure_ascii=False,
            indent=2
        )


def komut_isle(chat_id, mesaj):

    if mesaj.startswith("/liste"):

        urunler = urunleri_oku()

        if not urunler:
            mesaj_gonder(
                chat_id,
                "Takip edilen ürün yok."
            )
            return

        cevap = "📋 Takip listesi:\n\n"

        for i, urun in enumerate(urunler, 1):

            cevap += (
                f"{i}) {urun['name']}\n"
                f"Beden: {', '.join(urun['sizes'])}\n\n"
            )

        mesaj_gonder(chat_id, cevap)


    elif mesaj.startswith("/ekle"):

        parcalar = mesaj.split()

        if len(parcalar) < 3:

            mesaj_gonder(
                chat_id,
                "Kullanım:\n/ekle LINK BEDEN"
            )
            return


        link = parcalar[1]
        beden = parcalar[2].upper()


        urunler = urunleri_oku()


        urunler.append(
            {
                "name": "Yeni Zara Ürünü",
                "url": link,
                "sizes": [beden]
            }
        )


        urunleri_yaz(urunler)


        mesaj_gonder(
            chat_id,
            "✅ Ürün takip listesine eklendi."
        )


    elif mesaj.startswith("/yardim"):

        mesaj_gonder(
            chat_id,
            "Komutlar:\n\n"
            "/ekle LINK BEDEN\n"
            "/liste\n"
            "/yardim"
        )


def main():

    print("Telegram bot başladı")

    offset = None

    while True:

        data = telegram_get_updates(offset)

        for update in data.get("result", []):

            offset = update["update_id"] + 1

            mesaj = update.get(
                "message",
                {}
            )

            chat_id = mesaj.get("chat", {}).get("id")

            text = mesaj.get("text", "")

            if chat_id and text:

                komut_isle(
                    chat_id,
                    text
                )


if __name__ == "__main__":
    main()
