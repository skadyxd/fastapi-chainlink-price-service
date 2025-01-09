import json

with open('../abi/AggregatorV3Interface.json', 'r') as config_file:
    AggregatorV3Interface_abi = json.load(config_file)

with open('../abi/AccessControlledOCR2Aggregator.json', 'r') as config_file:
    AccessControlledOCR2Aggregator_abi = json.load(config_file)
