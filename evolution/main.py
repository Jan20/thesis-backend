def evolution_cloud_function(request):
    
    import os
    import sys
    import json

    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    from models.user import User
    from evolution.evolution import Evolution
    from models.level import Level

    request_json = request.get_json(silent=True)
    request_args = request.args

    user_key: str

    if request_json and 'user_key' in request_json:
    
        user_key = request_json['user_key']
    
    elif request_args and 'user_key' in request_args:
    
        user_key = request_args['user_key']
    
    else:
    
        user_key = 'User not found.'

    #
    #
    #
    session_key: str = Evolution().execute(user_key)

    #
    #
    #
    return f'Session {session_key} has been created.'


# if __name__ == "__main__":
    
#     evolution_cloud_function()

