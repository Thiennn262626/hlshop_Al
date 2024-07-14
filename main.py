from flask import Flask
from dotenv import load_dotenv
from flask import jsonify, make_response
import numpy as np



load_dotenv()
app = Flask(__name__)

from models.loader import Loader, LoaderStartTrain
from models.collaborative_filtering import CF
from models.collab_by_time import training_collab_by_time
from dbs.redis import Redis

@app.route("/", methods=["GET"])
def read_root():
    return {"Hello": "World"}

@app.route('/train-full', methods=['GET'])
def train_full():
    redis_instance = Redis()
    train_set = Loader()
    r_cols = ["user_id", "item_id", "rating"]
    new_df = train_set.ratings.copy()
    new_df.rename(
        columns={"userId": "user_id", "productId": "item_id"}, inplace=True
    )
    new_df = new_df[r_cols]
    Y_data = new_df.values
    rs = CF(Y_data, k=2, uuCF=1)
    rs.fit()
    for u in range(rs.n_users):
            recommended_items = rs.recommend(u)
            idUser = train_set.idx2userid[u]
            values = [
                train_set.idx2productid[item]
                for item in recommended_items
                if item in train_set.idx2productid
            ]
            print(f"{u}: {idUser} - {recommended_items}: {values}")
            key = f"collaborative_filtering_user_{idUser}"
            redis_instance.set_redis_data(key, values)
    return make_response(jsonify({"result": "Training completed"}), 200)

# @app.route('/train-full-item-item', methods=['GET'])
# def train_full_item_item():
#     redis_instance = Redis()
#     train_set = Loader()
#     r_cols = ["user_id", "item_id", "rating"]
#     new_df = train_set.ratings.copy()
#     new_df.rename(
#         columns={"userId": "user_id", "productId": "item_id"}, inplace=True
#     )
#     new_df = new_df[r_cols]
#     Y_data = new_df.values
#     rs = CF(Y_data, k=2, uuCF=0)
#     rs.fit()
#     for u in range(rs.n_items):
#             recommended_items = rs.recommend(u)
#             idProduct = train_set.idx2productid[u]
#             values = [
#                 train_set.idx2userid[item]
#                 for item in recommended_items
#                 if item in train_set.idx2userid
#             ]
#             print(f"{u}: {idProduct} - {recommended_items}: {values}")
#             key = f"collaborative_filtering_product_{idProduct}"
#             redis_instance.set_redis_data(key, values)
#     return make_response(jsonify({"result": "Training completed"}), 200)

@app.route('/train-get-items-by-item/<string:product_id>', methods=['GET'])
def train_get_items_by_item(product_id):
    # redis_instance = Redis()
    train_set = Loader()
    if product_id not in train_set.productid2idx:
        return make_response(jsonify({"result": []}), 200)
    idproductx = train_set.productid2idx[product_id]
    r_cols = ["user_id", "item_id", "rating"]
    new_df = train_set.ratings.copy()
    new_df.rename(
        columns={"userId": "user_id", "productId": "item_id"}, inplace=True
    )
    new_df = new_df[r_cols]
    Y_data = new_df.values
    rs = CF(Y_data, k=2, uuCF=0)
    rs.fit()
    print("idproductx", idproductx)
    recommended_items = rs.get_similar_items(idproductx)
    values = [
        train_set.idx2userid[item]
        for item in recommended_items
        if item in train_set.idx2userid
    ]
    print(f"{product_id}: {recommended_items}: {values}")
    # key = f"collaborative_filtering_user_{user_id}"
    # redis_instance.set_redis_data(key, values)

    return make_response(jsonify({"result": values}), 200)

@app.route('/get-recommendation-by-user/<string:user_id>', methods=['GET'])
def get_recommendation_by_user(user_id):
    redis_instance = Redis()
    train_set = Loader()
    if user_id not in train_set.userid2idx:
        return make_response(jsonify({"result": []}), 200)
    iduserx = train_set.userid2idx[user_id]
    r_cols = ["user_id", "item_id", "rating"]
    new_df = train_set.ratings.copy()
    new_df.rename(
        columns={"userId": "user_id", "productId": "item_id"}, inplace=True
    )
    new_df = new_df[r_cols]
    Y_data = new_df.values
    rs = CF(Y_data, k=2, uuCF=1)
    rs.fit()
    recommended_items = rs.recommend(iduserx)
    values = [
        train_set.idx2productid[item]
        for item in recommended_items
        if item in train_set.idx2productid
    ]
    print(f"{user_id}: {recommended_items}: {values}")
    key = f"collaborative_filtering_user_{user_id}"
    redis_instance.set_redis_data(key, values)

    return make_response(jsonify({"result": values}), 200)

@app.route('/train-by-time', methods=['GET'])
def train_by_time():
    redis_instance = Redis()
    products_result = training_collab_by_time()
    redis_instance.set_redis_data("collaborative_filtering_by_time", products_result)
    return make_response(jsonify({"result": products_result, 'total': len(products_result)}), 200)

# @app.route('/rmse', methods=['GET'])
# def rmse():
#     train_set = LoaderStartTrain()
#     r_cols = ["user_id", "item_id", "rating"]
#     ratings_train = train_set.ratings_train.copy()
#     ratings_train.rename(columns={"userId": "user_id", "productId": "item_id"}, inplace=True)
#     ratings_train = ratings_train[r_cols]
#     rate_train = ratings_train.values
#
#     r_cols = ["user_id", "item_id", "rating"]
#     ratings_test = train_set.ratings_test.copy()
#     ratings_test.rename(columns={"userId": "user_id", "productId": "item_id"}, inplace=True)
#     ratings_test = ratings_test[r_cols]
#     rate_test = ratings_test.values
#
#     rs = CF(rate_train, k=2, uuCF=1)
#     rs.fit()
#
#
#     n_tests = rate_test.shape[0]
#     SE = 0  # squared error
#
#     for n in range(n_tests):
#         print(n, "/", n_tests)
#         pred = rs.pred(rate_test[n, 0], rate_test[n, 1], normalized=0)
#         SE += (pred - rate_test[n, 2]) ** 2
#
#     RMSE = np.sqrt(SE / n_tests)
#     return make_response(jsonify({"result": RMSE}), 200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)