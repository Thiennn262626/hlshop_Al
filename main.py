from flask import Flask
from dotenv import load_dotenv
from flask import jsonify, make_response

load_dotenv()
app = Flask(__name__)

from models.loader import Loader
from models.collaborative_filtering import CF
from dbs.redis import redis_instance

@app.route("/", methods=["GET"])
def read_root():
    return {"Hello": "World"}

@app.route('/train-full', methods=['GET'])
def train_full():
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
            redis_instance.set_redis_data(key, values, 36000)
    return make_response(jsonify({"result": "Training completed"}), 200)

@app.route('/get-recommendation-by-user/<string:user_id>', methods=['GET'])
def get_recommendation_by_user(user_id):
    train_set = Loader()
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
    redis_instance.set_redis_data(key, values, 600)

    return make_response(jsonify({"result": values}), 200)

        


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3456)