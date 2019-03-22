def evolution_cloud_function(request):
    
    import os
    import sys
    import json

    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    from models.user import User
    from evolution.evolution import Evolution
    from models.level import Level

    from normalization.normalization import Normalization
    
    request_json = request.get_json(silent=True)
    request_args = request.args

    # Declares a variable to store a user key.
    user_key: str

    if request_json and 'user_key' in request_json:
    
        user_key = request_json['user_key']
    
    elif request_args and 'user_key' in request_args:
    
        user_key = request_args['user_key']
    
    else:
    
        user_key = 'User not found.'

    # Executes the actual evolution process by creating
    # an Evolution objects and calling the execute function
    # the retrieved user key.
    session_key: str = Evolution().execute(user_key)


    # Retruns a simple success message after the evolution
    # process has been terminated.
    return f'Session {session_key} has been created.'