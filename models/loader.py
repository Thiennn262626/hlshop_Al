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