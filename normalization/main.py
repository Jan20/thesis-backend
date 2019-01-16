def normalization_cloud_function(request):

    import os
    import sys
    import json

    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    from models.user import User
    from normalization.normalization import Normalization
    
    user_key: str = request.args.get('user_key')

    normalization: Normalization = Normalization()
    normalization.calculate_average_performance(user_key)

    return "Performance of user " + user_key + " has been normalized."


