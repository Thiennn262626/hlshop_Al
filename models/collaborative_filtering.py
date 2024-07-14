import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse

class CF(object):
    def __init__(self, Y_data, k, dist_func=cosine_similarity, uuCF=1):
        self.uuCF = uuCF  # user-user (1) or item-item (0) CF
        self.Y_data = Y_data if uuCF else Y_data[:, [1, 0, 2]]
        self.k = k  # number of neighbor points
        self.dist_func = dist_func
        self.Ybar_data = None
        # number of users and items. Remember to add 1 since id starts from 0
        self.n_users = int(np.max(self.Y_data[:, 0])) + 1
        self.n_items = int(np.max(self.Y_data[:, 1])) + 1
        print("Number of users = ", self.n_users, "and number of items = ", self.n_items)
        print("CF model with k = ", self.k)

    def add(self, new_data):
        self.Y_data = np.concatenate((self.Y_data, new_data), axis=0)

    def normalize_Y(self):
        users = self.Y_data[:, 0] # all users - first col of the Y_data
        self.Ybar_data = self.Y_data[:, :3].astype(np.float64).copy()
        self.mu = np.zeros((self.n_users,))
        for n in range(self.n_users):
            ids = np.where(users == n)[0].astype(np.int32)
            item_ids = self.Y_data[ids, 1]
            ratings = self.Y_data[ids, 2]
            # avg rating dulicate item_ids
            if(item_ids.size > 1):
                unique_item_ids = np.unique(item_ids)
                for item_id in unique_item_ids:
                    idx = np.where(item_ids == item_id)[0]
                    if len(idx) > 1:
                        average_rating = np.mean(ratings[idx])
                        self.Ybar_data[ids[idx[:-1]], 2] = average_rating - self.mu[n]
                        #update ratings
                        ratings[idx] = average_rating

            m = np.mean(ratings)
            if np.isnan(m):
                m = 0
            # self.mu[n] = m
            # normalize
            self.Ybar_data[ids, 2] = ratings - self.mu[n]


        self.Ybar = sparse.coo_matrix((self.Ybar_data[:, 2],
            (self.Ybar_data[:, 1], self.Ybar_data[:, 0])), (self.n_items, self.n_users))
        self.Ybar = self.Ybar.tocsr()

    def similarity(self):
        self.S = self.dist_func(self.Ybar.T, self.Ybar.T)

    def refresh(self):
        self.normalize_Y()
        self.similarity()

    def fit(self):
        self.refresh()

    def __pred(self, u, i, normalized=1):
        ids = np.where(self.Y_data[:, 1] == i)[0].astype(np.int32)
        users_rated_i = (self.Y_data[ids, 0]).astype(np.int32)
        sim = self.S[u, users_rated_i]
        a = np.argsort(sim)[-self.k :]
        nearest_s = sim[a]
        r = self.Ybar[i, users_rated_i[a]]
        if normalized:
            return (r * nearest_s)[0] / (np.abs(nearest_s).sum() + 1e-8)

        return (r * nearest_s)[0] / (np.abs(nearest_s).sum() + 1e-8) + self.mu[u]

    def pred(self, u, i, normalized=1):
        if self.uuCF:
            return self.__pred(u, i, normalized)
        return self.__pred(i, u, normalized)

    def get_similar_items(self, item_id):
        ids = np.where(self.Y_data[:, 1] == item_id)[0].astype(np.int32)
        users_rated_i = (self.Y_data[ids, 0]).astype(np.int32)
        sim = self.S[item_id, users_rated_i]
        a = np.argsort(sim)[-self.k :]
        return self.Y_data[users_rated_i[a], 1].astype(np.int32)

    def recommend(self, u, normalized=1):
        ids = np.where(self.Y_data[:, 0] == u)[0]
        items_rated_by_u = self.Y_data[ids, 1].tolist()
        recommended_items = []
        for i in range(self.n_items):
            if i not in items_rated_by_u:
                rating = self.__pred(u, i)
                if rating > 0:
                    recommended_items.append(i)

        return recommended_items

    def print_recommendation(self):
        for u in range(self.n_users):
            recommended_items = self.recommend(u)
            if self.uuCF:
                print("    Recommend item(s):", recommended_items, "for user", u)
            else:
                print("    Recommend item", u, "for user(s) : ", recommended_items)
