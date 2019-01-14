import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.user import User
from evolution.evolution import Evolution

def evolution_cloud_function(request):

    user_key: str = request.args.get('user_key')
    session_key: str = request.args.get('session_key')
    level_key: str = request.args.get('level_key')

    evolution: Evolution = Evolution('user_042', 'session_042', 'level_01')

    evolution.execute()




