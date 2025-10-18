import requests
from bs4 import BeautifulSoup
import sys
import json
import re


def get_product_info(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        product_info = {}
        product_info["title"] = (
            soup.find("h1").get_text(strip=True) if soup.find("h1") else "N/A"
        )
        price_div = soup.find("div", class_="brutto-price-ui")
        if price_div:
            price_text = price_div.get_text(strip=True, separator=" ").replace("\n", " ").strip()
            numeric_part = price_text.replace("EUR", "").replace(",", ".").split()[0]
            product_info["price"] = numeric_part
        else:
            product_info["price"] = "N/A"
        availability_el = soup.find("div", class_="availability-ui")
        product_info["availability"] = (
            availability_el.get_text(strip=True).replace("Availability:", "").strip()
            if availability_el
            else "N/A"
        )
        product_info["url"] = url
        desc_elem = soup.find("meta", attrs={"name": "description"})
        product_info["description"] = (
            desc_elem.get("content", "N/A") if desc_elem else "N/A"
        )

        composition_div = soup.find("div", id="composition")
        if composition_div:
            p_tag = composition_div.find("p")
            if p_tag:
                ingredients_text = p_tag.get_text(strip=True).replace("Ingredients:", "").strip()
                ingredients_list = [ingredient.strip() for ingredient in ingredients_text.split(",") if ingredient.strip()]
                product_info['ingredients'] = str(ingredients_list if ingredients_list else "N/A")
            else:
                product_info['ingredients'] = "N/A"
        else:
            product_info['ingredients'] = "N/A"
        
        features_div = soup.find("div", id="attributes").find("ul")
        default_features_keys = [
            "upc_code",
            "capacity",
            "action",
            "type_of_skin",
            "time_of_application",
            "way_of_use",
            "cautions",
            "responsible_person",
            "adress_responsible_person",
        ]
        product_info.update({key: "N/A" for key in default_features_keys})

        if features_div:
            for li in features_div.find_all("li"):
                name_el = li.find("div", class_="name-ui")
                value_el = li.find("div", class_="value-ui")

                if name_el:
                    # Normalize key
                    key = name_el.get_text(strip=True).lower()
                    key = re.sub(r"[^a-z0-9]+", "_", key).strip("_")

                    # Only update if the key is in defaults
                    if key in default_features_keys:
                        value = value_el.get_text(strip=True) if value_el and value_el.get_text(strip=True) else "N/A"
                        product_info[key] = value


        return product_info

    except requests.exceptions.RequestException as e:
        return {"error": "Failed to fetch URL", "url": url, "details": str(e)}
    except Exception as e:
        return {"error": "Failed to parse product info", "url": url, "details": str(e)}


if __name__ == "__main__":
    all_products = []

    # Read URLs from stdin (e.g. cat urls.txt | python get_product_info.py)
    for line in sys.stdin:
        url = line.strip()
        if not url:
            continue
        product = get_product_info(url)
        all_products.append(product)
    attributeKeys = [
        "url",
        "title",
        "price",
        "availability",
        "upc_code",
        "capacity",
        "action",
        "type_of_skin",
        "time_of_application",
        "way_of_use",
        "cautions",
        "responsible_person",
        "adress_responsible_person",
        "ingredients"
    ]

    for product in all_products:
        tsvString = ""
        for key in attributeKeys:
            tsvString += product[key] + "\t"
        print(tsvString)
