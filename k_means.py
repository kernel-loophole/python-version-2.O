import numpy as np
class k_means:
    def __init__(self, k, tol, max_iter):
        self.k = k
        self.tol = tol
        self.max_iter = max_iter

    def fit(self, X):
        n_samples, n_features = X.shape
        self.centroids = {}
        for i in range(self.k):
            self.centroids[i] = X[i]
        for i in range(self.max_iter):
            self.classifications = {}
            for i in range(self.k):
                self.classifications[i] = []
            for featureset in X:
                distances = [np.linalg.norm(featureset - self.centroids[centroid]) for centroid in self.centroids]
                classification = distances.index(min(distances))
                self.classifications[classification].append(featureset)
            prev_centroids = dict(self.centroids)
            for classification in self.classifications:
                self.centroids[classification] = np.average(self.classifications[classification], axis=0)
            optimized = True
            for c in self.centroids:
                original_centroid = prev_centroids[c]
                current_centroid = self.centroids[c]
                if np.sum((current_centroid - original_centroid) / original_centroid * 100.0) > self.tol:
                    optimized = False
            if optimized:
                break
    def predict(self, X):
        distances = [np.linalg.norm(X - self.centroids[centroid]) for centroid in self.centroids]
        classification = distances.index(min(distances))
        return classification
    def score(self, X):
        score = 0
        for i in range(len(X)):
            distances = [np.linalg.norm(X[i] - self.centroids[centroid]) for centroid in self.centroids]
            classification = distances.index(min(distances))
            score += classification
    
        
    def get_centroids(self):
        return self.centroids
        
        
if __name__ == '__main__':
    X = np.array([[1, 2], [1.5, 1.8], [5, 8], [8, 8], [1, 0.6], [9, 11]])
    k_means = k_means(3, 1, 10)
    
    k_means.fit(X)
    centroids = k_means.get_centroids()
    for centroid in centroids:
        print(centroids[centroid])