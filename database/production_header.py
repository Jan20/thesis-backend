import os
import sys

from google.cloud import firestore

server_timestamp = firestore.SERVER_TIMESTAMP
db = firestore.Client()
