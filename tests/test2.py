import yaml


with open('config2.yaml', 'r') as yaml_file:
    config = yaml.safe_load(yaml_file)
    
user2 = config["config"]["credentials"]["oeg"]["username"]
print(user2)