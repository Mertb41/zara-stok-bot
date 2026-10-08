import json
import os


PRODUCT_FILE = "products.json"

PRODUCT_INDEX = int(
    os.environ.get("PRODUCT_INDEX")
)


with open(
    PRODUCT_FILE,
    "r",
    encoding="utf-8"
) as f:
    products = json.load(f)


if PRODUCT_INDEX < 1 or PRODUCT_INDEX > len(products):

    print("Geçersiz ürün numarası")
    exit(1)


silinen = products.pop(
    PRODUCT_INDEX - 1
)


with open(
    PRODUCT_FILE,
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        products,
        f,
        ensure_ascii=False,
        indent=2
    )


print(
    "Silindi:",
    silinen["name"]
)
