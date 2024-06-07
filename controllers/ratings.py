import pandas as pd
import requests

def get_rating_list():
    try:
        ratings_db = requests.get('https://hlshop.azurewebsites.net/api/hlshop/training/get-rating-for-python-service')
        ratings_db.raise_for_status()  # Raises exception for non-200 responses
        ratings_data = ratings_db.json()['data']

        data_original = []
        for rating in ratings_data:
            user_id = rating.get('userId')
            product_id = rating.get('productId')
            rating_val = rating.get('rating')
            timestamp = rating.get('timestamp')
            if user_id and product_id and rating_val and timestamp:
                data_original.append([user_id, product_id, rating_val, timestamp])

        ratings_df = pd.DataFrame(data_original, columns=["userId", "productId", "rating", "timestamp"])
        return ratings_df
    except requests.exceptions.RequestException as e:
        print("Error fetching data from API:", e)
        return None