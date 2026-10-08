import os
import json
import requests
from datetime import datetime
HISTORY_FILE = "stock_history.json"

BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

PRODUCT_URL = "https://www.zara.com/tr/tr/kemerli-pensli-genis-paca-pantolon-p02949228.html?v1=555448606"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120 Safari/537.36"
    ),
    "Accept-Language": "tr-TR,tr;q=0.9"
}


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
    def gecmis_kaydet(durum):

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            gecmis = json.load(f)

    except:
        gecmis = []


    kayit = {
        "tarih": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
        "urun": "Kemerli Pensli Geniş Paça Pantolon",
        "beden": "XS",
        "durum": durum
    }


    gecmis.append(kayit)


    # Son 100 kaydı tut
    gecmis = gecmis[-100:]


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


def zara_verisi_al():

    response = requests.get(
        PRODUCT_URL,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    return response.text


def xs_stok_kontrol():

    html = zara_verisi_al().lower()

    # Zara sayfasında beden bilgisi aranıyor
    xs_kelimesi = '"xs"' in html or "xs" in html

    # Satın alınabilirlik göstergeleri
    stok_isareti = (
        "addtocart" in html
        or "add to cart" in html
        or "sepete ekle" in html
    )

    return xs_kelimesi and stok_isareti


def main():

    print("Zara XS kontrol başladı")

    try:

        stok_var = xs_stok_kontrol()

        zaman = datetime.now().strftime("%d.%m.%Y %H:%M")

        if stok_var:
            gecmis_kaydet("XS stokta")

            mesaj = (
                "🚨 ZARA XS STOK BİLDİRİMİ 🚨\n\n"
                "Ürün:\n"
                "Kemerli Pensli Geniş Paça Pantolon\n\n"
                "Beden: XS\n\n"
                f"Kontrol: {zaman}\n\n"
                f"{PRODUCT_URL}"
            )

            telegram_gonder(mesaj)

            print("XS bulundu, bildirim gönderildi.")

        else:
            gecmis_kaydet("XS stokta değil")
            print(
                f"{zaman} - XS stokta görünmüyor."
            )

    except Exception as hata:

        print(
            "Kontrol hatası:",
            hata
        )


if __name__ == "__main__":
    main()
