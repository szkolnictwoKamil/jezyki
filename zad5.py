import csv

import numpy as np


class KNearestNeighbors():
    def __init__(self, X_train, y_train, n_neighbors=5, weights='uniform', metric='euclidean'):

        self.X_train = X_train
        self.y_train = y_train

        self.n_neighbors = n_neighbors
        self.weights = weights
        self.metric= metric
        assert self.metric in ['euclidean', 'manhattan', 'chebyshev', 'cosine']

        self.n_classes = 2

    def train(self, X_train_new, Y_train_new):
        self.X_train = np.column_stack((X_train_new, Y_train_new))
        return self.X_train

    def euclidean_distance(self, a, b):
        return np.sqrt(np.sum((a - b)**2, axis=1))

    def manhattan_distance(self, a, b):
        return np.sum(np.abs(a - b), axis=1)

    def chebyshev_distance(self, a, b):
        return np.max(np.abs(a - b), axis=1)

    def cosine_distance(self, a, b):
        distances=[(1 - np.dot(a, b_) / (np.sqrt(np.dot(a, a)) * np.sqrt(np.dot(b_, b_)))) for b_ in b]

        return np.array(distances)

    def kneighbors(self, X_test, return_distance=False):

        dist = []
        neigh_ind = []

        callable = getattr(self, f'{self.metric}_distance')
        point_dist = [callable(x_test, self.X_train) for x_test in X_test]

        for row in point_dist:
            enum_neigh = enumerate(row)
            sorted_neigh = sorted(enum_neigh,
                                  key=lambda x: x[1])[:self.n_neighbors]

            ind_list = [tup[0] for tup in sorted_neigh]
            dist_list = [tup[1] for tup in sorted_neigh]

            dist.append(dist_list)
            neigh_ind.append(ind_list)

        if return_distance:
            return np.array(dist), np.array(neigh_ind)

        return np.array(neigh_ind)

    def predict(self, X_test):

        if self.weights == 'uniform':
            neighbors = self.kneighbors(X_test)
            y_pred = np.array([
                np.argmax(np.bincount(self.y_train[neighbor]))
                for neighbor in neighbors
            ])

            return y_pred

        if self.weights == 'distance':

            dist, neigh_ind = self.kneighbors(X_test, return_distance=True)

            inv_dist = 1 / dist

            mean_inv_dist = inv_dist / np.sum(inv_dist, axis=1)[:, np.newaxis]

            proba = []

            for i, row in enumerate(mean_inv_dist):

                row_pred = self.y_train[neigh_ind[i]]

                for k in range(self.n_classes):
                    indices = np.where(row_pred == k)
                    prob_ind = np.sum(row[indices])
                    proba.append(np.array(prob_ind))

            predict_proba = np.array(proba).reshape(X_test.shape[0],
                                                    self.n_classes)

            y_pred = np.array([np.argmax(item) for item in predict_proba])

            return y_pred

    def score(self, X_test, y_test):
        y_pred = self.predict(X_test)

        return float(sum(y_pred == y_test)) / float(len(y_test))

data = np.genfromtxt("C:/repo/dataset1.csv", delimiter='')


split_rate = 0.7

train, test = np.split(data, [int(split_rate * (data.shape[0]))])

X_train = train[:, :-1]
y_train = train[:, -1]

X_test = test[:, :-1]
y_test = test[:, -1]

y_train = y_train.astype(int)
y_test = y_test.astype(int)

# print(y_train)

neighbor = KNearestNeighbors(X_train, y_train, metric='cosine')

print(neighbor.kneighbors(X_test))
print(neighbor.predict(X_test))
print(neighbor.predict(X_test[:1]))
print(neighbor.score(X_test, y_test))
print(neighbor.predict([[7, 7]]))
print(neighbor.predict([[17, 10]]))

with open ('dane.csv', 'a', newline='') as file:
    w = csv.writer(file, delimiter = ' ')
    w.writerows(neighbor.train(X_train, y_train))