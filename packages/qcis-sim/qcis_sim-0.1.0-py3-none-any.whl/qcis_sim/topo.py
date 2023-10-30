import json
import os

file_path = os.path.dirname(__file__)
# FIX: path
with open(os.path.join(file_path, "config_66bit.json"), "r") as config_json:
    config = json.load(config_json)
    coupler_map = config["overview"]["coupler_map"]
    qubit_used = config["qubit"]["singleQubit"]["X/2 length"]["qubit_used"]
    qubit_used = sorted([int(i[1:]) for i in qubit_used])
    adjacency_list = []
    for Q1, Q2 in coupler_map.values():
        q1 = int(Q1[1:])
        q2 = int(Q2[1:])
        if q1 not in qubit_used and q2 not in qubit_used:
            continue
        adjacency_list.append([q2, q1])
    adjacency_list.sort()
