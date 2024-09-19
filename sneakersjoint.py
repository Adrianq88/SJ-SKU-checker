import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base search URL
search_url = "https://sneakersjoint.com/?s={}&post_type=product"

# Function to perform search and get product links
def get_product_links_for_sku(sku):
    url = search_url.format(sku)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all product links on the search result page
    product_links = [a['href'] for a in soup.find_all('a', class_='woocommerce-LoopProduct-link')]

    print("Total Product Links Found:", len(product_links))  # Debugging statement
    return product_links

# Function to scrape SKU, size, and price details from each product page
def get_product_details(product_url, target_sku):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    model_name = soup.find('h1', class_='product_title').text.strip()

    size_price_list = []

    # Find size elements with price data
    sizes = soup.find_all('div', class_='woovr-variation')
    if sizes:
        for size in sizes:
            sku = size['data-sku']
            print(f"Checking SKU: {sku} on page: {product_url}")  # Debugging statement
            if sku == target_sku:
                size_text = size['data-attrs'].split(":")[1].strip('"') + " EU"
                price_text = size['data-price']
                size_price_list.append((model_name, sku, size_text, price_text, product_url))
                print("Model:", model_name, "SKU:", sku, "Size:", size_text, "Price:", price_text, "Link:", product_url)  # Debugging statement
    return size_price_list

def search_sku_on_site(sku):
    # Get product links for the given SKU
    product_links = get_product_links_for_sku(sku)

    # Collect all product details for the given SKU
    all_product_details = []
    processed_links = set()
    for link in product_links:
        if link not in processed_links:
            try:
                print(f"Processing link: {link}")  # Debugging statement
                details = get_product_details(link, sku)
                if details:
                    all_product_details.extend(details)
                processed_links.add(link)
            except Exception as e:
                print(f"Error scraping {link}: {e}")

    if all_product_details:
        # Remove duplicates
        all_product_details = list(set(all_product_details))

        # Create a DataFrame
        df = pd.DataFrame(all_product_details, columns=['Model', 'SKU', 'Size', 'Price', 'Link'])

        # Sort the DataFrame by the Size column
        df['Size'] = df['Size'].apply(lambda x: float(x.replace('-5"', '.5').replace('"', '').replace(' EU', '').replace('}', '')))
        df = df.sort_values(by='Size')

        # Add " EU" to sizes
        df['Size'] = df['Size'].apply(lambda x: f"{x} EU")

        # Save to Excel
        df.to_excel('sneakers_prices_with_sku.xlsx', index=False)

        print("Data scraped and saved to sneakers_prices_with_sku.xlsx")
        return df
    else:
        print("No products found with the given SKU.")
        return None
