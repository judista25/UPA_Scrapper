import requests
from bs4 import BeautifulSoup
import sys

def get_product_urls():
    urls = []
    for i in range(3,20):
        try:    
            # Example: scraping from a test e-commerce site
            base_base_url = "https://skincare.pl/en/"
            base_url = "{}products/skin-cincerns-and-needs/2-230?pageId={}".format(base_base_url, i)
            response = requests.get(base_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            products = soup.find_all(attrs={"data-product-id": True})
            for p in products:
                url = base_base_url + p.get("data-url")  # relative URL
                if(urls.__contains__(url) != True):
                    urls.append(url)
            
        except Exception as e:
            print(f"❌ Error for {base_url}: {e}", file=sys.stderr)
            continue
        
    for url in urls:
        print(url)
    print(f"Size of URLS",len(urls),file=sys.stderr)
    

if __name__ == "__main__":
    get_product_urls()