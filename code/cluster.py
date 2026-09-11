
import csv
from sklearn.cluster import KMeans
import numpy as np

channel_file = "new_channel.csv"


def cluster_data(channel_file):
	file = open(channel_file, "r")
	channel = list(csv.reader(file, delimiter=","))
	channel.pop(0)
	channel = np.array(channel)
	file.close()
	channel = channel[:,1:]
	print(channel)

	num_clusters = 2
	kmeans = KMeans(n_clusters=num_clusters, random_state=42)
	kmeans.fit(channel)
	cluster_labels = kmeans.labels_
	clustered_data = list(zip(channel, cluster_labels))
	# Print the clustered data
	#for row, cluster in clustered_data:
	#	print(f"Row: {row}, Cluster: {cluster}")
	return cluster_data

cluster_data(channel_file)