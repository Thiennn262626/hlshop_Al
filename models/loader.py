from controllers.ratings import get_rating_list

class Loader():
    def __init__(self):
        self.ratings = get_rating_list()
        ratings_df = self.ratings
        # Extract all user IDs and product IDs
        users = ratings_df.userId.unique()
        product = ratings_df.productId.unique()

        self.userid2idx = {o: i for i, o in enumerate(users)}
        self.productid2idx = {o: i for i, o in enumerate(product)}
        self.idx2userid = {i: o for o, i in self.userid2idx.items()}
        self.idx2productid = {i: o for o, i in self.productid2idx.items()}

        self.ratings.productId = ratings_df.productId.apply(
            lambda x: self.productid2idx[x]
        )
        self.ratings.userId = ratings_df.userId.apply(lambda x: self.userid2idx[x])


class LoaderStartTrain():
    def __init__(self):
        self.ratings = get_rating_list()
        ratings_df = self.ratings
        ratings_train = ratings_df.sample(frac=0.9)
        ratings_test = ratings_df.drop(ratings_train.index)
        # Extract all user IDs and product IDs
        users_train = ratings_train.userId.unique()
        product_train = ratings_train.productId.unique()
        print("users_train", users_train.shape)
        print("product_train", product_train.shape)
        self.userid2idx = {o: i for i, o in enumerate(users_train)}
        self.productid2idx = {o: i for i, o in enumerate(product_train)}
        self.idx2userid = {i: o for o, i in self.userid2idx.items()}
        self.idx2productid = {i: o for o, i in self.productid2idx.items()}

        users_test = ratings_test.userId.unique()
        product_test = ratings_test.productId.unique()

        self.userid2idx_test = {o: i for i, o in enumerate(users_test)}
        self.productid2idx_test = {o: i for i, o in enumerate(product_test)}
        self.idx2userid_test = {i: o for o, i in self.userid2idx_test.items()}
        self.idx2productid_test = {i: o for o, i in self.productid2idx_test.items()}

        ratings_train.productId = ratings_train.productId.apply(
            lambda x: self.productid2idx[x]
        )
        ratings_train.userId = ratings_train.userId.apply(lambda x: self.userid2idx[x])

        ratings_test.productId = ratings_test.productId.apply(
            lambda x: self.productid2idx_test[x]
        )
        ratings_test.userId = ratings_test.userId.apply(lambda x: self.userid2idx_test[x])

        self.ratings_train = ratings_train
        self.ratings_test = ratings_test
