#!/usr/bin/env python
import json
import os
from collections import OrderedDict

DIRNAME = os.path.dirname(os.path.realpath(__file__))

print("Generating example_config.json from config.json")

config = json.load(open(
    os.path.join(DIRNAME, "..", "config.json"),
),object_pairs_hook=OrderedDict)

if "sensitive_keys" in config.keys():
    sensitive_keys = config["sensitive_keys"]
else:
    sensitive_keys = []

for _key in sensitive_keys:
    config[_key] = "your <{}>".format(_key)


filtered_config = json.dumps(config, indent=2)
print(filtered_config)
fp = open(os.path.join(
    DIRNAME, "..", "config.json.example"
), "w")
fp.write(filtered_config)
fp.close()
print("Written update config file to config.json.example")
