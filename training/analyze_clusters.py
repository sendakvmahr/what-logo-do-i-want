import numpy as np
import pickle
from numpy.linalg import norm
from sklearn.cluster import KMeans

"""
Analyzes clusters. Clusters that have too many similar members 
suggest that those clusters should be pruned for good variety
"""

def load_pickle(file):
	with open(file, "rb") as f: 
		return pickle.load(f)

#

# get num of points, and average of points
if __name__ == "__main__":
	data = load_pickle("data.pickle")
	cluster = load_pickle("cluster_algo.pickle")
	cluster_info = {}

	for i in range(cluster.n_clusters):
		cluster_info[i] = []

	for row in data:
		cluster_num = cluster.predict([row])[0]
		cluster_info[cluster_num].append(row)

	for i in range(cluster.n_clusters):
		cluster_center = cluster.cluster_centers_[i]
		points = np.array(cluster_info[i])
		count = len(points)
		#avg = np.linalg.norm([cluster_center], points)
		avg = np.linalg.norm(points - cluster_center, axis=1)
		avg = sum(avg) / count

		cluster_info[i] = [count, avg]

	with open("analysis.csv", "w") as file:
		file.write("id,count,avg\n")
		for i in range(cluster.n_clusters):
			info = cluster_info[i]
			file.write("{},{},{}\n".format(i, info[0], info[1]))




