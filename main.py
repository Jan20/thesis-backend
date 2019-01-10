# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import logging

import numpy as np
from flask import Flask
from sklearn.cluster import KMeans

from computations.cluster import Cluster
from computations.transform import Transform
from models.performance import Performance
from evolution.evolution import Evolution

app = Flask(__name__)

# def quickstart_new_instance():
#     # [START quickstart_new_instance]
#     from google.cloud import firestore

#     # Project ID is determined by the GCLOUD_PROJECT environment variable
#     db = firestore.Client()
#     # [END quickstart_new_instance]

#     return db

@app.route('/api/compute/average/performance/<user_key>')
def tescalculate_average_performancet(user_key: str):

    return Transform().calculate_average_performance(user_key)


@app.route('/api/compute/cluster')
def cluster_users() -> str:

    return str(Cluster().cluster_users())

@app.route('/api/evolve/level/<user_key>/<session_key>/<level_key>')
def evolve_level(user_key: str, session_key: str, level_key: str) -> str:

    return Evolution(level_key, user_key, session_key).load_level()

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
    
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=False)

# [END gae_python37_app]
