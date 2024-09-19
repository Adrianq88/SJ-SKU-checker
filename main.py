import re
from sneakersjoint import get_product_links_for_sku as sj_get_product_links, get_product_details as sj_get_product_details

def extract_keywords(model_name):
    # Extract keywords for colorway and collaboration
    keywords = re.findall(r'\b(?:Travis|Scott|Canary|Yellow|OG|Retro|Low|SP|Nike|Jordan|High|Pack)\b', model_name, re.IGNORECASE)
    return " ".join(keywords)

def search_sku_on_sites(sku):
    # Search on Sneakers Joint
    print("Searching on Sneakers Joint...")
    sj_product_links = sj_get_product_links(sku)
    print("Total Product Links Found on Sneakers Joint:", len(sj_product_links))

    all_product_details = []

    for link in sj_product_links:
        try:
            print(f"Processing link on Sneakers Joint: {link}")
            details = sj_get_product_details(link, sku)
            if details:
                all_product_details.extend(details)
        except Exception as e:
            print(f"Error scraping {link}: {e}")

    if all_product_details:
        print("Data from Sneakers Joint found.")
        # Extract model name from the first detail
        model_name = all_product_details[0][0]
        keywords = extract_keywords(model_name)
    else:
        print("No data found on Sneakers Joint.")
        keywords = sku  # Fall back to using the SKU as the search term

if __name__ == "__main__":
    target_sku = input("Enter the SKU to search for: ")
    search_sku_on_sites(target_sku)
