import pandas as pd
from dbs.connection_hander import ConnectionHandler

# 		WITH RankedRatings AS (
#     SELECT
#         r.id_user AS userId,
#         p.id AS productId,
#         r.product_quality AS rating,
#         r.created_date AS timestamp,
#         ROW_NUMBER() OVER (PARTITION BY r.id_user, p.id ORDER BY r.created_date DESC) AS row_num
#     FROM
#         [Rating] AS r
#     INNER JOIN
#         ProductSku AS ps ON r.product_sku_id = ps.id
#     INNER JOIN
#         Product AS p ON ps.idProduct = p.id
# )
# SELECT
#     userId,
#     productId,
#     rating,
#     timestamp
# FROM
#     RankedRatings
# WHERE
#     row_num = 1
# ORDER BY
#     userId;
def get_rating_list():
    db_connection = ConnectionHandler()
    ratings_db = db_connection.fetch_data(
        "WITH RankedRatings AS (SELECT r.id_user AS userId, p.id AS productId, r.product_quality AS rating, r.created_date AS timestamp, ROW_NUMBER() OVER (PARTITION BY r.id_user, p.id ORDER BY r.created_date DESC) AS row_num FROM [Rating] AS r INNER JOIN ProductSku AS ps ON r.product_sku_id = ps.id INNER JOIN Product AS p ON ps.idProduct = p.id) "
        "SELECT userId, productId, rating, timestamp FROM RankedRatings WHERE row_num = 1 ORDER BY userId;"
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