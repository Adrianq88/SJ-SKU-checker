from flask import Flask, request, render_template
import pandas as pd
from sneakersjoint import search_sku_on_site as search_sneakersjoint
from aplug import scrape_aplug_product_by_sku as search_aplug

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    sneakersjoint_details = None
    if request.method == 'POST':
        sku = request.form['sku']
        sneakersjoint_df = search_sneakersjoint(sku)

        if sneakersjoint_df is not None and not sneakersjoint_df.empty:
            sneakersjoint_details = sneakersjoint_df

    return render_template('index.html',
                           sneakersjoint_details=sneakersjoint_details)

if __name__ == "__main__":
    app.run(debug=True)
