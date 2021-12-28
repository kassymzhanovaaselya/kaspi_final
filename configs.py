import os
import json

filename = 'config.json'
file_ = open(filename, 'r')
configs = json.loads(file_.read())
