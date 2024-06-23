import pandas as pd
from dbs.connection_hander import db_connection


def get_rating_list():
    ratings_db = db_connection.fetch_data(
        "SELECT r.id_user AS userId, p.id AS productId, r.product_quality AS rating, r.created_date AS timestamp "
        "FROM [Rating] AS r "
        "INNER JOIN ProductSku AS ps ON r.product_sku_id = ps.id "
        "INNER JOIN Product AS p ON ps.idProduct = p.id "
        "ORDER BY r.id_user"
    )
    dataOriginal = [
        [
            rating[0],
            rating[1],
            rating[2],
            rating[3].strftime("%Y-%m-%d %H:%M:%S"),
        ]
        for rating in ratings_db
    ]
    print("data", len(dataOriginal))

    ratings_df = pd.DataFrame(
        dataOriginal, columns=["userId", "productId", "rating", "timestamp"]
    )

    return ratings_df