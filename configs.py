import os
import json

filename = 'configs.json'
file_ = open(filename, 'r')
configs = json.loads(file_.read())
