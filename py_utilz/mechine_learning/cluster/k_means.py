import numpy as np
from sklearn.cluster import KMeans

from py_utilz.file_util import write_to_csv
from py_utilz.plot_util import cluster_elbow


def k_means_cluster(features, k_range, feature_names=None, sample_keys=None, elbow_path=None, sample_result_path=None,
                    center_result_path=None, encoding='utf8'):
    """
    进行多次kmeans聚类
    :param features:
    :param k_range:
    :param feature_names:
    :param sample_keys:
    :param elbow_path:
    :param sample_result_path:
    :param center_result_path:
    :param encoding:
    :return:
    """
    if feature_names is None:
        feature_names = list(range(len(features)))
    kmeans_center_report = list()
    inertias = list()
    if sample_keys is not None:
        sample_cluster_id = [[k] for k in sample_keys]
    else:
        sample_cluster_id = [[i] for i in range(len(features))]
    for cluster_num in k_range:
        k_means = KMeans(n_clusters=cluster_num, n_jobs=2)
        k_means.fit(features)
        labels = k_means.predict(features)
        sample_num = list()
        cluster_names = list()

        for i in range(cluster_num):
            sample_num.append(np.count_nonzero(labels == i))
            cluster_names.append('cluster' + str(i))
        inertias.append(k_means.inertia_)
        kmeans_center_report.append([cluster_num])
        kmeans_center_report.append(['cluster'] + feature_names + ['cluster num'])
        kmeans_center_report.extend(np.concatenate((np.array(cluster_names).reshape(cluster_num, -1),
                                                    np.array(k_means.cluster_centers_),
                                                    np.array(sample_num).reshape(cluster_num, -1)), axis=1).tolist())
        for i in range(len(labels)):
            sample_cluster_id[i].append('cluster' + str(labels[i]))
        kmeans_center_report.append([])

    cluster_elbow(k_range, inertias, title='K-Means elbow', file_path=elbow_path)
    if sample_result_path is not None:
        write_to_csv(sample_result_path, sample_cluster_id, encoding=encoding)
    if center_result_path is not None:
        write_to_csv(center_result_path, kmeans_center_report)
