import os
import json
import requests
from datetime import datetime
with open("products.json", "r", encoding="utf-8") as f:
    PRODUCTS = json.load(f)


BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

HISTORY_FILE = "stock_history.json"
STATE_FILE = "stock_state.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120 Safari/537.36"
    ),
    "Accept-Language": "tr-TR,tr;q=0.9"
}

durumlar = durum_oku()

anahtar = (
    urun["name"]
    + "_"
    + beden
)


daha_once_var = durumlar.get(
    anahtar,
    False
)


if not daha_once_var:

    telegram_gonder(mesaj)


durumlar[anahtar] = True

durum_yaz(durumlar)
def telegram_gonder(mesaj):

    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram bilgileri eksik")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": mesaj
        },
        timeout=20
    )


def gecmis_kaydet(urun, beden, durum):

    try:
        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:
            gecmis = json.load(f)

    except:
        gecmis = []


    gecmis.append(
        {
            "tarih": datetime.now().strftime(
                "%d.%m.%Y %H:%M:%S"
            ),
            "urun": urun,
            "beden": beden,
            "durum": durum
        }
    )


    gecmis = gecmis[-200:]
def durum_oku():

    try:
        with open(
            STATE_FILE,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)

    except:
        return {}


def durum_yaz(durum):

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            durum,
            f,
            ensure_ascii=False,
            indent=2
        )

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            gecmis,
            f,
            ensure_ascii=False,
            indent=2
        )


def urun_kontrol(urun):

    try:

        response = requests.get(
            urun["url"],
            headers=HEADERS,
            timeout=30
        )

        html = response.text.lower()


        bulunan_bedenler = []


        for beden in urun["sizes"]:

            if beden.lower() in html:

                # Satın alma işareti kontrolü
                if (
                    "addtocart" in html
                    or "add to cart" in html
                    or "sepete ekle" in html
                ):
                    bulunan_bedenler.append(beden)


        return bulunan_bedenler


    except Exception as hata:

        print(
            urun["name"],
            "hata:",
            hata
        )

        return []


def main():

    print(
        "Zara çoklu ürün kontrol başladı"
    )


    for urun in PRODUCTS:

        stoklar = urun_kontrol(urun)


        if stoklar:

            for beden in stoklar:

                mesaj = (
                    "🚨 ZARA STOK BİLDİRİMİ 🚨\n\n"
                    f"Ürün: {urun['name']}\n"
                    f"Beden: {beden}\n\n"
                    f"{urun['url']}"
                )


                telegram_gonder(mesaj)


                gecmis_kaydet(
                    urun["name"],
                    beden,
                    "Stokta"
                )


                print(
                    "Stok bulundu:",
                    urun["name"],
                    beden
                )


        else:

            for beden in urun["sizes"]:

                gecmis_kaydet(
                    urun["name"],
                    beden,
                    "Stok yok"
                )


                print(
                    "Stok yok:",
                    urun["name"],
                    beden
                )
durumlar = durum_oku()

anahtar = (
    urun["name"]
    + "_"
    + beden
)

durumlar[anahtar] = False

durum_yaz(durumlar)

if __name__ == "__main__":
    main()
