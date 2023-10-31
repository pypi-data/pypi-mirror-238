import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


class SpikeSorter:

    def __init__(self, data):
        self.data = data
        self.output = None
        self.noise = None

    def detect_noise(self):
        self.noise = [all(spike < 0) or all(spike > 0) for spike in self.data]
        return self

    def pca(self, num_components):
        pca = PCA(n_components=num_components)
        self.data = pca.fit_transform(self.data)
        return self

    def kmeans(self, num_clusters):
        # Apply K-means clustering
        kmeans = KMeans(n_clusters=num_clusters, n_init='auto')
        labels = kmeans.fit_predict(self.data)
        self.output = [int(lab) + 1 for lab in labels]
        if self.noise is not None:
            self.output = [-1 if noise else lab for noise, lab in zip (self.noise, self.output)]
        return self

    def run(self):
        return self.output
