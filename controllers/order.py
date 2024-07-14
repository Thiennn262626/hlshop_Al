import pandas as pd
from dbs.connection_hander import ConnectionHandler
def get_order_list():
    db_connection = ConnectionHandler()
    orders_db = db_connection.fetch_data(
        "SELECT o.idUser AS userID, oi.product_id AS productID, oi.quantity, o.createdDate AS orderDate "
        "FROM Order_item AS oi "
        "JOIN [Order] AS o ON o.id = oi.orderId "
    )
    db_connection.close_connection()
    dataOriginal = [
        [
            order[0],
            order[1],
            order[2],
            order[3].strftime("%Y-%m-%d %H:%M:%S"),
        ]
        for order in orders_db
    ]
    print("data", len(dataOriginal))

    ratings_df = pd.DataFrame(
        dataOriginal, columns=["userID", "productID", "quantity", "orderDate"]
    )

    return ratings_df