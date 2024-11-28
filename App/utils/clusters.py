import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
import pickle
from database.connection import *
import random

def create_and_save_clusters(query, n_clusters=20, filename='cluster_info.pkl'):
    # Connect to your database
    conn = connect()
    cur = conn.cursor()
    #cur.execute('SELECT version()')
    #db_version = cur.fetchone()
    #print(db_version)

    # Load data into a DataFrame
    df = pd.read_sql_query(query, conn)

    # Close the connection
    #conn.close()

    print("Clustering data")
    # Select features for clustering
    X = df[['latitude', 'longitude']]

    # Apply K-Means clustering
    kmeans = KMeans(n_clusters=n_clusters)
    df['cluster'] = kmeans.fit_predict(X)

    # Calculate the average speed for each cluster
    cluster_info = {}
    for cluster in df['cluster'].unique():
        cluster_data = df[df['cluster'] == cluster]
        avg_speed = cluster_data['speed'].mean()

        # Compute the Convex Hull
        points = cluster_data[['latitude', 'longitude']].values
        hull = ConvexHull(points)

        # Save the cluster information
        cluster_info[cluster] = {
            'average_speed': avg_speed,
            'convex_hull': hull
        }

    # Save the cluster information to a file
    with open(filename, 'wb') as f:
        pickle.dump(cluster_info, f)

    return df, cluster_info

def classify_new_point(lat, lon, speed, cluster_info):
    point = np.array([lat, lon])
    for cluster, info in cluster_info.items():
        hull = info['convex_hull']
        if all(np.dot(eq[:-1], point) + eq[-1] <= 0 for eq in hull.equations):
            avg_speed = info['average_speed']
            if speed > avg_speed:
                return cluster, 'above average'
            else:
                return cluster, 'below average'
    return None, 'outside all clusters'

def display_cluster_borders(df, cluster_info, new_point=None):
    plt.figure(figsize=(10, 8))
    for cluster in df['cluster'].unique():
        cluster_data = df[df['cluster'] == cluster]
        plt.scatter(cluster_data['latitude'], cluster_data['longitude'], label=f'Cluster {cluster}')

        # Plot the Convex Hull
        points = cluster_data[['latitude', 'longitude']].values
        hull = cluster_info[cluster]['convex_hull']
        for simplex in hull.simplices:
            plt.plot(points[simplex, 0], points[simplex, 1], 'k-')

    if new_point:
        new_lat, new_lon = new_point
        plt.scatter(new_lat, new_lon, color='black', s=100, label='New GPS Data Point')

    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title('GPS Data Clustering with Convex Hull Boundaries')
    plt.legend()
    plt.show()

# Generate a list of random colors
def generate_random_colors(num_colors):
    colors = []
    for _ in range(num_colors):
        color = f'rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, 0.2)'
        colors.append(color)
    return colors

"""

# Example usage
query = "SELECT time, latitude, longitude, elevation, speed FROM sandbox.gps_c07 ORDER BY time"
df, cluster_info = create_and_save_clusters(query)

# Classify a new GPS data point
new_lat = -22.965998
new_lon = -69.076355
new_speed = 44

with open('cluster_info.pkl', 'rb') as f:
    loaded_cluster_info = pickle.load(f)

cluster, speed_comparison = classify_new_point(new_lat, new_lon, new_speed, loaded_cluster_info)
print(f'New point belongs to cluster {cluster} and its speed is {speed_comparison}.')

# Display the clusters and their boundaries
display_cluster_borders(df, cluster_info, new_point=(new_lat, new_lon))
"""