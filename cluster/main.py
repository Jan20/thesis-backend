def cluster_cloud_function(request):

    import os, sys, json
    from models.user import User
    from cluster.cluster import Cluster

    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    
    request_json = request.get_json()

    cluster: Cluster = Cluster(number_of_clusters = 1)

    cluster.cluster_users()
    
    return "Clusters have been created."
