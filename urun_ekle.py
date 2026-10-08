import json
import os

PRODUCT_FILE = "products.json"

name = os.environ.get("PRODUCT_NAME", "Yeni Zara Ürünü")
url = os.environ.get("PRODUCT_URL")
size = os.environ.get("PRODUCT_SIZE")


with open(PRODUCT_FILE, "r", encoding="utf-8") as f:
    products = json.load(f)


products.append(
    {
        "name": name,
        "url": url,
        "sizes": [
            size.upper()
        ]
    }
)


with open(PRODUCT_FILE, "w", encoding="utf-8") as f:
    json.dump(
        products,
        f,
        ensure_ascii=False,
        indent=2
    )


print("Ürün eklendi:")
print(name, size)
