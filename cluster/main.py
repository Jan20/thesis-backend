def cluster_cloud_function(request):

    import os, sys, json
    from models.user import User
    from cluster.cluster import Cluster
    
    request_json = request.get_json()

    cluster: Cluster = Cluster(number_of_clusters = 1)

    cluster.cluster_users()
    
    return "Clusters have been created."
