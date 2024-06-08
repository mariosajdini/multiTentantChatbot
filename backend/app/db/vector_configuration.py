from qdrant_client.models import VectorParams, Distance


class VectorConfiguration:
    def __init__(self, vector_size, distance_metric):
        self.vector_size = vector_size
        self.distance_metric = distance_metric
        self.distance = self.return_distance_metric()
        self.vector_params = VectorParams(
            size=self.vector_size,
            distance=self.distance
        )

    def get_vector_params(self):
        return self.vector_params

    def get_vector_size(self):
        return self.vector_size

    def get_distance_metric(self):
        return self.distance

    def return_distance_metric(self):
        if self.distance_metric == 'cosine':
            return Distance.COSINE
        elif self.distance_metric == 'dot':
            return Distance.DOT
        elif self.distance_metric == 'manhattan':
            return Distance.MANHATTAN
        elif self.distance_metric == 'euclid':
            return Distance.EUCLID
