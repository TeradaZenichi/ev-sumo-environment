from environment import SingleEV


import json 



"""Load config at config/config.json"""
with open(r'config/config.json', 'r') as config_file:
    config = json.load(config_file)

with open('config/vehicles.json', "r", encoding="utf-8") as f:
    vehicles = json.load(f)


def main():
    start = "00:00"  # definir um dia, mes e ano e usar datetime
    env = SingleEV(config, vehicles, start)
    pass

if __name__ == "__main__":
    main()