# Process thermal sensor data to detect group size via clustering

import numpy as np
from sklearn.cluster import DBSCAN
import serial

def get_thermal_data():
    # Simulated thermal sensor data
    return np.random.rand(100, 2) * 10  # (x, y) coordinates

def cluster_birds(data):
    clustering = DBSCAN(eps=1.5, min_samples=3).fit(data)
    n_clusters = len(set(clustering.labels_)) - (1 if -1 in clustering.labels_ else 0)
    return n_clusters, clustering.labels_

if __name__ == "__main__":
    from messaging.send_to_controller import send_thermal_alert

    data = get_thermal_data()
    count, labels = cluster_birds(data)
    send_thermal_alert(count)
