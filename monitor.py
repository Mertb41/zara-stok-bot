import os
import time
import requests
from datetime import datetime

# Telegram bilgileri GitHub Secrets'tan gelecek
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# Takip edilecek Zara ürünü
PRODUCT_URL = "https://www.zara.com/tr/tr/kemerli-pensli-genis-paca-pantolon-p02949228.html?v1=555448606"

CHECK_INTERVAL = 300  # 5 dakika

bildirim_gonderildi = False


def telegram_gonder(mesaj):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram bilgileri eksik!")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": mesaj
        }
    )


def stok_kontrol():

    global bildirim_gonderildi

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/120 Safari/537.36"
        )
    }

    try:
        response = requests.get(
            PRODUCT_URL,
            headers=headers,
            timeout=20
        )

        sayfa = response.text.lower()

        # XS ve sepete ekleme kontrolü
        xs_var = "xs" in sayfa
        sepete_ekle = (
            "add to cart" in sayfa
            or "sepete ekle" in sayfa
        )

        zaman = datetime.now().strftime("%d.%m.%Y %H:%M")

        if xs_var and sepete_ekle:

            if not bildirim_gonderildi:

                telegram_gonder(
                    "🚨 ZARA STOK BİLDİRİMİ 🚨\n\n"
                    "Ürün:\n"
                    "Kemerli Pensli Geniş Paça Pantolon\n\n"
                    "Beden: XS\n\n"
                    f"Kontrol zamanı: {zaman}\n\n"
                    f"{PRODUCT_URL}"
                )

                bildirim_gonderildi = True

                print("Bildirim gönderildi.")

        else:
            bildirim_gonderildi = False
            print(
                f"{zaman} - XS stokta değil."
            )

    except Exception as hata:
        print("Hata:", hata)


if __name__ == "__main__":

    print("Zara stok takip başladı...")

    while True:
        stok_kontrol()
        time.sleep(CHECK_INTERVAL)
