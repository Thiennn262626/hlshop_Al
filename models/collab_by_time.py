import pandas as pd
from datetime import datetime, timedelta
from controllers.order import get_order_list


def training_collab_by_time():
    orders_df = get_order_list()
    orders_df['orderDate'] = pd.to_datetime(orders_df['orderDate'])

    current_date = datetime.now()
    start_date = current_date - timedelta(days=7)
    end_date = current_date + timedelta(days=14)
    orders_df['year'] = orders_df['orderDate'].dt.year
    years = orders_df['year'].unique().tolist()
    if current_date.year in years:
        years.remove(current_date.year)

    # Tính các sản phẩm được mua nhiều nhất trong 1 tiếng qua
    hour_data = orders_df[(orders_df['orderDate'] >= current_date - timedelta(hours=1)) & (orders_df['orderDate'] <= current_date)]
    hour_product_counts = hour_data.groupby('productID')['quantity'].sum().sort_values(ascending=False)
    product_trending_hour = hour_product_counts.head(15).index.tolist()
    # Tính các sản phẩm được mua nhiều nhất trong tuần qua
    week_data = orders_df[(orders_df['orderDate'] >= start_date) & (orders_df['orderDate'] <= current_date)]
    week_product_counts = week_data.groupby('productID')['quantity'].sum().sort_values(ascending=False)
    product_trending = week_product_counts.head(30).index.tolist()
    # Tính các sản phẩm được mua nhiều nhất trong 2 tuần tới so với các năm trước
    filtered_data = pd.DataFrame()
    for year in years:
        start_date_year = start_date.replace(year=year)
        end_date_year = end_date.replace(year=year)
        yearly_data = orders_df[(orders_df['orderDate'] >= start_date_year) & (orders_df['orderDate'] <= end_date_year)].sort_values(by='orderDate')
        filtered_data = pd.concat([filtered_data, yearly_data])

    product_counts = filtered_data.groupby('productID')['quantity'].sum().sort_values(ascending=False)
    print(product_counts.head(80))
    products_time_range = product_counts.head(80).index.tolist()
    # Kết hợp 3 danh sách sản phẩm trên
    combined_top_products = list(set(product_trending_hour + product_trending + products_time_range))

    return combined_top_products
