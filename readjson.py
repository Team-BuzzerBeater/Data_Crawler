import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, 'shoot_info_91011.json'), 'r') as f:
    json_data = json.load(f)
    #json_data = [play for play in json_data if "TYPE_CD" in play and play["TYPE_CD"] == "ST"]
print(json.dumps(json_data, indent ='\t'))
'''
with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as file:
    json.dump(json_data,file)
'''